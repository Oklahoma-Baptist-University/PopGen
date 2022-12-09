# The Simulation

This simulation is a framework for simulating population growth and gene tracking. The different colored dots can be representative of real world objects, and there is a rudimentary gene tracking system in place which is visually seen by the color of the red dots getting increasingly darker as the generations go by. Currently the red dots are set to have more offspring, demonstrating the spread of a gene while the simulation is not yet programmed for the dots to interact.

# Instructions

1. Verify PyQt5 is installed on your system. You can use the command `pip install pyqt5` in Terminal.
1. Open "simulation.py"
2. Edit variables at the bottom of the file as desired:
    * `maxWorldAge` = How long the world will run if thing count never hit 0
    * `worldSpeed` = How fast the world ticks in milliseconds
3. Run file

# Notes

* Adjusting the height and width of the simulation using the variables does not resize the screen well. The x and y grid does not scale with everything properly.
* There is currently no interaction between different "things" in the simulation.
* Once the dots are black, they remain that color.

*Code by Joshua Graham, based on work from Python Programming in Context, 3rd Edition by Bradley Miller, David Ranum, and Julie Anderson.*