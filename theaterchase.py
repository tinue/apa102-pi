import apa102

"""
Chase a segment of LEDs round the strip
"""
try:
    numPixels = 432-73 # 1/2 Strip plus one LED is broken
    strip = apa102.APA102(numPixels, 2) # Low brightness (2 out of max. 31)
    while True:  # Loop forever
        for j in range(256): # Change the color through the color wheel
            for q in range(7):
                # For smooth entry and exit, the loop must start and end with hidden pixels
                # This way, the pixels "roll in" and "slide out" of the strip
                for i in range(-5, numPixels, 7): # Each segment is 7 LEDs long
                    index = strip.wheel( (i + j) % 255)
                    strip.setPixelRGB(i+q, 0);
                    strip.setPixelRGB(i+q+1, 0);
                    strip.setPixelRGB(i+q+2, index);
                    strip.setPixelRGB(i+q+3, index);
                    strip.setPixelRGB(i+q+4, index);
                    strip.setPixelRGB(i+q+5, index);
                    strip.setPixelRGB(i+q+6, index); # Wrap, if we are at the end of the strip
                strip.show()    

except KeyboardInterrupt:  # Abbruch...
    print('Interrupted...')
    strip.clearStrip()
    print('Strip cleared')
    strip.cleanup()
    print('SPI closed')
