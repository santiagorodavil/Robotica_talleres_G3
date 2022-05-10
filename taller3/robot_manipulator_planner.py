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
	#CAmbiar link por la distancia del brazo totalmente estirado
	link =  18

	x = position.x
	if x == link:
		x = x - 1e-8
	elif x == -link:
		x = x + 1e-8


	y = position.y
	if y == link:
		y = y - 1e-8

	elif y == -link:
		y = y + 1e-8
	#theta2 = mitad
	#theta1 = base


	theta_y = m.asin(y/link) #radianes

	theta_giro = (m.acos(x/link)) #radianes

	if theta_giro > m.pi:
		theta_giro = theta_giro - m.pi
	if y < 0:
		theta_y = theta_y + m.pi 

	#if theta_y > m.pi:
		#theta_y = theta_y - m.pi/2


	




	#cos_theta2 =  (1/(2*link1*link2)) * ((x_2d*x_2d + z*z)-(link1*link1 +link2*link2))

	#cos_theta1 = (1/(x_2d*x_2d + z*z)) * (x_2d*(link1+(link2*cos_theta2)) + z*(link2*m.sqrt(1- cos_theta2*cos_theta2)))
	print(str(theta_giro)+ " giro")

	#cos_theta1 = (1/(x_2d*x_2d + z*z)) * (x_2d*(link1+(link2*cos_theta2)) - z*(link2*m.sqrt(1- cos_theta2*cos_theta2)))
	print(str(theta_y)+ " altura")

	angulo.linear.x = round(m.degrees(theta_giro))
	angulo.linear.y = round(m.degrees(theta_y))
	angulo.linear.z = round(90)

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
