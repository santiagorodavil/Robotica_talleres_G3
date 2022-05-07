#! /usr/bin/env python3
import math as m
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
angulo = Twist()
tomar_bola = True

def positonToAngle(position):
	global angulo
	global tomar_bola

	link1 =8 
	link2 =13
	x = position.x
	y = position.y
	z = position.z

		# Mueve el eje de rotacion hasta que la bola quede en la franja central de la imagen
	while tomar_bola ==True:
		print("-------------------")
		if x<315:
			x = x+1
			angulo.linear.x = round(x*135/620)
			angulo.linear.y = 90
			angulo.linear.z = z
			print(str(angulo.linear.x)+" if")
			rot_angle = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
			rot_angle.publish(angulo)
		else:
			x = x-1
			angulo.linear.x = x*135/620
			angulo.linear.y = 90
			angulo.linear.z = z
			#angulo.angular.z = 1
			print(str(angulo.linear.x)+" else")
			rot_angle = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
			rot_angle.publish(angulo)
		if(x>270 and x<330):
			tomar_bola = False
			#x < 270 and x > 350
	print("****************")
	#max y = 473.  Regla de 3 para el angulo que debe tomar el servo
	theta1 = round(90-(y*90/473))
	print(theta1)

	# Restar el angulo del servo hasta que se encuentre en frente del ping pong
	while y >(theta1+10):
		y = y-1
		angulo.linear.y = y
		rot_angle = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
		rot_angle.publish(angulo)

	#### Cerrar la garra
	angulo.angular.x = 0
	angulo.linear.y = theta1
	rot_angle = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	rot_angle.publish(angulo)
	

	###theta2 = mitad
	###theta1 = base
def plannerCamera():
	global angulo
	rospy.init_node("robot_manipulator_planner")
	rospy.Subscriber('robot_manipulator_goal', Point, positonToAngle)

	pub = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		pub.publish(angulo)
		rate.sleep()
if __name__ == '__main__':
	plannerCamera()
