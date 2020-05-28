#!/usr/bin/env python3
"""Sample script to run a few colour tests on the strip."""
from apa102_pi.colorschemes import colorschemes

NUM_LED = 576

# One Cycle with one step and a pause of three seconds. Hence three seconds of white light
print('Three Seconds of white light')
MY_CYCLE = colorschemes.Solid(num_led=NUM_LED, pause_value=3,
                              num_steps_per_cycle=1, num_cycles=1, order='rgb')
MY_CYCLE.start()

# Go twice around the clock
print('Go twice around the clock')
MY_CYCLE = colorschemes.RoundAndRound(num_led=NUM_LED, pause_value=0,
                                      num_steps_per_cycle=NUM_LED, num_cycles=2, order='rgb')
MY_CYCLE.start()

# One cycle of red, green and blue each
print('One strandtest of red, green and blue each')
MY_CYCLE = colorschemes.StrandTest(num_led=NUM_LED, pause_value=0,
                                   num_steps_per_cycle=NUM_LED, num_cycles=3, order='rgb')
MY_CYCLE.start()

# One slow trip through the rainbow
print('One slow trip through the rainbow')
MY_CYCLE = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0,
                                num_steps_per_cycle=255, num_cycles=1, order='rgb')
MY_CYCLE.start()

# Five quick trips through the rainbow
print('Five quick trips through the rainbow')
MY_CYCLE = colorschemes.TheaterChase(num_led=NUM_LED, pause_value=0.04,
                                     num_steps_per_cycle=35, num_cycles=5, order='rgb')
MY_CYCLE.start()

print('Finished the test')
