"""Very rudimentary test class, might get extended in the future"""
from unittest import TestCase

import apa102


class TestAPA102(TestCase):
    # Check num_led
    def test_check_init(self):
        with self.assertRaises(ValueError):
            apa102.APA102(num_led=-1)
        with self.assertRaises(ValueError):
            apa102.APA102(num_led=0)
        with self.assertRaises(ValueError):
            apa102.APA102(num_led=1025)
        try:
            apa102.APA102(num_led=1)
        except ValueError:
            self.fail("num_led 1 should be valid")
        try:
            apa102.APA102(num_led=1024)
        except ValueError:
            self.fail("num_led 1024 should be valid")
        # Check bus_method
        with self.assertRaises(ValueError):
            apa102.APA102(bus_method='invalid')
        try:
            apa102.APA102(bus_method='spi')
        except ValueError:
            self.fail("spi should be valid")
        try:
            apa102.APA102(bus_method='bitbang', mosi=12, sclk=25)
        except ValueError:
            self.fail("bitbang should be valid")
        # Check spi-bus
        with self.assertRaises(ValueError):
            apa102.APA102(bus_method='spi', spi_bus=9)
        try:
            apa102.APA102(bus_method='spi', spi_bus=0)
        except ValueError:
            self.fail("bus 0 should exist")
        # Check bitbang
        with self.assertRaises(ValueError):
            apa102.APA102(bus_method='bitbang')
        with self.assertRaises(ValueError):
            apa102.APA102(bus_method='bitbang', mosi=25, sclk=25)
