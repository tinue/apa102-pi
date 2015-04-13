# APA102_Pi
Pure Python library to drive APA102 LED stripes; Use with Raspberry Pi.

Prerequisite: spidev v3. I used the one from here: https://github.com/doceme/py-spidev

The LED stripe is attached to the Raspberry Pi like this:
- Gnd to a Gnd pin, e.g. the one right next to the SPI pins
- Data to SPI MOSI
- Clock to SPI SCLK
- Do *not* connect the LED stripe power to the Raspberry Pi: You will kill it right away.

Instead, use a separate 5V power supply to power the stripe. All of the grounds must be shared.
