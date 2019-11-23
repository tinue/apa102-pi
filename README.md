# apa102-pi

## Updating
If you are currently using this library, you will have to update your `import` statements and add the 
previously missing package name. For example:
* Old: `from driver import apa102`
* New: `from apa102_pi.driver import apa102`

## Introduction
Apa102-pi is a pure Python library to drive APA102 type LED strands. It is supposed to work on a Raspberry Pi,
and is not tested on any other platform.

APA102 LEDs are typically 5050 type LEDs with an additional driver chip per LED.
The driver chip takes care of receiving the desired colour via its input lines, and then holding
this colour until a new command is received.

Depending on where these LEDs are bought, they might be called "APA102", "Superled", or "DotStar".
They should not be confused with the three-wire WS2812 LEDs, also known as "NeoPixel".

The really nice part about the driver chip is this: Once it has received its own colour command,
it forwards any further colour commands from its input to its output lines.
This allows to easily chain multiple LEDs together. Colour command #1 lights the first LED,
command #2 the next LED, and so forth. Sending for example 300 colour commands does light
an entire 5 Meter, 60 LEDs per Meter strip.

Some APA102 pictures are available [here](https://www.iot-projekte.ch/apa102-led-part-1-pictures)

## Purpose
The library is designed to take care of the details about sending colour commands.
It is supposed to be educational, and is therefore written in Python.
The library is fast enough to produce nice colour effects on a 300 LED strand, even though it is running
via the Python interpreter. However, if you need something really fast, e.g. to drive a
small "display" based on APA102 LEDs with 15 frames per second, then you have to look elsewhere.

## Prerequisites
* A Raspberry Pi, running an up-to-date version of Raspbian (the library is tested with the 2019-09-26
version of Raspbian Buster Lite).
* If hardware SPI is used: SPI enabled and active (`raspi-config`, Interfacing Options, SPI, \<Yes\>);
The SPI must be free and unused.
* For software SPI (bit bang mode): Two free GPIO pins
* The Adafruit_Python_GPIO library (https://github.com/adafruit/Adafruit_Python_GPIO).
The library will be installed automatically if you follow the instructions below.  
* Python 3: Some people tried with Python 2 and reported it working, but I can't vouch for this myself.
I used Python 3 for all development and test. 

For a permanent installation, a 10$ Raspberry Pi Zero W can be dedicated to the task of driving the LEDs.
The connector to the LED stripe would be soldered directly to the correct ports on the board.
For development purposes, a Raspberry Pi 4 Model B is a better choice due to its greater speed.
Even the 1GB model is more than enough.

## Wiring
The Raspberry Pi is a 3.3 Volt device, and the APA102 LEDs are 5 Volt devices. 
Therefore it's possible that the 3.3 Volt SPI signal is not properly recognized by the LED driver chips.
To avoid this risk, use a 74AHCT125 or 74AHC125 level shifter for both the clock and the MOSI signal.
You will not damage the Raspberry Pi without a level shifter, because the Raspberry Pi determines
the voltage of MOSI and SCLK.  
In my limited testing with four different stripes from various Chinese sources I had no issues without
a level shifter, but your experience might be different.

Without a level shifter, the wiring is very simple:

- LED ground to one of the Raspberry ground pins  
- LED Data to Raspberry SPI MOSI  
- LED Clock to Raspberry SPI SCLK

Note that the "Chip Select" line (CE0 or CE1) is not used on an APA102 strip.
The APA102 chip always accepts data, and cannot be switched off.
For "Chip Select" to work, you need additional hardware. If you use a level shifter,
you can wire CE0 or CE1 to its "output-enable" pin, for example.

The LED strip uses a lot of power (roughly 20mA per LED, i.e. 60mA for one bright white dot).
If you try to power the LEDs from the Raspberry Pi 5V output, you will most likely immediately
kill the Raspberry! Therefore I recommend not to connect the power line of the LED with the Raspberry. 
To be on the safe side, use a separate USB power supply for the Raspberry, and a strong 5V supply 
for the LEDs. If you use a level shifter, power it from the 5V power supply as well.

Having said this, you *can* power the Raspberry from the same power supply as the LED stripes
(instead of using an extra USB power supply). If you decide to do this, make sure to never plug
a USB power supply to the Raspberry Pi, or you risk that the LEDs try to take power through the Raspberry.

All combined, this is my extremely low-tech wiring diagram:

![Wiring Diagram](Wiring.jpg)

And here it is, the finished contraption running a "rainbow" program:

![Raspberry Pi Zero driving APA102 LEDs](Finished.jpg)

This is a Raspberry Pi Zero W with a Phat Beat amplifier on top. The amplifier's "VU meter" is simply
a bunch of APA 102 LEDs; They show the "Rainbow" color scheme:

![Raspberry Pi Zero W with Phat Beat](PhatBeat.jpg)

Plugged into the USB port is a WLAN stick (nowadays I use a Raspberry Pi Zero W, of course).
This way I can reprogram the light show from my desk, even if the strips are installed outside 
as a Christmas light. Compare this to an Arduino/WS2812 based installation: To reprogram one has
to take the Arduino inside, or a laptop outside.

## Quick Raspberry Pi setup
Because the Raspberry Pi Zero runs headless, the Raspbian Lite image was used.
This image only contains the bare minimum of packages, and some packages have be added manually.

The current Raspbian Lite images can easily be set-up to run headless from the start.
After burning the card on a Mac or PC, it will be mounted as "boot". Go to this directory,
and create an empty file named `ssh` to enable SSH.  
On a Mac you would do this: `touch /Volumes/boot/ssh`. To enable and configure WLAN, create
a file named `wpa_supplicant.conf`. Its content should be:  

	country=CH
	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1
	
	network={
		ssid="Your_SSID"
		psk="Your_Password"
		key_mgmt=WPA-PSK
	}

Of course, use the correct country and ssid/psk. After booting (be patient: The Pi will initially boot twice)
you can SSH into the Raspberry Pi: `ssh pi@raspberrypi.local`. The initial password
is `raspberry`: Make sure to change it right away!

Next, install additional packages and enable SPI:

- Update your installation (`sudo apt update && sudo apt -y upgrade`).
- Install packages: `sudo apt install -y python3-pip`
- Activate SPI: `sudo raspi-config`; Go to "Interfacing Options"; Go to "SPI"; Enable SPI;
While you are at it: Do change the default password! Exit exit the tool and reboot  

## Use the APA102 project as a library
The library was originally built as an educational piece of software. It shows how the protocol
for APA102 LEDs works. Most of this is explained in the form of comments in the source code.
If you are interested in this, then follow up with the next chapter.
If all you need is the library itself for your own projects, then this chapter is enough to get you started.

Install the library like this: `sudo pip3 install apa102-pi`. 
This will install the library and it's dependencies for all users. 

To verify the installation, download the test script from Github:
`curl https://raw.githubusercontent.com/tinue/apa102-pi/master/runcolorcycle.py -o runcolorcycle.py`.
To run, type `python3 ./runcolorcycle.py`.
 
## Full installation
To retrieve the full library including source code, this is what you need to do *additionally*:
- Install the git client: `sudo apt install -y git`  
- Prepare GIT: `git config --global user.name "John Doe" && git config --global user.email johndoe@example.com`  
- Create a development directory and change into it: `mkdir ~/Development && cd ~/Development`  
- Get the APA102 Library and sample light programs: `git clone https://github.com/tinue/apa102-pi.git && cd apa102-pi`  
- You might want to set the number of LEDs to match your strip: `nano runcolorcycle.py`; Update the number, Ctrl-X and "Yes" to save.  
- Run the sample lightshow: `./runcolorcycle.py`.
- Optional: Remove the previously installed central version of the library (but keep the necessary dependencies): `sudo pip3 uninstall apa102-pi`

## Troubleshooting
### Flicker
Some users reported flicker towards the end of large stripes. It seems that there is a correlation amongst
three variables:
* SPI bus speed
* Overall brightness of the strip
* Length of the strip

It turns out that you can only have two out of three: On a long, bright strip you will have to lower the bus speed significantly.
Check the apa102.py driver: Default is 8MHz (`BUS_SPEED_HZ = 8000000`). You may have to go as low as 1.5MHz, 
i.e. `BUS_SPEED_HZ = 1500000`. This means that all light programs with lots of updates and zero wait
(e.g. rainbow) will run much slower.

## Release history
- 1.0.0 (2015-04-13): Initial version
- 1.1.0 (2015-12-04): Add documentation
- 1.1.1 (2015-12-11): Rewrote the examples, driver itself is unchanged
- 1.2.0 (2015-12-17): Fixes for reported problems; Update all of the color samples; Decouple number of steps from number of LEDs
- 1.3.0 (2016-03-25): Merged changes from kapacuk: Allow stripes with different color coding than RGB
- 1.3.1 (2016-03-27): Merged 'rotate' method from kapacuk; Fixed errors from previous merge
- 1.3.2 (2016-12-25): Fixed error related to 'rotate'; Removed annoying messages on console; Added a debug method
- 1.3.3 (2017-04-14): Merged pull request #19 from DurandA/master; Cleanup; Update README.MD, No functional changes
- 1.4.0 (2017-04-16): Update code to better comply with the Python style guide (PEP 8); Merged pull request from 'jmb'
- 1.4.1 (2017-08-26): Tested with Raspbian Stretch; Update Readme.
- 2.0.0 (2017-11-05): Exchanged the SPI library to Adafruit_Python_GPIO. This allows to support devices that do not use hardware SPI, for example the Pimoroni Blinkt! or the Phat Beat.
- 2.0.1 (2018-01-19): Tiny release: Added a sample
- 2.0.2 (2018-05-25): No change in the driver; Slight restructuring of the templates and schemes to allow easier change of the SPI pins; Additional sample specific to the the Pimoroni Blinkt!
- 2.1.0 (2018-06-08): Make the library installable
- 2.1.1 (2019-03-15): Enable Chip Select (thanks @grandinquisitor); Simplify installation (thanks @nielstron)
- 2.2.0 (2019-03-16): First version that is available on PyPi (pip 3 install); Renamed package for compliancy with PEP 8.
- 2.2.1 (2019-09-20): Nothing new, just a re-test of the library with Raspbian Buster
- 2.3.0 (2019-11-23): Untested fix for SK9822 type LEDs; Fix name space; Update readme. Note: The namespace fix
                      breaks compatibility with the previous version, hence the minor upgrade in the version number.