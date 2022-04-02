#! /usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtle_bot_3.srv import cambiar_nombre

lin_vel = 0
rot_vel= 0
def callback(request):
	global lin_vel
	global rot_vel

	pullData = open("./src/turtle_bot_3/results/"+ str(request.nombre_archivo)+".txt").read()
	dataList = pullData.split('\n')
	finalAction = False
	vel = Twist()

	#Toma los primeros dos valores del txt para tomar las velocidades agular y lineal
	lin_vel = float(dataList[0])
	rot_vel = float(dataList[1])

	for eachLine in dataList:
		if len(eachLine) > 1 and finalAction ==False:
			if eachLine == "'w'":
			    vel.linear.x = lin_vel
			    vel.angular.z = 0 
				

			elif eachLine == "'s'":
				vel.linear.x = -lin_vel
				vel.angular.z = 0

			elif eachLine == "'d'":
				vel.linear.x = 0
				vel.angular.z = rot_vel
				

			elif eachLine == "'a'":
				vel.linear.x = 0
				vel.angular.z = -rot_vel

			elif eachLine =="'g'":
				mov = 0
				finalAction = True
				break
			else:
				vel.linear.x = 0
				vel.angular.z = 0

		
		rate = rospy.Rate(20)
		sendMov.publish(vel)
		rate.sleep()
		#print("%s---%s"%(mov_rot,mov_lin))
		#mov_lin = 0
		#mov_rot = 0
	vel.linear.x = 0
	vel.angular.z = 0
	sendMov.publish(vel)
	




def change_name_server():
	global sendMov
	rospy.init_node("turtlebot_player")
	sendMov = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 1)
	service = rospy.Service('cambiar_nombre', cambiar_nombre, callback)
	print('listo para recibir nombre')
	rospy.spin()


if __name__ == '__main__':
	change_name_server()
