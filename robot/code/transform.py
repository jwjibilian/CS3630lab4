from math import cos, sin
def robotToGlobal(robot, cmap, point):
    theta = robot.pose_angle.radians
    x = cmap.get_start().x
    y = cmap.get_start().y
    rot =[[cos(theta), sin(theta),x],[-sin(theta), cos(theta), y],[0,0,1]]
    a = rot[0][0]*point[0] + rot[0][1]*point[1] + rot[0][2]
    b = rot[1][0]*point[0] + rot[1][1]*point[1] + rot[1][2]
    c = rot[2][0]*point[0] + rot[2][1]*point[1] + rot[2][2]
    position = [[a],[b],[c]]
    return position

def globalToRobot(robot, cmap, point):
    theta = -robot.pose_angle.radians
    x = -cmap.get_start().x
    y = -cmap.get_start().y
    rot =[[cos(theta), -sin(theta),x],[sin(theta), cos(theta), y],[0,0,1]]
    a = rot[0][0]*point[0] + rot[0][1]*point[1] + rot[0][2]
    b = rot[1][0]*point[0] + rot[1][1]*point[1] + rot[1][2]
    c = rot[2][0]*point[0] + rot[2][1]*point[1] + rot[2][2]
    position = [[a],[b],[c]]
    return position