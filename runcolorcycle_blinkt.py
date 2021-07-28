#!/usr/bin/env python3
"""Sample script to run a few colour tests on a Pimoroni Blinkt!."""
from apa102_pi.colorschemes import colorschemes

NUM_LED = 8
MOSI = 23  # Hardware SPI uses BCM 10 & 11. Change these values for bit bang mode
SCLK = 24  # e.g. MOSI = 23, SCLK = 24 for Pimoroni Phat Beat or Blinkt!


def main():
    # Paint white, red, green and blue once for one second
    print('White, red, green, blue on all LEDs')
    my_cycle = colorschemes.Solid(num_led=NUM_LED, pause_value=1, order='rgb',
                                  num_steps_per_cycle=4, num_cycles=1, mosi=MOSI, sclk=SCLK)
    my_cycle.start()

    # Five trips through the rainbow
    print('Five trips through the rainbow')
    my_cycle = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0, order='rgb',
                                    num_steps_per_cycle=255, num_cycles=5, mosi=MOSI, sclk=SCLK)
    my_cycle.start()

    print('Finished the test')


if __name__ == '__main__':
    main()
