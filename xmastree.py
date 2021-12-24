#!/usr/bin/env python3
"""Ultra simple sample on how to use the library. Light up the xmas tree in red"""
from apa102_pi.driver import apa102
import time


def main():
    # Initialize the library and the strip. The xmas tree needs bitbang. Default order 'rgb' is fine.
    strip = apa102.APA102(num_led=25, bus_method='bitbang', mosi=12, sclk=25, global_brightness=31)

    # Clear the buffer
    strip.clear_strip()

    # Loop over all pixels snd set them to red
    for i in range(25):
        strip.set_pixel_rgb(i, 0xFF0000)  # Red

    # Show the buffer, sleep 20 seconds
    strip.show()
    time.sleep(20)

    # Clear the strip and shut down
    strip.clear_strip()
    strip.cleanup()

if __name__ == '__main__':
    main()
