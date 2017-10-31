import asyncio
import sys
import cv2
import numpy as np
import cozmo
from cmap import *
from statemachine import *

import time
import stopMachine
import plan
from cozmo.util import degrees, distance_mm, Speed, radians


def run(robot: cozmo.robot.Robot, cmap):

    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = True
    robot.camera.enable_auto_exposure = True

    thePlaner =  plan.plan()
    stopM = stopMachine.stop()
    fm = StateMachine()
    fm.addState(thePlaner)
    fm.addState(stopM)
    fm.setStartState(thePlaner)
    fm.setEndState(stopM)
    fm.run(robot, cmap)



if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)