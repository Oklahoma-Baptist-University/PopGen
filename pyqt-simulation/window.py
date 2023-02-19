from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import world as wor

class Window(QMainWindow):
    def __init__(self, maxWorldAge, maxX, maxY, w, h, worldSpeed):
        super(Window, self).__init__()

        self.world = wor.World(maxWorldAge, maxX, maxY, worldSpeed)
  
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("border : 2px solid black;")
  
        # Calling showMessage method when signal received by World.
        self.world.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.world)
  
        self.setWindowTitle('Simulation')
  
        self.setGeometry(maxX, maxY, w, h)
        self.setFixedSize(w, h)
  
        self.world.start()
  
        self.show()