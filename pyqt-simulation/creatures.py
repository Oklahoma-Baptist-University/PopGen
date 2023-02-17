from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import random
from abc import ABC, abstractmethod

# Class for anything that moves around.
class MovingObject(ABC):
    def __init__(self, maxAge, speed, geneTransferSpeed):
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
        self.geneTransferSpeed = geneTransferSpeed

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
        return mateFound, thingThere

    @abstractmethod
    def passOnGene(self, mateFound, thing):
        return

    def geneCheck(self, baby):
        if baby.geneLvl > 255:
            baby.geneLvl = 255

    #@abstractmethod
    def liveALittle(self):
        if self.babies < 1:
            moved = self.tryToMove()
            mateFound, thing = self.findMate()
            mated = self.passOnGene(mateFound, thing)
            self.age += 1
        else:
            moved = False
            mated = False
            self.dead = True
        
        return moved, mated


# Red
class RedDot(MovingObject):
    def __init__(self, maxAge, speed, geneTransferSpeed):
        super().__init__(maxAge, speed, geneTransferSpeed)
        self.geneTransferSpeed = geneTransferSpeed
        self.geneLvl = 255
        self.babies = 0

    def passOnGene(self, mateFound, thing):
        if mateFound == "blue":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True
        if mateFound == "red":
            baby = RedDot(self.maxAge, self.speed, self.geneTransferSpeed)
            self.geneCheck(baby)
            self.birth(baby)
            return True
        if mateFound == "nextGen":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += thing.geneLvl + self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True
    
        return False

# Blue
class BlueDot(MovingObject):
    def __init__(self, maxAge, speed, geneTransferSpeed):
        super().__init__(maxAge, speed, geneTransferSpeed)
        self.geneTransferSpeed = geneTransferSpeed
        self.geneLvl = 0
        self.babies = 0

    def passOnGene(self, mateFound, thing):
        if mateFound == "red":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True
        if mateFound == "nextGen":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += thing.geneLvl
            self.geneCheck(baby)
            self.birth(baby)
        if mateFound == "blue":
            baby = BlueDot(self.maxAge, self.speed, self.geneTransferSpeed)
            self.geneCheck(baby)
            self.birth(baby)
            return True

        return False


class nextGenDot(MovingObject):
    def __init__(self, maxAge, speed, geneTransferSpeed):
        super().__init__(maxAge, speed, geneTransferSpeed)
        self.geneTransferSpeed = geneTransferSpeed
        self.geneLvl = 0
        self.babies = 0

    def passOnGene(self, mateFound, thing):
        if mateFound == "blue":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True
        if mateFound == "red":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += self.geneLvl + self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True
        if mateFound == "nextGen":
            baby = nextGenDot(self.maxAge, self.speed, self.geneTransferSpeed)
            baby.geneLvl += thing.geneLvl + self.geneTransferSpeed
            self.geneCheck(baby)
            self.birth(baby)
            return True

        return False