# The Simulation

This simulation is a framework for simulating population growth and gene tracking. The different colored dots can be representative of real world objects, and there is a  gene tracking system in place which is visually seen by the color of red spreading through the blue dots as the generations go by. Terrain is visually seen and can be built using terrain classes, but right now it does not impact the life of the dots.

# Instructions

1. Verify PyQt5 is installed on your system. You can use the command `pip install pyqt5` in Terminal.
2. Open "run.py"
3. Edit variables at the top of the file as desired:
    * `maxWorldAge` = How long the world will run if thing count never hit 0
    * `maxX` = Max X length of grid and window
    * `maxY` = Max Y length of grid and window
    * `numReds` = Number of red dots at beginning of simulation.
    * `numBlues` = Number of Blue dots at beginning of simulation.
    * `maxCreatureAge` = How old a dot can be before it dies. Currently not in use for testing.
    * `worldSpeed` = How fast the world ticks in milliseconds
    * `geneTransferSpeed` = How fast the red gene spreads.
4. Run file

# Class Summaries

### Window
* Main window built out of a `QMainWindow` widget. Holds the world class and listens for signals from it.
* Methods:
    * None

### World
* World itself built out of a `QFrame` widget. Just about everything happens within here.
* Methods:
    * `start` - Starts the timer of the world.
    * `addThing` - Adds a creature to the world.
    * `delThing` - Removes a creature from the world.
    * `addTerrain` - Adds terrain to the world.
    * `visualizeTerrain` - Prints terrain grid in a readable format.
    * `advanceTime` - Advances the age of the world by one increment and checks for simulation ending conditions.
    * `drawThing` - Draws creature at its current location.
    * `drawTerrain` - Draws terrain at its current location.
    * `paintEvent` - Draws all creatures and terrain in the world.
    * `timerEvent` - Loop that runs the `advanceTime` method and ages world.
    * `emptyLocation` - Checks to see if location is empty.
    * `checkLocation` - Returns whatever is at a location.

### Creatures
* File contains the varying classes of creatures contained within the world.
* Methods:
    * `tryToMove` - Looks around creature for empty location to move to.
    * `birth` - Looks around creature for empty location to create new creature.
    * `findMate` - Looks around creature for potential mate and returns what is found.
    * `liveALittle` - Method which defines how each creature actually lives its life.
    * `passOnGene` - Takes what creature is found in the `findMate` method, determines gene level of baby, and executes `birth` method with appropriate child.   
    
### Terrain
* File contains the varying classes of terrain contained within the world.
* Methods:
    * None

### Run
* File containing code to actually run simulation.
* Methods:
    * None

# Known Issues

* Adjusting the height and width of the simulation using the variables does not resize the screen well. The X and Y grid does not scale with everything properly.
* To keep the population stable for testing, the `maxAge` attribute is currently not used and each creature just lives until it has one child.
* The dots all freeze one by one once the simulation has run a certain duration, completely unknown why. It appears to happen slower the less dots are present in the simulation.
* The terrain currently does not impact anything the dots do.

*Code by Joshua Graham, based on work from Python Programming in Context, 3rd Edition by Bradley Miller, David Ranum, and Julie Anderson.*