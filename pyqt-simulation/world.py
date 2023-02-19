from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import logging

class World(QFrame):

    msg2statusbar = pyqtSignal(str)

    logging.basicConfig(filename="PopGen/pyqt-simulation/log.log",
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        encoding="utf-8",
        level=logging.DEBUG,
        filemode="w")
    logging.info("Log file created.")

    def __init__(self, maxWorldAge, maxX, maxY, worldSpeed):
        super(World, self).__init__()

        self.timer = QBasicTimer()
        self.setStyleSheet("background-image: url('PopGen/pyqt-simulation/background.png')")
        self.setFocusPolicy(Qt.StrongFocus)

        self.maxX = maxX
        self.maxY = maxY
        self.grid = []

        self.terrainGrid = []
        self.terrainList = []

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

    def start(self): # Starting message and the clock
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

    def addTerrain(self, terrain):
        self.terrainList.append(terrain)
        for y in range(terrain.y - 1, terrain.y + terrain.h - 1):
            for x in range(terrain.x - 1, terrain.x + terrain.w - 1):
                self.terrainGrid[y][x] = terrain.type

    def visualizeTerrain(self):
        for row in self.terrainGrid:
            print(row)

    def advanceTime(self):
        if self.worldAge > self.maxWorldAge:
            self.msg2statusbar.emit("Max world age reached.")
            print("Max world age reached.")
            self.timer.stop()
            self.update()
        elif all([thing.geneLvl > 0 for thing in self.thingList]):
            self.msg2statusbar.emit("All things in world have gene presence.")
            print("All things in world have gene presence.")
            self.timer.stop()
            self.update()    
        elif self.thingList != []:
            random.shuffle(self.thingList)
            for thing in self.thingList:
                if thing.dead == True:
                    self.delThing(thing)
                else:
                    moved, mated = thing.liveALittle()
                    logMessage = str(type(thing)) + " - Moved: " + str(moved) + \
                        " | Mated: " + str(mated) + " | Gene Level: " + str(thing.geneLvl)
                    logging.info(logMessage)
        
        else:
            self.msg2statusbar.emit("There is nothing left in the world...")
            print("There is nothing left in the world...")
            self.timer.stop()
            self.update()

    def drawThing(self, painter, thing):
        #image = QPixmap(thing.imagePath)
        #painter.drawPixmap(int(thing.xPos), int(thing.yPos), 15, 15, image)

        color = QColor(thing.geneLvl, 0, 100)
        painter.setPen(QPen(color, 5, Qt.SolidLine))
        painter.drawEllipse(int(thing.xPos), int(thing.yPos), 5, 5)

    def drawTerrain(self, painter, terrain):
        painter.setPen(QPen(terrain.color, 5, Qt.SolidLine))
        painter.setBrush(QBrush(terrain.color, Qt.DiagCrossPattern))
        painter.drawRect(terrain.x, terrain.y, terrain.h, terrain.w)
    
    def paintEvent(self, event): # Draw everything for each frame.
        painter = QPainter(self)
        for thing in self.thingList:
            self.drawThing(painter, thing)
        for terrain in self.terrainList:
            self.drawTerrain(painter, terrain)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.advanceTime()
            self.update()
            self.worldAge += 1

    def emptyLocation(self, x, y):
        try:
            if self.grid[y][x] == None:
                return True
            else:
                return False
        except IndexError:
            #print("IndexError occured.")
            return False

    def checkLocation(self, x, y):
        try:
            if not self.emptyLocation(x, y):
                return self.grid[y][x]
            else:
                return None
        except IndexError:
            #print("IndexError occured.")
            return False