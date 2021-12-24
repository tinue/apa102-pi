#!/usr/bin/env python3
"""Sample script to run a few colour tests on a Pi Hut '3D RGB Xmas Tree for Raspberry Pi'."""
from apa102_pi.colorschemes import colorschemes

NUM_LED = 25
BRIGHTNESS = 10  # My Pi 4 managed full brightness of 31 (1.25A current draw); Increase the value at your own risk!
MOSI = 12  # We need bitbang mode, and have to specify the GPIO pins used
SCLK = 25


def main():
    # Paint white, red, green and blue once for one second
    print('White, red, green, blue on all LEDs')
    my_cycle = colorschemes.Solid(num_led=NUM_LED, pause_value=1, order='rgb',
                                  num_steps_per_cycle=4, num_cycles=1, bus_method='bitbang', mosi=MOSI, sclk=SCLK,
                                  global_brightness=BRIGHTNESS)
    my_cycle.start()

    # Five trips through the rainbow
    print('Five trips through the rainbow')
    my_cycle = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0, order='rgb',
                                    num_steps_per_cycle=100, num_cycles=10, bus_method='bitbang', mosi=MOSI, sclk=SCLK,
                                    global_brightness=BRIGHTNESS)
    my_cycle.start()

    print('Finished the test')


if __name__ == '__main__':
    main()
