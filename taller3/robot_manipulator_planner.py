#! /usr/bin/env python3
#publica a robot_manipulator_angles el angulo del end deffector
import math as m
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point

angulo = Twist()
def positonToAngle(position):
	global angulo

	link1 =8 
	link2 =13

	x = position.x
	y = position.y
	z = position.z
	#theta2 = mitad
	#theta1 = base


	x_2d = m.sqrt(x*x+y*y)

	theta_giro = 1/m.cos(x/x_2d)

	cos_theta2 =  (1/(2*link1*link2)) * ((x_2d*x_2d + z*z)-(link1*link1 +link2*link2))

	cos_theta1 = (1/(x_2d*x_2d + z*z)) * (x_2d*(link1+(link2*cos_theta2)) + z*(link2*m.sqrt(1- cos_theta2*cos_theta2)))
	print(str(cos_theta1)+ "cos +")

	cos_theta1 = (1/(x_2d*x_2d + z*z)) * (x_2d*(link1+(link2*cos_theta2)) - z*(link2*m.sqrt(1- cos_theta2*cos_theta2)))
	print(str(cos_theta1)+ "cos -")

	angulo.linear.x = theta_giro*(180/m.pi)
	angulo.linear.y = m.acos(cos_theta1)*(180/m.pi)
	angulo.linear.z = 1/cos_theta2*(180/m.pi)

	print(angulo)
	sendAngle = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	sendAngle.publish(angulo)

def planner():
	global angulo
	rospy.init_node("robot_manipulator_planner")
	rospy.Subscriber('robot_manipulator_goal', Point, positonToAngle)

	pub = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		pub.publish(angulo)
		rate.sleep()
if __name__ == '__main__':
	planner()
