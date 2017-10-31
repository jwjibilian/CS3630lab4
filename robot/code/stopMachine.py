import asyncio
import cozmo
from cmap import *
from rrt import *
from cozmo.util import degrees, time
#from find_cube import find_cube
import numpy as np

#from imageShow import showImage

global cmap, startState

class stop:
    def getName(self):
        return "stop"

    def run(self, robot: cozmo.robot.Robot, cmap):
        print("should not run")
        return "stop", robot

