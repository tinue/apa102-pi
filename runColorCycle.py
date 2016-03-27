import colorschemes

numLEDs = 430

# One Cycle with one step and a pause of one second. Hence one second of white light
myCycle = colorschemes.Solid(numLEDs=numLEDs, pauseValue=1, numStepsPerCycle = 1, numCycles = 1)
myCycle.start()
# Go twice around the clock
myCycle = colorschemes.RoundAndRound(numLEDs=numLEDs, pauseValue=0, numStepsPerCycle = numLEDs, numCycles = 2)
myCycle.start()
# One cycle of red, green and blue each
myCycle = colorschemes.StrandTest(numLEDs=numLEDs, pauseValue=0, numStepsPerCycle = numLEDs, numCycles = 3, globalBrightness=10)
myCycle.start()
# Two slow trips through the rainbow
myCycle = colorschemes.Rainbow(numLEDs=numLEDs, pauseValue=0, numStepsPerCycle = 255, numCycles = 2, globalBrightness=10)
myCycle.start()
# Five quick trips through the rainbow
myCycle = colorschemes.TheaterChase(numLEDs=numLEDs, pauseValue=0.04, numStepsPerCycle = 35, numCycles = 5, globalBrightness=10)
myCycle.start()