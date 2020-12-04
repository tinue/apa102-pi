#!/usr/bin/env python3
"""Ultra simple sample on how to use the library"""
from apa102_pi.driver import apa102
import time

# Initialize the library and the strip
strip = apa102.APA102(num_led=430, mosi=10, sclk=11, order='rbg')

# Increase the brightness to 100% (from the default of 12.5%)
strip.set_global_brightness(31)
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
