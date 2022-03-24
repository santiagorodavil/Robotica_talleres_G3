#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension


def definirVel(wheel_vel, vel_R, vel_L):
	rospy.init_node('eight_figure')
	pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size = 1)
	rate = rospy.Rate(10)
	wheel_vel.data = [vel_L, vel_R]
	while not rospy.is_shutdown():
		pub.publish(wheel_vel)
		rate.sleep()
		

	


if __name__ == '__main__':
	in_vel_R = input("Ingrese la velocidad de la rueda derecha: ") 
	in_vel_L = input("Ingrese la velocidad de la rueda izquierda: ")
	vel_R = float(in_vel_R)
	vel_L = float(in_vel_L)
	wheel_vel = Float32MultiArray()
	definirVel(wheel_vel, vel_R, vel_L)
