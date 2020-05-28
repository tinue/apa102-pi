# Things to do after switching to Adafruit_Blinka
* Enable Bitbang. See ![Issue 292](https://github.com/adafruit/Adafruit_Blinka/issues/292).
* Enable Chip Select
* Test SPI1
* Change the colour templates so that the strip is passed instead of created. This way, multiple strips could run in parallel.

# Packaging
The upcoming v2.4.0 pypi package will include the proper dependencies. For now, they must be installed manually:
* sudo pip3 install adafruit-circuitpython-busdevice
* sudo pip3 install adafruit-circuitpython-bitbangio