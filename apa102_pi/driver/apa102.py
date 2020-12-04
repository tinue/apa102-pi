"""This is the main driver module for APA102 LEDs"""
import busio
import adafruit_bitbangio as bitbangio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
from math import ceil

RGB_MAP = {'rgb': [3, 2, 1], 'rbg': [3, 1, 2], 'grb': [2, 3, 1],
           'gbr': [2, 1, 3], 'brg': [1, 3, 2], 'bgr': [1, 2, 3]}


class APA102:
    """
    Driver for APA102 LEDS (aka "DotStar").

    (c) Martin Erzberger 2016-2020

    Public methods are:
     - set_pixel
     - set_pixel_rgb
     - show
     - clear_strip
     - cleanup

    Helper methods for color manipulation are:
     - combine_color
     - wheel

    The rest of the methods are used internally and should not be used by the
    user of the library. This file is the main driver, and is usually used "as is".

    Very brief overview of APA102: An APA102 LED is addressed with SPI. The bits
    are clocked in one by one, starting with the least significant bit.

    An LED usually just copies everything that is sent to its data-in to
    data-out. While doing this, it remembers its own color and keeps glowing
    with that color as long as there is power.

    An LED can be switched to not forward the data, but instead use the data
    to change it's own color. This is done by sending (at least) 32 bits of
    zeroes to data-in. The LED then accepts the next correct 32 bit LED
    frame (with color information) as its new color setting.

    After having received the 32 bit color frame, the LED changes color,
    and then resumes to just copying data-in to data-out.

    The really clever bit is this: While receiving the 32 bit LED frame,
    the LED sends zeroes on its data-out line. Because a color frame is
    32 bits, the LED sends 32 bits of zeroes to the next LED.
    As we have seen above, this means that the next LED is now ready
    to accept a color frame and update its color.

    So that's really the entire protocol:
    - Start by sending 32 bits of zeroes. This prepares LED 1 to update
      its color.
    - Send color information one by one, starting with the color for LED 1,
      then LED 2 etc.
    - Finish off by cycling the clock line a few times to get all data
      to the very last LED on the strip

    The last step is necessary, because each LED delays forwarding the data
    a bit. Imagine ten people in a row. When you tell the last color
    information, i.e. the one for person ten, to the first person in
    the line, then you are not finished yet. Person one has to turn around
    and tell it to person 2, and so on. So it takes ten additional "dummy"
    cycles until person ten knows the color. When you look closer,
    you will see that not even person 9 knows its own color yet. This
    information is still with person 2. Essentially the driver sends additional
    zeroes to LED 1 as long as it takes for the last color frame to make it
    down the line to the last LED.
    """
    # Constants
    LED_START = 0b11100000  # Three "1" bits, followed by 5 brightness bits

    def __init__(self, num_led=8, order='rgb', mosi=10, sclk=11, ce=None, bus_speed_hz=8000000):
        """Initializes the library

        :param num_led: Number of LEDs in the strip
        :param order: Order in which the colours are addressed (this differs from strip to strip)
        :param mosi: Master Out pin. Use 10 for SPI0, 20 for SPI1, any GPIO pin for bitbang.
        :param sclk: Clock, use 11 for SPI0, 21 for SPI1, any GPIO pin for bitbang.
        :param ce: GPIO to use for Chip select. Can be any free GPIO pin. Warning: This will slow down the bus
                   significantly. Note: The hardware CE0 and CE1 are not used
        :param bus_speed_hz: Speed of the hardware SPI bus. If glitches on the bus are visible, lower the value.
        """
        self.num_led = num_led
        order = order.lower()  # Just in case someone use CAPS here.
        self.rgb = RGB_MAP.get(order, RGB_MAP['rgb'])
        self.global_brightness = 4  # This is a 5 bit value, i.e. from 0 to 31. Conservative 1/8th, change if desired.
        self.use_bitbang = False  # Two raw SPI devices exist: Bitbang (software) and hardware SPI.
        self.use_ce = False  # If true, use the BusDevice abstraction layer on top of the raw SPI device

        self.leds = [self.LED_START, 0, 0, 0] * self.num_led  # Pixel buffer
        if ce is not None:
            # If a chip enable value is present, use the Adafruit CircuitPython BusDevice abstraction on top
            # of the raw SPI device (hardware or bitbang)
            # The next line is just here to prevent an "unused" warning from the IDE
            digitalio.DigitalInOut(board.D1)
            # Convert the chip enable pin number into an object (reflection à la Python)
            ce = eval("digitalio.DigitalInOut(board.D"+str(ce)+")")
            self.use_ce = True
        # Heuristic: Test for the hardware SPI pins. If found, use hardware SPI, otherwise bitbang SPI
        if mosi == 10:
            if sclk != 11:
                raise ValueError("Illegal MOSI / SCLK combination")
            self.spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI)
        elif mosi == 20:
            if sclk != 21:
                raise ValueError("Illegal MOSI / SCLK combination")
            self.spi = busio.SPI(clock=board.SCLK_1, MOSI=board.MOSI_1)
        else:
            # Use Adafruit CircuitPython BitBangIO, because the pins do not match one of the hardware SPI devices
            # Reflection à la Python to get at the digital IO pins
            self.spi = bitbangio.SPI(clock=eval("board.D"+str(sclk)), MOSI=eval("board.D"+str(mosi)))
            self.use_bitbang = True
        # Add the BusDevice on top of the raw SPI
        if self.use_ce:
            self.spibus = SPIDevice(spi=self.spi,  chip_select=ce, baudrate=bus_speed_hz)
        else:
            # If the BusDevice is not used, the bus speed is set here instead
            while not self.spi.try_lock():
                # Busy wait to acquire the lock
                pass
            self.spi.configure(baudrate=bus_speed_hz)
            self.spi.unlock()
        # Debug
        if self.use_ce:
            print("Use software chip enable")
        if self.use_bitbang:
            print("Use bitbang SPI")
        else:
            print("Use hardware SPI")

    def clock_start_frame(self):
        """Sends a start frame to the LED strip.

        This method clocks out a start frame, telling the receiving LED
        that it must update its own color now.
        """
        self.send_to_spi(bytes([0] * 4))

    def clock_end_frame(self):
        """Sends an end frame to the LED strip.

        As explained above, dummy data must be sent after the last real colour
        information so that all of the data can reach its destination down the line.
        The delay is not as bad as with the human example above.
        It is only 1/2 bit per LED. This is because the SPI clock line
        is being inverted by the LED chip.

        Say a bit is ready on the SPI data line. The sender communicates
        this by toggling the clock line. The bit is read by the LED
        and immediately forwarded to the output data line. When the clock goes
        down again on the input side, the LED will toggle the clock up
        on the output to tell the next LED that the bit is ready.

        After one LED the clock is inverted, and after two LEDs it is in sync
        again, but one cycle behind. Therefore, for every two LEDs, one bit
        of delay gets accumulated. For 300 LEDs, 150 additional bits must be fed to
        the input of LED one so that the data can reach the last LED.

        Ultimately, we need to send additional numLEDs/2 arbitrary data bits,
        in order to trigger numLEDs/2 additional clock changes. This driver
        sends zeroes, which has the benefit of getting LED one partially or
        fully ready for the next update to the strip. An optimized version
        of the driver could omit the "clockStartFrame" method if enough zeroes have
        been sent as part of "clockEndFrame".
        """
        # Send reset frame necessary for SK9822 type LEDs
        self.send_to_spi(bytes([0] * 4))
        for _ in range((self.num_led + 15) // 16):
            self.send_to_spi([0x00])

    def set_global_brightness(self, brigtness):
        """ Set the overall brightness of the strip."""
        self.global_brightness = brigtness

    def clear_strip(self):
        """ Turns off the strip and shows the result right away."""

        for led in range(self.num_led):
            self.set_pixel(led, 0, 0, 0)
        self.show()

    def set_pixel(self, led_num, red, green, blue, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed individually.
        If brightness is not set the global brightness setting is used.
        """
        if led_num < 0:
            return  # Pixel is invisible, so ignore
        if led_num >= self.num_led:
            return  # again, invisible

        # Calculate pixel brightness as a percentage of the
        # defined global_brightness. Round up to nearest integer
        # as we expect some brightness unless set to 0
        brightness = ceil(bright_percent * self.global_brightness / 100.0)
        brightness = int(brightness)

        # LED start frame is three "1" bits, followed by 5 brightness bits
        ledstart = (brightness & 0b00011111) | self.LED_START

        start_index = 4 * led_num
        self.leds[start_index] = ledstart
        self.leds[start_index + self.rgb[0]] = red
        self.leds[start_index + self.rgb[1]] = green
        self.leds[start_index + self.rgb[2]] = blue

    def set_pixel_rgb(self, led_num, rgb_color, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer.
        Colors are passed combined (3 bytes concatenated)
        If brightness is not set the global brightness setting is used.
        """
        self.set_pixel(led_num, (rgb_color & 0xFF0000) >> 16,
                       (rgb_color & 0x00FF00) >> 8, rgb_color & 0x0000FF,
                       bright_percent)

    def rotate(self, positions=1):
        """ Rotate the LEDs by the specified number of positions.

        Treating the internal LED array as a circular buffer, rotate it by
        the specified number of positions. The number could be negative,
        which means rotating in the opposite direction.
        """
        cutoff = 4 * (positions % self.num_led)
        self.leds = self.leds[cutoff:] + self.leds[:cutoff]

    def show(self):
        """Sends the content of the pixel buffer to the strip.

        Todo: More than 1024 LEDs requires more than one xfer operation.
        """
        self.clock_start_frame()
        # xfer2 kills the list, unfortunately. So it must be copied first
        # SPI takes up to 4096 Integers. So we are fine for up to 1024 LEDs.
        self.send_to_spi(self.leds)
        self.clock_end_frame()

    def cleanup(self):
        """Release the SPI device; Call this method at the end"""
        # Try to unlock, in case it is still locked
        try:
            self.spi.unlock()  # Unlock first
        except ValueError:
            # Do nothing, the bus was not locked
            pass
        self.clear_strip()
        self.spi.deinit()  # Close SPI port

    @staticmethod
    def combine_color(red, green, blue):
        """Make one 3*8 byte color value."""

        return (red << 16) + (green << 8) + blue

    def wheel(self, wheel_pos):
        """Get a color from a color wheel; Green -> Red -> Blue -> Green"""

        if wheel_pos > 255:
            wheel_pos = 255  # Safeguard
        if wheel_pos < 85:  # Green -> Red
            return self.combine_color(wheel_pos * 3, 255 - wheel_pos * 3, 0)
        if wheel_pos < 170:  # Red -> Blue
            wheel_pos -= 85
            return self.combine_color(255 - wheel_pos * 3, 0, wheel_pos * 3)
        # Blue -> Green
        wheel_pos -= 170
        return self.combine_color(0, wheel_pos * 3, 255 - wheel_pos * 3)

    def send_to_spi(self, data):
        """Internal method to output data to the chosen SPI device"""
        if self.use_ce:
            with self.spibus as bus_device:
                bus_device.write(data)
        elif self.use_bitbang:
            while not self.spi.try_lock():
                # Busy wait to acquire the lock
                pass
            self.spi.write(data)
            self.spi.unlock()
        else:
            self.spi.write(data)

    def dump_array(self):
        """For debug purposes: Dump the LED array onto the console."""

        print(self.leds)
