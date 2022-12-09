from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import random
import sys

class Window(QMainWindow):
    def __init__(self, maxWorldAge, maxX, maxY, w, h, worldSpeed):
        super(Window, self).__init__()

        self.world = World(maxWorldAge, maxX, maxY, worldSpeed)
  
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("border : 2px solid black;")
  
        # calling showMessage method when signal received by World
        self.world.msg2statusbar[str].connect(self.statusbar.showMessage)
  
        self.setCentralWidget(self.world)
  
        self.setWindowTitle('Simulation')
  
        self.setGeometry(maxX, maxY, w, h)
        self.setFixedSize(w, h)
  
        self.world.start()
  
        self.show()

class World(QFrame):

    msg2statusbar = pyqtSignal(str)

    def __init__(self, maxWorldAge, maxX, maxY, worldSpeed):
        super(World, self).__init__()
    
        self.timer = QBasicTimer()
        self.setStyleSheet("background-image: url('PopGen/pyqt-simulation/background.png')")
        self.setFocusPolicy(Qt.StrongFocus)

        self.maxX = maxX
        self.maxY = maxY
        self.grid = []
        self.terrainGrid = [] # Unused right now.
        self.thingList = []
        self.worldSpeed = worldSpeed # Milliseconds per frame.
        self.maxWorldAge = maxWorldAge
        self.worldAge = 0

        for aRow in range(self.maxY):
            row = []
            for aCol in range(self.maxX):
                row.append(None)
            self.grid.append(row)

        for aRow in range(self.maxY):
            row = []
            for aCol in range(self.maxX):
                row.append("L")
            self.terrainGrid.append(row)

        print("Size of grid:", len(self.grid))

    def start(self):
        # Starting message and the clock
        self.msg2statusbar.emit("Simulating.")
        self.timer.start(self.worldSpeed, self)

    def addThing(self, thing, x, y):
        if self.emptyLocation(x, y):
            thing.xPos = x
            thing.yPos = y
            thing.world = self
            thing.birthYear = self.worldAge
            self.grid[y][x] = thing
            self.thingList.append(thing)
            return thing
        else:
            print("Looks like there was something already there.")
    
    def delThing(self, thing):
        self.grid[thing.yPos][thing.xPos] = None
        self.thingList.remove(thing)

    def advanceTime(self):
        if self.worldAge > self.maxWorldAge:
            self.msg2statusbar.emit("Max world age reached.")
            print("Max world age reached.")
            self.timer.stop()
            self.update()
        elif self.thingList != []:
            random.shuffle(self.thingList)
            for thing in self.thingList:
                if thing.dead == True:
                    self.delThing(thing)
                else:
                    thing.liveALittle()
        else:
            self.msg2statusbar.emit("There is nothing left in the world...")
            print("There is nothing left in the world...")
            self.timer.stop()
            self.update()

    def drawThing(self, painter, thing):
        #image = QPixmap(thing.imagePath)
        #painter.drawPixmap(int(thing.xPos), int(thing.yPos), 15, 15, image)

        painter.setPen(QPen(thing.color, 5, Qt.SolidLine))
        painter.drawEllipse(int(thing.xPos), int(thing.yPos), 5, 5)

    # Draw everything for each frame.
    def paintEvent(self, event):
        painter = QPainter(self)
        for thing in self.thingList:
            self.drawThing(painter, thing)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.advanceTime()
            self.update()
            self.worldAge += 1
            #print("World age:", self.worldAge)

    def emptyLocation(self, x, y):
        try:
            if self.grid[y][x] == None:
                return True
            else:
                return False
        except IndexError:
            print("IndexError occured.")
            return False    

