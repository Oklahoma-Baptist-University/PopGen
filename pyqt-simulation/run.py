from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys
import window as win
import creatures as c
import terrain as t

# Run
if __name__ == '__main__':
    app = QApplication([])

    maxWorldAge = 20000000
    maxX = 800
    maxY = 600
    width = maxX + 20
    height = maxY + 20

    numReds = 5
    numBlues = 50
    maxCreatureAge = 2
    worldSpeed = 25
    geneTransferSpeed = 50

    window = win.Window(maxWorldAge, maxX, maxY, width, height, worldSpeed)
    theWorld = window.world
    theWorld.addTerrain(t.Water(20, 20, 100))
    theWorld.addTerrain(t.Water(100, 200, 300))
    theWorld.addTerrain(t.Mountains(450, 30, 200))

    for i in range(numReds):
        newDot = c.RedDot(maxCreatureAge, 10, geneTransferSpeed)
        x = random.randrange(theWorld.maxX)
        y = random.randrange(theWorld.maxY)
        while not theWorld.emptyLocation(x, y):
            x = random.randrange(theWorld.maxX)
            y = random.randrange(theWorld.maxY)
        theWorld.addThing(newDot, x, y)

    for i in range(numBlues):
        newDot = c.BlueDot(maxCreatureAge, 10, geneTransferSpeed)
        x = random.randrange(theWorld.maxX)
        y = random.randrange(theWorld.maxY)
        while not theWorld.emptyLocation(x, y):
            x = random.randrange(theWorld.maxX)
            y = random.randrange(theWorld.maxY)
        theWorld.addThing(newDot, x, y)

    #theWorld.visualizeTerrain()
    
    sys.exit(app.exec_())

theWorld.visualizeTerrain()
print(theWorld.grid)
print(theWorld.thingList)