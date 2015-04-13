import apa102

"""
Now for the actual rainbow cycle algorithm
"""
try:
    numPixels = 432-73 # 1/2 Strip plus one LED is broken
    strip = apa102.APA102(numPixels, 2) # Low brightness (2 out of max. 31)
    while True:  # Loop forever
        for j in range(numPixels<<8): # Shift the start of the rainbow across the strip
            for i in range(numPixels): # spread (or compress) one rainbow onto the strip
                # For a faster shift, add more than 1 * j per loop (e.g. + 2 * j)
                index = strip.wheel((((i << 8) // numPixels) + j*4) & 255)
                strip.setPixelRGB(i, index);
            strip.show()    

except KeyboardInterrupt:  # Abbruch...
    print('Interrupted...')
    strip.clearStrip()
    print('Strip cleared')
    strip.cleanup()
    print('SPI closed')
