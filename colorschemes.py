from colorcycletemplate import ColorCycleTemplate

class StrandTest(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        self.color = 0x000000  # Initialize with black

    def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
        # One cycle = The 9 Test-LEDs wander through numStepsPerCycle LEDs.
        if (currentStep == 0): self.color >>= 8  # Red->green->blue->black
        if (self.color == 0): self.color = 0xFF0000  # If black, reset to red

        head = (currentStep + 9) % numStepsPerCycle # The head pixel that will be turned on in this cycle
        tail = currentStep # The tail pixel that will be turned off
        strip.setPixelRGB(head, self.color)  # Paint head
        strip.setPixelRGB(tail, 0)  # Clear tail

        return 1 # Repaint is necessary


class TheaterChase(ColorCycleTemplate):
    def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
        # One cycle = One thrip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # Note: For a smooth transition between cycles, numStepsPerCycle must be a multiple of 7
        startIndex = currentStep % 7 # Each segment is 7 dots long: 2 blank, and 5 filled
        colorIndex = strip.wheel(int(round(255/numStepsPerCycle * currentStep, 0)))
        for pixel in range(numLEDs):
        	  # Two LEDs out of 7 are blank. At each step, the blank ones move one pixel ahead.
            if ((pixel+startIndex) % 7 == 0) or ((pixel+startIndex) % 7 == 1): strip.setPixelRGB(pixel, 0)
            else: strip.setPixelRGB(pixel, colorIndex)
        return 1


class RoundAndRound(ColorCycleTemplate):

    def init(self, strip, numLEDs):
        strip.setPixelRGB(0, 0xFF0000);
        strip.setPixelRGB(1, 0x00FF00);

    def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
        # Simple class to demonstrate the "rotate" method
        strip.rotate()
        return 1


class Solid(ColorCycleTemplate):

    def init(self, strip, numLEDs):
    	  for led in range(0, numLEDs):
    	  	  strip.setPixelRGB(led,0xFFFFFF) # Paint white

    def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
    	  # Do nothing: Init lit the strip, and update just keeps it this way
    	  return 0


class Rainbow(ColorCycleTemplate):
    def update(self, strip, numLEDs, numStepsPerCycle, currentStep, currentCycle):
        # One cycle = One thrip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # -> LED 0 goes from index 0 to 254 in numStepsPerCycle cycles. So it might have to step up
        #     more or less than one index depending on numStepsPerCycle.
        # -> The other LEDs go up to 254, then wrap arount to zero and go up again until the last one is just
        #     below LED 0. This way, the strip always shows one full rainbow, regardless of the number of LEDs
        scaleFactor = 255 / numLEDs # Value for the index change between two neighboring LEDs
        startIndex = 255 / numStepsPerCycle * currentStep # Value of LED 0
        for i in range(numLEDs):
            ledIndex = startIndex + i * scaleFactor # Index of LED i, not rounded and not wrapped at 255
            ledIndexRoundedAndWrappedAround = int(round(ledIndex, 0)) % 255 # Now rounded and wrapped
            pixelColor = strip.wheel(ledIndexRoundedAndWrappedAround) # Get the actual color out of the wheel
            strip.setPixelRGB(i, pixelColor);
        return 1 # All pixels are set in the buffer, so repaint the strip now