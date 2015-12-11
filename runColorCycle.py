import colorschemes

myCycle = colorschemes.Solid(numLEDs=430, pauseValue=0.01, numCycles = 1)
myCycle.start()
myCycle = colorschemes.StrandTest(numLEDs=430, pauseValue=0, numCycles = 4, globalBrightness=10)
myCycle.start()
myCycle = colorschemes.Rainbow(numLEDs=430, pauseValue=0, numCycles = 6, globalBrightness=10)
myCycle.start()
myCycle = colorschemes.TheaterChase(numLEDs=430, pauseValue=0.04, numCycles = 2, globalBrightness=10)
myCycle.start()