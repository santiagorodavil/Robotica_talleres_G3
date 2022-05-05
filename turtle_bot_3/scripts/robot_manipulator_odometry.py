#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math as m


final_position = Twist()



def setAngles(servo):
	'''
	angulo de los servos:

	linear.x -> servo giratorio
	linear.y -> servo base
	linear.z -> servo mitad
	angular.x -> servo garra
	'''
	global final_position
	link1 = 8
	link2 = 17

	theta_giro = servo.linear.x
	theta_base = servo.linear.y
	theta_mitad = servo.linear.z

	arm_length =  m.cos(theta_base)*link1 + m.cos(theta_mitad)*link2
	arm_height = m.sin(theta_base)*link1 + m.sin(theta_mitad)*link2

	final_position.linear.x = m.cos(theta_giro)*arm_length
	final_position.linear.y = m.sin(theta_giro)*arm_length
	final_position.linear.z = arm_height

	sendPos = rospy.Publisher('robot_manipulator_position', Twist, queue_size = 10)
	sendPos.publish(final_position)



def robotOdom():
	global final_position

	rospy.init_node('robot_manipulator_odom')
	rospy.Subscriber("robot_manipulator_angles",Twist,setAngles)
	pub = rospy.Publisher('robot_manipulator_position',Twist, queue_size = 10)
	rate = rospy.Rate(10)
	final_position = Twist()

	while not rospy.is_shutdown():
		pub.publish(final_position)
		rate.sleep()



if __name__ == '__main__':
	robotOdom()


