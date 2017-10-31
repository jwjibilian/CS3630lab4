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
import transform
#from imageShow import showImage

global cmap, startState, cubesSeenBefore

class goTo:
    def getName(self):
        return "goTo"


    def run(self, robot: cozmo.robot.Robot, cmap):
        print(cubesSeenBefore)

        # cubes = None
        # while True:
        #     try:
        #         cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
        #     except asyncio.TimeoutError:
        #         print("Cube not found")
        #     if cubes:
        #         print("x:", cubes[0].pose.position.x, " y:", cubes[0].pose.position.y, " z:", cubes[0].pose.position.z)
        #         print("robot -- x:", robot.pose.position.x, " y:", robot.pose.position.y, " z:", robot.pose.position.z)

        thestack = stack()
        goals = cmap.get_goals()
        node = goals[0]
        while node is not None:
            thestack.push(node)
            print(node.x, node.y)
            node = node.parent

        fromNode = thestack.pop()
        oldRad = robot.pose_angle.radians
        while not thestack.isEmpty():
            toNode = thestack.pop()

            newRad = atan2(toNode.coord[1] - fromNode.coord[1], toNode.coord[0] - fromNode.coord[0])

            action = robot.turn_in_place(radians(newRad - oldRad))
            action.wait_for_completed()

            #TODO: check for obj



            action = robot.drive_straight(distance_mm(get_dist(fromNode, toNode)), Speed(1000), should_play_anim=False)
            action.wait_for_completed()
            print(robot.pose)

            oldRad = newRad
            fromNode = toNode
        cmap.reset()
        cmap.set_start(fromNode)

        x = transform.robotToGlobal(robot, cmap, [50, 0])
        print('&&&&&&&&&&&&&&&&&&&&&&&&&')
        for y in x:
            for z in y:
                print(z)
        print('$$$$$$$$$$$$$$$$$$$$$$')
        a = x[0][0]
        b = x[1][0]
        # a = int(a)
        # b = int(b)
        nodes = [Node([a,b]),Node([a+20,b]), Node([a+20,b+20]), Node([a,b+20]) ]
        cmap.add_obstacle(nodes)

        return "stop", robot

def checkNewNode(robot):
    cubes = None
    try:
        cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
    except asyncio.TimeoutError:
        print("Cube not found")

    if cubes:
        cubesSeenBefore = [1, 2 ,3]
        for cube in cubes:
            cubeSeenBefore = False
            if cube.object_id in cubesSeenBefore:
                cubeSeenBefore = True
            if not cubeSeenBefore:
                # add to map as obstacle
                # set start location to robot's fromNode coords
                # break out of stack
                # run goTo
                pass