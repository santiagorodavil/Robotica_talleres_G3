#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist

longitud = 13.4
diametro = 6.8

x = 0
y = 0
theta = 0
pose = Pose2D()

dt = 0.05
def callback(vel_msg):
    global x
    global y
    global theta
    global longitud
    global pose
    
    velocidadLineal = ((vel_msg.linear.x*100)/10) + 70
    velocidadAngular = (vel_msg.angular.z*longitud)/2
    for i in np.arange(0,3,dt):
        if velocidadLineal != 0 :
            x = (x + 0.5 * (velocidadLineal) * np.cos(theta) * dt)
            y = (y + 0.5 * (velocidadLineal) * np.sin(theta) * dt)
            theta = (theta + (1/longitud) * velocidadAngular * dt)
    pose.x = x
    pose.y = y
    pose.theta =theta
    

def main():
	global pose
	rospy.init_node('Odometria')
	velocidad_subscriber = rospy.Subscriber('/turtlebot_cmdVel',Twist,callback)
	velocidad_publisher = rospy.Publisher('/turtlebot_position',Pose2D,queue_size=10)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
	    velocidad_publisher.publish(pose)
	    rate.sleep()
	    
	
if __name__=='__main__':
	main()
	
