#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math as m


final_position = Twist()



def setAngles(servo):
	'''
	angulo de los servos:

	linear.x -> servo giratorio  u,j
	linear.y -> servo base i,k
	linear.z -> servo mitad o,l
	angular.x -> servo garra
	'''
	global final_position
	link1 = 8
	link2 = 13
	
	theta_giro = servo.linear.x *m.pi/180.0
	theta_base = servo.linear.y*m.pi/180.0
	theta_mitad = servo.linear.z*m.pi/180.0

	arm_length =  m.cos(theta_base)*link1 + m.cos(theta_mitad)*link2
	arm_height = m.sin(theta_base)*link1 + m.sin(theta_mitad)*link2

	final_position.linear.x = m.cos(theta_giro)*arm_length
	final_position.linear.y = m.sin(theta_giro)*arm_length
	final_position.linear.z = arm_height
	print(arm_length)

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


