import spidev

"""
Driver for APA102 LEDS (aka "DotStar").
(c) Martin Erzberger 2015

My very first Python code, so I am sure there is a lot to be optimized ;)

Public methods are:
 - setPixel
 - setPixelRGB
 - show
 - clearStrip
 - cleanup
 
Helper methods for color manipulation are:
 - combineColor
 - wheel
 
The rest of the methods are used internally and should not be used by the user of the library.

Very brief overview of APA102: An APA102 LED is addressed with SPI. The bits are shifted in one by one, 
starting with the least significant bit.

An LED usually just copies everything that is sent to it via data-in to its data-out. While doing this, it
remembers its own color and keeps glowing with that color as long as there is power. If the color of a
particular LED must be updated, then (at least) 32 bits of zeroes must be sent to data-in. The LED then
accepts the next real 32 bit LED frame (with color information) as its new color setting.

After having received the 32 bit color frame, the LED changes color, and then goes on to just copying
data-in to data-out.

The really clever bit is this: While receiving the 32 bit LED frame, the LED sends all zeroes on its
data-out line. So the next LED down the strip receives a "color change" frame automatically. Since the
next 32 bits are then just copied by LED 1 to LED 2, LED 2 now updates its color, and preps LED 3 at
the same time.

So that's really the entire protocol:
- Start LED 1 with 32 bits of zeroes
- Send one 32 bit color frame per LED on the strip to data-in of the first LED
- Finish off by cycling the clock line a few times to get all data to the very last LED on the strip
"""
class APA102:
    def __init__(self, numLEDs, globalBrightness = 31): # The number of LEDs in the Strip
        self.numLEDs = numLEDs
        # LED startframe is three "1" bits, followed by 5 brightness bits
        self.ledstart = (globalBrightness & 0b00011111) | 0b11100000 # Don't validate, just slash of extra bits
        self.leds = [] # Pixel buffer
        for _ in range(self.numLEDs): # Allocate the entire buffer. If later some LEDs are not set,
            self.leds.extend([self.ledstart]) # they will just be black,
            self.leds.extend([0x00] * 3) #  instead of crashing the driver.
        self.spi = spidev.SpiDev()  # Init the SPI device
        self.spi.open(0, 1)  # Open SPI port 0, slave device (CS)  1
        self.spi.max_speed_hz=8000000 # Up the speed a bit, so that the LEDs are painted faster
    
    """
    This method clocks out a start frame, telling the receiving LED that it must update its own color now.
    """
    def clockStartFrame(self):
        _ = self.spi.xfer2([0x00, 0x00, 0x00, 0x00])  # Start frame, 32 zero bits
    
    """
    The end frame is not really a data package. Its purpose is to trigger additional clock pulses. The clock pulses
    are required because of the way SPI works. In SPI, the first step is to set a stable data signal. Then, the
    clock signal is raised. This triggers the receiver to read the data line.
    This works fine for one LED. But the second LED has a problem with this. As soon as LED one reads data on its
    data-in, it should prepare data on data-out. But it can't do this while the clock line is "high". So LED one
    will invert the clock signal.
    When the clock-in of LED one is high, LED one sets its clock-out to low.
    It readies its data-out, and as soon as the LED one input clock is lowered in order to prepare the next input for
    LED one, the clock-out of LED one is raised, and LED 2 can read the data line. 
    This goes on like this through the entire strip. Each LED delays its data-out by 1/2 clock cycle by inverting the 
    clock signal. At the end of the strip, we are numLEDs/2 clock cycles behind. Usually this means that the last LED did not
    yet receive all of its data (32 bits is a full LED data frame, so if the strip has 64 LEDs or less, then only the last LED
    is affected).
    Ultimately, we need to send additional numLEDs/2 arbitrary data bits, in order to trigger numLEDs/2 additional clock
    changes. This driver sends zeroes, which has the benefit of getting LED one partially or fully ready for the next update
    to the strip. An optimized version of the driver could omit the "clockStartFrame" method if enough zeroes have 
    been sent as part of "clockEndFrame".
    """
    def clockEndFrame(self):
        for _ in range((self.numLEDs + 15) // 16):  # Round up numLEDs/2 bits (or numLEDs/16 bytes)
            self.spi.xfer2([0x00])

    """
    Sets the color for the entire strip to black, and immediately shows the result.
    """
    def clearStrip(self):
        self.spi.xfer2([self.ledstart, 0x00, 0x00, 0x00] * self.numLEDs)
        self.clockEndFrame() # ... and clock the end frame so that also the last LED(s) shut down.

    """
    Sets the color of one pixel in the LED stripe. The changed pixel is not shown yet on the Stripe, it is only
    written to the pixel buffer. Colors are passed individually.
    """
    def setPixel(self, ledNum, red, green, blue):
        if ledNum < 0:
            return # Pixel is invisible, so ignore
        if ledNum >= self.numLEDs:
            return # again, invsible
        startIndex = 4 * ledNum
        self.leds[startIndex] = self.ledstart
        self.leds[startIndex+3] = red
        self.leds[startIndex+1] = green
        self.leds[startIndex+2] = blue
        
    """
    Sets the color of one pixel in the LED stripe. The changed pixel is not shown yet on the Stripe, it is only
    written to the pixel buffer. Colors are passed combined (3 bytes concatenated)
    """
    def setPixelRGB(self, ledNum, rgbColor):
        self.setPixel(ledNum, (rgbColor & 0xFF0000) >> 16, (rgbColor & 0x00FF00) >> 8, rgbColor & 0x0000FF)

    """
    Sends the content of the pixel buffer to the strip.
    Todo: More than 1024 LEDs requires more than one xfer operation.
    """
    def show(self):
        self.clockStartFrame()
        self.spi.xfer2(self.leds) # SPI takes up to 4096 Integers. So we are fine for up to 1024 LEDs. 
        self.clockEndFrame()

    """
    This method should be called at the end of a program in order to release the SPI device
    """
    def cleanup(self):
        self.spi.close()  # ... SPI Port schliessen
        
    """
     Make one 3*8 byte color value
    """
    def combineColor(self, red, green, blue):
        return (red << 16) + (green << 8) + blue

    """
    Get a color from a color wheel
    Green -> Red -> Blue -> Green
    """
    def wheel(self, wheelPos):
        if wheelPos < 85: # Green -> Red
            return self.combineColor(wheelPos * 3, 255 - wheelPos * 3, 0)
        elif wheelPos < 170: # Red -> Blue
            wheelPos -= 85
            return self.combineColor(255 - wheelPos * 3, 0, wheelPos * 3)
        else: # Blue -> Green
            wheelPos -= 170
            return self.combineColor(0, wheelPos * 3, 255 - wheelPos * 3);