# Class for anything that moves around.
class MovingObject:
    def __init__(self, maxAge, speed):
        self.world = None
        self.dead = False
        self.birthYear = None
        self.age = 0
        self.maxAge = maxAge
        self.speed = speed
        self.xPos = None
        self.yPos = None
        self.offsetList = [(-speed, speed), (0, speed), (speed, speed),
                           (-speed, 0),                     (speed, 0),
                           (-speed, -speed), (0, -speed), (speed, -speed)]

    def tryToMove(self):
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextX = self.xPos + randomOffset[0]
        nextY = self.yPos + randomOffset[1]
        while not (0 <= nextX < self.world.maxX and \
                   0 <= nextY < self.world.maxY):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextX = self.xPos + randomOffset[0]
            nextY = self.yPos + randomOffset[1]

        if self.world.emptyLocation(nextX, nextY):
            self.xPos = nextX
            self.yPos = nextY

    def tryToBreed(self, thing):
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextX = self.xPos + randomOffset[0]
        nextY = self.yPos + randomOffset[1]
        while not (0 <= nextX < self.world.maxX and \
                   0 <= nextY < self.world.maxY):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextX = self.xPos + randomOffset[0]
            nextY = self.yPos + randomOffset[1]

        if self.world.emptyLocation(nextX, nextY):
            baby = self.world.addThing(thing, nextX, nextY)

# Red
class RedDot(MovingObject):
    def __init__(self, maxAge, speed):
        super().__init__(maxAge, speed)
        self.geneLvl = 255
        self.color = QColor(self.geneLvl, 0, 0)
        self.babies = 0

    def tryToBreed(self, baby):
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextX = self.xPos + randomOffset[0]
        nextY = self.yPos + randomOffset[1]
        while not (0 <= nextX < self.world.maxX and \
                   0 <= nextY < self.world.maxY):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextX = self.xPos + randomOffset[0]
            nextY = self.yPos + randomOffset[1]

        if self.world.emptyLocation(nextX, nextY):
            if self.geneLvl > 15:
                baby.geneLvl = self.geneLvl - 10
                baby.color = QColor(baby.geneLvl, 0, 0)
            else:
                baby.geneLvl = self.geneLvl
                baby.color = QColor(baby.geneLvl, 0, 0)
            self.world.addThing(baby, nextX, nextY)

    def liveALittle(self):
        if self.age <= self.maxAge:
            if self.age >= (self.maxAge/2) and self.babies < 2:
                baby = RedDot(self.maxAge, self.speed)
                self.tryToBreed(baby)
                self.babies += 1
            self.tryToMove()
            self.age += 1
        else:
            self.dead = True

# Blue
class BlueDot(MovingObject):
    def __init__(self, maxAge, speed):
        super().__init__(maxAge, speed)
        self.color = QColor(0, 0, 205)
        self.babies = 0

    def liveALittle(self):
        if self.age <= self.maxAge:
            if self.age >= (self.maxAge/2) and self.babies < 1:
                baby = BlueDot(self.maxAge, self.speed)
                self.tryToBreed(baby)
                self.babies += 1
            self.tryToMove()
            self.age += 1
        else:
            self.dead = True

# Run
if __name__ == '__main__':
    app = QApplication([])
    maxWorldAge = 128319877
    maxX = 800
    maxY = 600
    width = 800
    height = 600
    numReds = 1
    numBlues = 20
    worldSpeed = 200
    window = Window(maxWorldAge, maxX, maxY, width, height, worldSpeed)
    theWorld = window.world

    for i in range(numReds):
        newDot = RedDot(50, 10)
        x = random.randrange(theWorld.maxX)
        y = random.randrange(theWorld.maxY)
        while not theWorld.emptyLocation(x, y):
            x = random.randrange(theWorld.maxX)
            y = random.randrange(theWorld.maxY)
        theWorld.addThing(newDot, x, y)

    for i in range(numBlues):
        newDot = BlueDot(50, 10)
        x = random.randrange(theWorld.maxX)
        y = random.randrange(theWorld.maxY)
        while not theWorld.emptyLocation(x, y):
            x = random.randrange(theWorld.maxX)
            y = random.randrange(theWorld.maxY)
        theWorld.addThing(newDot, x, y)

    sys.exit(app.exec_())



