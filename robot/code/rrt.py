import cozmo

import TheMachine
from cmap import *
from gui import *
from utils import *
from random import *
from time import sleep
from math import atan2
from cubesSeen import *


import asyncio
from cozmo.util import degrees, distance_mm, Speed, radians

MAX_NODES = 20000

################################################################################
# NOTE:
# Before you start, please familiarize yourself with class Node in utils.py
# In this project, all nodes are Node object, each of which has its own
# coordinate and parent if necessary. You could access its coordinate by node.x
# or node[0] for the x coordinate, and node.y or node[1] for the y coordinate
################################################################################

def step_from_to(node0, node1, limit=75):
    ############################################################################
    # TODO: please enter your code below.
    # 1. If distance between two nodes is less than limit, return node1
    # 2. Otherwise, return a node in the direction from node0 to node1 whose
    #    distance to node0 is limit. Recall that each iteration we can move
    #    limit units at most
    # 3. Hint: please consider using np.arctan2 function to get vector angle
    # 4. Note: remember always return a Node object
    distance = get_dist(node0, node1)
    if ( distance <= limit):
        return node1
    newx = (((node1.x - node0.x)/distance)*limit) + node0.x
    newy = (((node1.y - node0.y) / distance) * limit) + node0.y
    node1 = Node((newx, newy))
    return node1
    ############################################################################


def node_generator(cmap):
    rand_node = Node([-1,-1])
    ############################################################################
    # TODO: please enter your code below.
    # 1. Use CozMap width and height to get a uniformly distributed random node
    # 2. Use CozMap.is_inbound and CozMap.is_inside_obstacles to determine the
    #    legitimacy of the random node.
    # 3. Note: remember always return a Node object
    pass
    map_width, map_height = cmap.get_size()
    while not cmap.is_inbound(rand_node) and not cmap.is_inside_obstacles(rand_node):
        rand_node = Node([randint(0, map_width),randint(0, map_height)])
    ############################################################################
    return rand_node


def RRT(cmap, start):
    cmap.add_node(start)

    map_width, map_height = cmap.get_size()

    while (cmap.get_num_nodes() < MAX_NODES):
        ########################################################################
        # TODO: please enter your code below.
        # 1. Use CozMap.get_random_valid_node() to get a random node. This
        #    function will internally call the node_generator above
        # 2. Get the nearest node to the random node from RRT
        # 3. Limit the distance RRT can move
        # 4. Add one path from nearest node to random node
        #
        rand_node = None
        nearest_node = None
        pass
        rand_node = cmap.get_random_valid_node()

        thenodes = cmap.get_nodes()
        for n in thenodes:
            if nearest_node is None:
                nearest_node = n
            if get_dist(rand_node, n) < get_dist(rand_node, nearest_node):
                nearest_node = n
        theLimit = 80
        rand_node = step_from_to(nearest_node, rand_node, limit = theLimit)
        #######################################################################
        # sleep(0.01)
        cmap.add_path(nearest_node, rand_node)
        if cmap.is_solved():
            break

    if cmap.is_solution_valid():
        print("A valid solution has been found :-) ")
    else:
        print("Please try again :-(")




def CozmoPlanning(robot: cozmo.robot.Robot):
    # Allows access to map and stopevent, which can be used to see if the GUI
    # has been closed by checking stopevent.is_set()
    global cmap, stopevent, goal, startState, themap

    startState = Node((100,75))
    ########################################################################
    # TODO: please enter your code below.
    # Description of function provided in instructions
    robot.set_head_angle(degrees(-5)).wait_for_completed()
    robot.move_lift(-5)
    print(cmap.get_start().x," ", cmap.get_start().y)
    TheMachine.run(robot,cmap)

    # cubes = None
    # try:
    #     cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
    # except asyncio.TimeoutError:
    #     print("Cube not found")
    #
    # print(cubes)



    # while True:
    #     try:
    #         cubes = await robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
    #     except asyncio.TimeoutError:
    #         print("Cube not found")
    #     if cubes:
    #         print("x:", cubes[0].pose.position.x, " y:", cubes[0].pose.position.y, " z:", cubes[0].pose.position.z)

    # cmap.add_goal(Node((325,225)))
    # nodes = [Node((280,160)), Node((320,160)), Node((320,340)), Node((280,340))]
    # cmap.add_obstacle(nodes)
    # RRT(cmap, cmap.get_start())
    #
    # goals = cmap.get_goals()
    # goal = goals[0]
    # print("goal:", goal.coord)
    # await moveToCoord(robot, goal)





    # action = robot.drive_straight(distance_mm(30), Speed(1000), should_play_anim=False)
    # await action.wait_for_completed()

def beginSearch(robot, cmap):
    targetFound = False
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
    if cubes:
        for cube in cubes:
            if cube.object_id == 3:
                targetFound = True

    if not targetFound:
        cmap.add_goal(Node((325, 225)))
        RRT(cmap, cmap.get_start())
        goals = cmap.get_goals()
        goal = goals[0]
        moveToCoord(robot, goal)

        try:
            cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=1)
        except asyncio.TimeoutError:
            print("Cube not found")


    if cubes:
        for cube in cubes:
            x = int(round(cube.pose.position.x))
            y = int(round(cube.pose.position.y))
            if cube.object_id == 3:
                cmap.add_goal(Node((x,y)))
            else:
                nodes = [Node((x-20,y-20)), Node((x-20,y+20)), Node((x+20,y+20)), Node((x+20,y-20))]
                cmap.add_obstacle(nodes)

async def moveToCoord(robot, node): #return robots current angle
    parent = node.parent
    if parent == None:
        print(node.coord)
        return 0
    oldRad = await moveToCoord(robot, node.parent)
    newRad = atan2(node.coord[1] - parent.coord[1], node.coord[0] - parent.coord[0])
    print(node.coord)

    action = robot.turn_in_place(radians(newRad - oldRad))
    await action.wait_for_completed()
    action = robot.drive_straight(distance_mm(get_dist(parent, node)), Speed(1000), should_play_anim=False)
    await action.wait_for_completed()

    return newRad



    

################################################################################
#                     DO NOT MODIFY CODE BELOW                                 #
################################################################################

class RobotThread(threading.Thread):
    """Thread to run cozmo code separate from main thread
    """

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        # Please refrain from enabling use_viewer since it uses tk, which must be in main thread
        cozmo.run_program(CozmoPlanning,use_3d_viewer=False, use_viewer=False)
        stopevent.set()


class RRTThread(threading.Thread):
    """Thread to run RRT separate from main thread
    """

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while not stopevent.is_set():
            RRT(cmap, cmap.get_start())
            sleep(100)
            cmap.reset()
        stopevent.set()


if __name__ == '__main__':
    global cmap, stopevent
    stopevent = threading.Event()
    cmap = CozMap("maps/emptygrid.json", node_generator)
    robot_thread = RobotThread()
    robot_thread.start()
    visualizer = Visualizer(cmap)
    visualizer.start()
    stopevent.set()
