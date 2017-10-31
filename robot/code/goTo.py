import asyncio
import cozmo
from cmap import *
from rrt import *
from cozmo.util import degrees, time
#from find_cube import find_cube
import numpy as np
import stack

#from imageShow import showImage

global cmap, startState

class goTo:
    def getName(self):
        return "goTo"

    def run(self, robot: cozmo.robot.Robot, cmap):
        thething = stack()

        return "stop", robot

