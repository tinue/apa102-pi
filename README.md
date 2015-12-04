# APA102_Pi

## Introduction
APA102_Pi is a pure python library to drive APA102 type LED strands. It is supposed to work on a Raspberry Pi, and is not tested on any other platform.

APA102 LEDs are typically 5050 type LEDs with an additional driver chip per LED. The driver chip takes care of receiving the desired colour via its input lines, and then holding this colour until a new command is received.

Depending on where these LEDs are bought, they might be called "APA102", "Superled", or "DotStar". They should not be confused with the three-wire WS2812 LEDs, also known as "NeoPixel".

The really nice part about the driver chip is this: Once it has received its own colour command, it forwards any further colour commands from its input to its output lines. This allows to easily chain multiple LEDs together. Colour command #1 lights the first LED, command #2 the next LED, etc. Sending e.g. 300 colour commands lights an entire 5 Meter, 60 LEDs per Meter strip.

## Purpose
The library is designed to take care of the details about sending colour commands. It is supposed to be educational, and is therefore written in Python. The library is fast enough to produce nice colour effects on a 300 LED strand, even though it is running via the Python interpreter. However, if you need something really fast, e.g. to drive a small "display" based on APA102 LEDs with 15 frames per second, then you have to look elsewhere.

## Prerequisites
* A Raspberry Pi, running an up-to-date version of Raspbian (the library is tested with the 2015-11-21 version of Raspbian Jessie).
* SPI enabled and active (raspi-config, Advanced Options, SPI, Enable and load the module by default)
* The SPI must be free and unused
* A library named "spidev", Version 3. I used the one from here: https://github.com/doceme/py-spidev

Ideally, a 5$ Raspberry Pi Zero is dedicated to the task of driving the LEDs. The connector to the LED stripe can be soldered directly to the correct ports on the board.

## Wiring

The Raspberry Pi is a 3.3 Volt device, and the APA102 LEDs are 5 Volt devices. Therefore it's possible that the 3.3 Volt SPI signal is not being recognized by the LED driver chips. To avoid this risk, use a 74AHCT125 level shifter for both the clock and the MOSI signal.

Without a level shifter, the wiring is very simple:
- LED ground to one of the Raspberry ground pins
- LED Data to Raspberry SPI MOSI
- LED Clock to Raspberry SPI SCLK

The LED stripe uses a lot of power. If you try to power the LEDs from the Raspberry Pi, you will most likely immediately kill the Raspberry! Therefore I recommend not to connect the power line of the LED with the Raspberry. To be on the safe side, use a separate USB power supply for the Raspberry, and a strong 5V supply for the LEDs. If you use a level shifter, power it from the 5V power supply as well.

Having said this, you *can* power the Raspberry from the same power supply as the LED stripes (instead of using an extra USB power supply). If you decide to do this, make sure to never power the Raspberry Pi from its USB power supply, or you risk that the LEDs try to take power from the Raspberry.

All combined, this is my extremely low-tech wiring diagram:

![Wiring Diagram](Wiring.jpg)

And here it is, the finished contraption running a "rainbow" program:

![Raspberry Pi Zero driving APA102 LEDs](Finished.jpg)

Plugged into the USB port is a WLAN stick. This way I can reprogram the light show from my desk, even if the strips are installed outside as a christmas light. Compare this to an Arduino/WS2812 based installation: To reprogram one has to take the Arduino inside, or a laptop outside.

## Using the library
TODO