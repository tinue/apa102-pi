#!/usr/bin/env python3
"""Sample script to run a few colour tests on a christmas tree."""
from apa102_pi.colorschemes import colorschemes

NUM_LED = 25
MOSI =12  # Tree uses 12
SCLK = 25  # Tree uses 25


def main():
    # Paint white, red, green and blue once for one second
    print('White, red, green, blue on all LEDs')
    my_cycle = colorschemes.Solid(num_led=NUM_LED, pause_value=1, order='rgb',
                                  num_steps_per_cycle=4, num_cycles=1, bus_method='bitbang', mosi=MOSI, sclk=SCLK)
    my_cycle.start()

    # Five trips through the rainbow
    print('Five trips through the rainbow')
    my_cycle = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0, order='rgb',
                                    num_steps_per_cycle=255, num_cycles=5, bus_method='bitbang', mosi=MOSI, sclk=SCLK)
    my_cycle.start()

    print('Finished the test')


if __name__ == '__main__':
    main()
