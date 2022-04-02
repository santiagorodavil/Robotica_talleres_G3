#! /usr/bin/env python3
import rospy
from std_msgs.msg import Int8
from turtle_bot_3.srv import cambiar_nombre

mov = 0
sendMov = ""
def callback(request):
	global mov
	global sendMov

	pullData = open("./src/turtle_bot_3/results/"+ str(request.nombre_archivo)+".txt").read()
	dataList = pullData.split('\n')
	finalAction = False

	#Toma los primeros dos valores del txt para tomar las velocidades agular y lineal
#	vel_lin = float(dataList[0])
#	vel_rot = float(dataList[1])

	for eachLine in dataList:
		if len(eachLine) > 1 and finalAction ==False:
			if eachLine == "'w'":
				mov = 1

			elif eachLine == "'s'":
				mov = 2

			elif eachLine == "'d'":
				mov = 3

			elif eachLine == "'a'":
				mov = 4

			elif eachLine =="'g'":
				mov = 0
				finalAction = True
				break
			else:
				mov = 0

		velocidad = mov
		rate = rospy.Rate(20)
		sendMov.publish(velocidad)
		rate.sleep()
		#print("%s---%s"%(mov_rot,mov_lin))
		#mov_lin = 0
		#mov_rot = 0
	velocidad = 0
	sendMov.publish(velocidad)
	




def change_name_server():
	global sendMov
	rospy.init_node("turtlebot_player")
	sendMov = rospy.Publisher('turtlebot_cmdVel', Int8, queue_size = 1)
	service = rospy.Service('cambiar_nombre', cambiar_nombre, callback)
	print('listo para recibir nombre')
	rospy.spin()


if __name__ == '__main__':
	change_name_server()
