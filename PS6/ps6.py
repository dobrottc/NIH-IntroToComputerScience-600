import math
import random

import ps6_visualize
import pylab
import numpy as np
import matplotlib.pyplot as plt

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    roomBinA = None
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.roomBinA = np.zeros((width,height))
        self.width = width
        self.height = height
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.roomBinA[int(pos.x), int(pos.y)] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return bool(self.roomBinA[m,n])
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return np.prod(np.shape(self.roomBinA))

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return np.sum(self.roomBinA.ravel()==1)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(np.random.rand()*self.width,
                            np.random.rand()*self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if ((pos.x >= 0) & (pos.x < self.width)
            and (pos.y >= 0 ) & (pos.y < self.height)):
            return True
        else:
            return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = int(np.random.rand()*360)
        self.pos = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.pos)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return(self.pos)
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return(self.direction)

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.

        NOTE: this is an abstract method, do not implement it here!
        """
        raise NotImplementedError('This is an abstract method, do not call in the Robot class')


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """


    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        while True:
            newPos = self.pos.getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(newPos):
                break
            else:
                self.direction = int(np.random.rand()*360)
                continue
        # now we know newPos is in the room, and we have a good direction, brute force all points
        for (iS,tS) in enumerate(np.linspace(0,self.speed,100)):
            tempPos = self.pos.getNewPosition(self.direction, tS)
            self.room.cleanTileAtPosition(tempPos)

        self.pos = newPos

        return

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """

    nStepsV = np.zeros((num_trials,))
    for iT in range(num_trials):
        room = RectangularRoom(width=width, height=height)

        robotL = []
        for iL in range(num_robots):
            robotL.append(robot_type(room, speed))

        tNSteps = 0
        while True:
            for (iL, tL) in enumerate(robotL):
                    tL.updatePositionAndClean()
            tNSteps = tNSteps + 1
            coverage = room.getNumCleanedTiles() / room.getNumTiles()
            if coverage >= min_coverage:
                break
        nStepsV[iT] = tNSteps
    #print('debug: steps each trial: %s' % repr(nStepsV))
    return (np.mean(nStepsV))


# === Problem 4

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """

    robotV = np.arange(1,10)
    outV = 0.0*robotV.copy()
    
    for (iR,tR) in enumerate(robotV):
        outV[iR] = \
                   runSimulation(num_robots=tR, speed=2, width=20, height=20, 
                                     min_coverage=0.8, num_trials=20, robot_type=StandardRobot)

    plt.plot(robotV, outV)

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """

    sizeL = [ (20,20), (25,16), (40,10), (50,8), (80,5), (100,4) ]
    outV = np.zeros((6,1))
    
    for (iS,tS) in enumerate(sizeL):
        outV[iS] = \
                   runSimulation(num_robots=2, speed=2, width=tS[0], height=tS[1], 
                                     min_coverage=0.8, num_trials=10, robot_type=StandardRobot)

    plt.plot(outV)
