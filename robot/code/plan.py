import asyncio
import cozmo

import rrt
from cmap import *
from rrt import *
from cozmo.util import degrees, time
#from find_cube import find_cube
import numpy as np

#from imageShow import showImage



YELLOW_LOWER = np.array([68, 113, 158])
YELLOW_UPPER = np.array([113, 195, 255])

class plan:
    def getName(self):
        return "plan"

    def run(self, robot: cozmo.robot.Robot, cmap):
        goal = None

        if len(cmap.get_goals()) == 0:
            [x,y] = cmap.get_size()
            goal = Node((x/2, y/2))
        print(goal.x, goal.y)
        cmap.add_goal(goal)
        #print(startState.x, startState.y)
        RRT(cmap, cmap.get_start())
        path = []
        print(cmap.get_goals())
        for x in cmap.get_goals():
            curr = x
            while curr is not None:
                path.append(curr)
                curr = curr.parent
        for x in path:
            print(x.x, x.y)
        print("ending right now")

        return "stop", robot


