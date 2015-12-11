import apa102
import time

"""
This class is the basis of all color cycles, such as rainbow or theater chase.
"""

class BaseColorCycle:
    def __init__(self, numLEDs, pauseValue = 0, globalBrightness = 31): # Init method
        self.numLEDs = numLEDs
        self.pauseValuse = pauseValue
        self.globalBrightness = globalBrightness
        timeOfLastCall = 0
        cycleCounter = 0

    """
    void init()
    This method is called to initialize a color program.
    """
    def init(self):
    	  # The default does nothing. A particular subclass could e.g. light all LEDs to white.
    	  print('Init')

    """
    void shutdown()
    This method is called at the end, when the light program shoule terminate
    """
    def shutdown(self):
        # The default does nothing
        print('Shutdown')

    """
    void update()
    This method paints one cycle. It must be implemented
    """
    def update(self):
    	  raise NotImplementedError("Please implement the update() method")

    """
    Start the actual work
    """

    try:
        strip = apa102.APA102(numPixels, globalBrightness) # Low brightness (2 out of max. 31)
        while True:  # Loop forever
            cycleCounter += 1
            update()
            strip.show()
            time.sleep(pauseValue)

    except KeyboardInterrupt:  # Abbruch...
        print('Interrupted...')
        strip.clearStrip()
        print('Strip cleared')
        strip.cleanup()
        print('SPI closed')