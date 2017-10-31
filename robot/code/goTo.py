import asyncio
import cozmo
from cmap import *
from rrt import *
from cozmo.util import degrees, time
#from find_cube import find_cube
import numpy as np
from stack import *
from math import atan2
from cozmo.util import degrees, distance_mm, Speed, radians
from utils import *
#from imageShow import showImage

global cmap, startState

class goTo:
    def getName(self):
        return "goTo"


    def run(self, robot: cozmo.robot.Robot, cmap):
        thestack = stack()
        goals = cmap.get_goals()
        node = goals[0]
        while node is not None:
            thestack.push(node)
            print(node.x, node.y)
            node = node.parent

        fromNode = thestack.pop()
        oldRad = 0
        while not thestack.isEmpty():
            toNode = thestack.pop()

            newRad = atan2(toNode.coord[1] - fromNode.coord[1], toNode.coord[0] - fromNode.coord[0])

            action = robot.turn_in_place(radians(newRad - oldRad))
            action.wait_for_completed()
            action = robot.drive_straight(distance_mm(get_dist(fromNode, toNode)), Speed(1000), should_play_anim=False)
            action.wait_for_completed()

            oldRad = newRad
            fromNode = toNode

        return "stop", robot


# parent = node.parent
# if parent == None:
#     print(node.coord)
#     return 0
# oldRad = await moveToCoord(robot, node.parent)
# newRad = atan2(node.coord[1] - parent.coord[1], node.coord[0] - parent.coord[0])
# print(node.coord)
#
# action = robot.turn_in_place(radians(newRad - oldRad))
# await action.wait_for_completed()
# action = robot.drive_straight(distance_mm(get_dist(parent, node)), Speed(1000), should_play_anim=False)
# await action.wait_for_completed()
