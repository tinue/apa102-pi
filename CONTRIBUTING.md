# Contributing to apa102-pi

* Feel free to answer any questions that pop up as issues or in discussions.
* To contribute code, please make a pull request against the "develop" branch. I will review and merge the code, and release it on "main" whenever I do the next release. I will also update the release history in README.md.

## Ideas
Possible contributions:
* Test multiple strips using different chip select pins
* Simplify SPI handling, see below

## On SPI handling
All that the library needs to do with SPI is write data as quickly as possible. For this, it needs to open the SPI bus, change the bus speed, and then write the data.  
To make matters slightly more complicated is the fact that some APA102 LEDs (notably the Pimoroni Blinkt!) do not use any of the physical SPI buses of the Raspberry Pi. Instead, they use two of the general purpose IO pins for MOSI and SCLK. The SPI protocol must therefore be implemented in software, which is also known as "bitbang" mode.  
The Adafruit library that is used by the driver does all this nicely, and it does many more things that is not required by the driver. I believe therefore that this library is a bit of an overkill for the simple purposes that are required.

For hardware SPI, the [spidev](https://pypi.org/project/spidev) library is all that we would need. This library was used initially (before bitbang support), and it fits perfectly.

In order to go back to this library, bitbang would have to be implemented. It's not super difficult, I believe: Send bit by bit over MOSI, and toggle SCLK after every bit high/low. MISO can be ignored altogether (data is only sent, not received), and Chip Select can initially also be ignored.

So, if anyone wants to give this a go, then please try!

Once this works, some clever boilerplate needs to be added to select hardware or software SPI, and to select the proper hardware bus.