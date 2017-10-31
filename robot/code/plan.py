import asyncio
import cozmo

from cmap import *
from rrt import *
from utils import *
from cozmo.util import degrees, time
#from find_cube import find_cube
import numpy as np
from cozmo.util import degrees, distance_mm, Speed, radians
from time import sleep
from math import atan2
from cubesSeen import *

#from imageShow import showImage

class plan:
    def getName(self):
        return "plan"

    def run(self, robot: cozmo.robot.Robot, cmap):
        targetFound = False
        cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
        if cubes:
            for cube in cubes:
                if cube.object_id == 1:
                    targetFound = True

        if not targetFound:
            cmap.add_goal(Node((325, 225)))
            RRT(cmap, cmap.get_start())
            goals = cmap.get_goals()
            goal = goals[0]
            moveToCoord(robot, goal)
            cmap.reset()
            cmap.clear_goals()
            cmap.set_start(Node((325, 225)))

            while not targetFound:
                action = robot.turn_in_place(degrees(30))
                action.wait_for_completed()
                cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=0.5)
                if len(cubes) > 0:
                    for cube in cubes:
                        print(cube)
                        if cube.object_id == 1:
                            targetFound = True


        if cubes:
            for cube in cubes:
                x = int(round(cube.pose.position.x))
                y = int(round(cube.pose.position.y))
                cubesSeen.append(cubesSeen, cube.object_id)
                if cube.object_id == 1:
                    cmap.add_goal(Node((100,200)))
                    # cmap.add_goal(Node((x,y))) #todo: add goal with real coords
                # else: #todo: add obstacles with real coords
                #     nodes = [Node((x-20,y-20)), Node((x-20,y+20)), Node((x+20,y+20)), Node((x+20,y-20))]
                #     cmap.add_obstacle(nodes)

        # goal = None
        #
        # if len(cmap.get_goals()) == 0:
        #     [x,y] = cmap.get_size()
        #     goal = Node((x/2, y/2))
        # print(goal.x, goal.y)
        # cmap.add_goal(goal)
        # #print(startState.x, startState.y)
        # RRT(cmap, cmap.get_start())
        # # path = []
        # # print(cmap.get_goals())
        # # for x in cmap.get_goals():
        # #     curr = x
        # #     while curr is not None:
        # #         path.append(curr)
        # #         curr = curr.parent
        # # for x in path:
        # #     print(x.x, x.y)
        # print("ending right now")

        return "goTo", robot


def moveToCoord(robot, node): #return robots current angle
    parent = node.parent
    if parent == None:
        print(node.coord)
        return 0
    oldRad = moveToCoord(robot, node.parent)
    newRad = atan2(node.coord[1] - parent.coord[1], node.coord[0] - parent.coord[0])
    print(node.coord)

    action = robot.turn_in_place(radians(newRad - oldRad))
    action.wait_for_completed()
    action = robot.drive_straight(distance_mm(get_dist(parent, node)), Speed(1000), should_play_anim=False)
    action.wait_for_completed()

    return newRad