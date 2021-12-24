#!/usr/bin/env python3
"""Ultra simple sample on how to use the library"""
from apa102_pi.driver import apa102
import time


def main():
    # Initialize the library and the strip. This defaults to SPI bus 0, order 'rgb' and a very low brightness
    strip = apa102.APA102(num_led=430)

    # Turn off all pixels (sometimes a few light up when the strip gets power)
    strip.clear_strip()

    # Prepare a few individual pixels
    strip.set_pixel_rgb(12, 0xFF0000)  # Red
    strip.set_pixel_rgb(24, 0xFFFFFF)  # White
    strip.set_pixel_rgb(40, 0x00FF00)  # Green

    # Copy the buffer to the Strip (i.e. show the prepared pixels)
    strip.show()

    # Wait a few Seconds, to check the result
    time.sleep(20)

    # Clear the strip and shut down
    strip.clear_strip()
    strip.cleanup()


if __name__ == '__main__':
    main()
