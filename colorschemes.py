from colorcycletemplate import ColorCycleTemplate

class StrandTest(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        self.color = 0x000000  # Initialize with black

    def update(self, strip, numLEDs, currentStep, currentCycle):
        if (currentStep == 0): self.color >>= 8  # Red->green->blue->black
        if (self.color == 0): self.color = 0xFF0000  # If black, reset to red

        head = (currentStep + 9) % numLEDs # The head pixel that will be turned on in this cycle
        tail = currentStep # The tail pixel that will be turned off
        strip.setPixelRGB(head, self.color)  # Paint head
        strip.setPixelRGB(tail, 0)  # Clear tail

        return 1 # Repaint is necessary


class TheaterChase(ColorCycleTemplate):
    def update(self, strip, numLEDs, currentStep, currentCycle):
        startIndex = currentStep % 7 # Each segment is 7 dots long: 2 blank, and 5 filled
        colorIndex = strip.wheel((currentCycle*numLEDs+currentStep) % 255)
        for pixel in range(numLEDs):
        	  # Two LEDs out of 7 are blank. At each step, the blank ones move one pixel ahead.
            if ((pixel+startIndex) % 7 == 0) or ((pixel+startIndex) % 7 == 1): strip.setPixelRGB(pixel, 0)
            else: strip.setPixelRGB(pixel, colorIndex)
        return 1



class Solid(ColorCycleTemplate):

    def init(self, strip, numLEDs):
    	  for led in range(0, numLEDs):
    	  	  strip.setPixelRGB(led,0xFFFFFF) # Paint white

    def update(self, strip, numLEDs, currentStep, currentCycle):
    	  # Do nothing: Init lit the strip, and update just keeps it this way
    	  return 0


class Rainbow(ColorCycleTemplate):
    def update(self, strip, numLEDs, currentStep, currentCycle):
        shiftCounter = currentCycle * numLEDs + currentStep
        for i in range(numLEDs): # spread (or compress) one rainbow onto the strip
            # For a faster shift, add more than 1 * j per loop (e.g. + 2 * j)
            index = strip.wheel((((i << 8) // numLEDs) + shiftCounter) & 255)
            strip.setPixelRGB(i, index);
        return 1 # Repaint the strip