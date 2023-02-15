from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import random
from abc import ABC, abstractmethod

# Class for anything that moves around.
class MovingObject(ABC):
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
        self.distantOffset = [(-3, 3),  (-2, 3),  (-1, 3),  (0, 3),  (1, 3),  (2, 3),  (3, 3),
                              (-3, 2),  (-2, 2),  (-1, 2),  (0, 2),  (1, 2),  (2, 2),  (3, 2),
                              (-3, 1),  (-2, 1),  (-1, 1),  (0, 1),  (1, 1),  (2, 1),  (3, 1),
                              (-3, 0),  (-2, 0),  (-1, 0),           (1, 0),  (2, 0),  (3, 0),
                              (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
                              (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
                              (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3)]

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
            return True
        
        return False

    def birth(self, baby):
        randomOffsetIndex = random.randrange(len(self.offsetList))
        randomOffset = self.offsetList[randomOffsetIndex]
        nextX = self.xPos + randomOffset[0]
        nextY = self.yPos + randomOffset[1]
        mateFound = False
        while not (0 <= nextX < self.world.maxX and \
                0 <= nextY < self.world.maxY):
            randomOffsetIndex = random.randrange(len(self.offsetList))
            randomOffset = self.offsetList[randomOffsetIndex]
            nextX = self.xPos + randomOffset[0]
            nextY = self.yPos + randomOffset[1]

        if self.world.emptyLocation(nextX, nextY):
            self.world.addThing(baby, nextX, nextY)
            self.babies += 1
            return True
        return False

    @abstractmethod
    def findMate(self, baby):
        return

    #@abstractmethod
    def liveALittle(self):
        if self.babies < 1:
            moved = self.tryToMove()
            mated = self.findMate()
            self.age += 1
        else:
            moved = False
            mated = False
            self.dead = True
        
        return moved, mated
    

# Red
class RedDot(MovingObject):
    def __init__(self, maxAge, speed):
        super().__init__(maxAge, speed)
        self.geneLvl = 255
        self.color = QColor(self.geneLvl, 0, 0)
        self.babies = 0

    def findMate(self):
        mateFound = None
        for offset in self.distantOffset:
            thingThere = self.world.checkLocation(self.xPos + offset[0], self.yPos + offset[1])
            if isinstance(thingThere, BlueDot):
                mateFound = "blue"
                break
            if isinstance(thingThere, RedDot):
                mateFound = "red"
                break
            if isinstance(thingThere, nextGenDot):
                mateFound = "nextGen"
                break

        if mateFound == "blue":
            baby = nextGenDot(self.maxAge, self.speed)
            baby.geneLvl += 25
            self.birth(baby)
            return True
        if mateFound == "red":
            baby = RedDot(self.maxAge, self.speed)
            self.birth(baby)
            return True
        if mateFound == "nextGen":
            baby = nextGenDot(self.maxAge, self.speed)
            baby.geneLvl += thingThere.geneLvl + 25
            self.birth(baby)
            return True
    
        return False

# Blue
class BlueDot(MovingObject):
    def __init__(self, maxAge, speed):
        super().__init__(maxAge, speed)
        self.geneLvl = 0
        self.color = QColor(self.geneLvl, 0, 255)
        self.babies = 0

    def findMate(self):
        mateFound = None
        for offset in self.distantOffset:
            thingThere = self.world.checkLocation(self.xPos + offset[0], self.yPos + offset[1])
            if isinstance(thingThere, BlueDot):
                mateFound = "blue"
                break
            if isinstance(thingThere, RedDot):
                mateFound = "red"
                break
            if isinstance(thingThere, nextGenDot):
                mateFound = "nextGen"
                break

        if (mateFound == "red") or (mateFound == "nextGen"):
            baby = nextGenDot(self.maxAge, self.speed)
            baby.geneLvl += thingThere.geneLvl
            self.birth(baby)
            return True
        if mateFound == "blue":
            baby = BlueDot(self.maxAge, self.speed)
            self.birth(baby)
            return True

        return False


class nextGenDot(MovingObject):
    def __init__(self, maxAge, speed):
        super().__init__(maxAge, speed)
        self.geneLvl = 0
        self.color = QColor(self.geneLvl, 0, 255)
        self.babies = 0

    def findMate(self):
        mateFound = None
        for offset in self.distantOffset:
            thingThere = self.world.checkLocation(self.xPos + offset[0], self.yPos + offset[1])
            if isinstance(thingThere, BlueDot):
                mateFound = "blue"
                break
            if isinstance(thingThere, RedDot): # Make this a function
                mateFound = "red"
                break
            if isinstance(thingThere, nextGenDot):
                mateFound = "nextGen"
                break

        if mateFound == "blue":
            baby = nextGenDot(self.maxAge, self.speed)
            baby.geneLvl += 25
            self.birth(baby)
            return True
        if mateFound == "red":
            baby = nextGenDot(self.maxAge, self.speed)
            baby.geneLvl += self.geneLvl + 25
            self.birth(baby)
            return True
        if mateFound == "nextGen":
            baby = nextGenDot(self.maxAge, self.speed)
            #baby.geneLvl = int((thingThere.geneLvl + self.geneLvl) / 2)
            baby.geneLvl += thingThere.geneLvl + 25
            self.birth(baby)
            return True

        return False