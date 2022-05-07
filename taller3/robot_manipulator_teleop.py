#! /usr/bin/env python3
import rospy
from pynput import keyboard
from geometry_msgs.msg import Twist

'''
Las teclas que se usaran para mover el robot son las siguientes:
Tecla U => Giro + servo1
Tecla J => Giro - servo1
Tecla I => Giro + servo2
Tecla K => Giro - servo2
Tecla O => Giro + servo3
Tecla L => Giro - servo3
Tecla P => Giro + servo4
Tecla Ñ => Giro - servo4
'''
lin_input1 = input("Ingrese la velocidad servo 1: ")
lin_input2 = input("Ingrese la velocidad servo 2: ") 
lin_input3 = input("Ingrese la velocidad servo 3: ") 
lin_input4 = input("Ingrese la velocidad servo 4: ")
lin_vel_input1 = float(lin_input1)
lin_vel_input2 = float(lin_input2)
lin_vel_input3 = float(lin_input3)
lin_vel_input4 = float(lin_input4) 
angle_servo1= 0
angle_servo2= 0
angle_servo3= 0
angle_servo4= 0
#rot_input = input("Ingrese la velocidad angular: ")
#rot_vel_input = float(rot_input)
velocidad = Twist()
pressU = False
pressJ = False
pressI = False
pressK = False
pressO = False
pressL = False
pressP = False
pressÑ = False

#Se crea un archivo .txt en donde se guardara el recorrido realizado por las teclas
#file = open ("./src/turtle_bot_3/results/info_recorrido.txt", 'w')
#file.write(str(lin_input)+'\n')
#file.write(str(rot_input)+'\n')
#file.close()




#Esta funcion publica en el nodo turtlebot_cmdVel el movimiento cuando se presiona una tecla
def on_press(key):

	global lin_vel_input1
	global lin_vel_input2
	global lin_vel_input3
	global lin_vel_input4
	global angle_servo1
	global angle_servo2
	global angle_servo3
	global angle_servo4
	#global rot_vel_input
	global pressU
	global pressJ
	global pressI
	global pressK
	global pressO
	global pressL
	global pressP
	global pressÑ
	global velocidad
	
	
	if key == keyboard.KeyCode.from_char('u'):
		if angle_servo1 < 180:
			angle_servo1 = angle_servo1+(1*lin_vel_input1)
			if angle_servo1 >= 180:
				angle_servo1 = 180
		else:
			angle_servo1 = 180
		velocidad.linear.x = angle_servo1
		pressU = True

	elif key == keyboard.KeyCode.from_char('j'):
		if angle_servo1 > 0:
			angle_servo1 = angle_servo1-(1*lin_vel_input1)
			if angle_servo1 <= 0:
				angle_servo1 = 0
		else:
			angle_servo1 = 0
		velocidad.linear.x = angle_servo1
		pressJ = True

	elif key == keyboard.KeyCode.from_char('i'):
		if angle_servo2 < 180:
			angle_servo2 = angle_servo2+(1*lin_vel_input2)
			if angle_servo2 >= 180:
				angle_servo2 = 180
		else:
			angle_servo2 = 180
		velocidad.linear.y = angle_servo2
		pressI = True

	elif key == keyboard.KeyCode.from_char('k'):
		if angle_servo2 > 0:
			angle_servo2 = angle_servo2-(1*lin_vel_input2)
			if angle_servo2 <= 0:
				angle_servo2 = 0
		else:
			angle_servo2 = 0
		velocidad.linear.y = angle_servo2
		pressK = True

		
	elif key == keyboard.KeyCode.from_char('o'):
		if angle_servo3 < 180:
			angle_servo3 = angle_servo3+(1*lin_vel_input3)
			if angle_servo3 >= 180:
				angle_servo3 = 180
		else:
			angle_servo3 = 180
		velocidad.linear.z = angle_servo3
		pressO = True

	elif key == keyboard.KeyCode.from_char('l'):
		if angle_servo3 > 0:
			angle_servo3 = angle_servo3-(1*lin_vel_input3)
			if angle_servo3 <= 0:
				angle_servo3 = 0
		else:
			angle_servo3 = 0
		velocidad.linear.z = angle_servo3
		pressL = True

	elif key == keyboard.KeyCode.from_char('p'):
		if angle_servo4 < 180:
			angle_servo4 = angle_servo4+(1*lin_vel_input4)
			if angle_servo4 >= 180:
				angle_servo4 = 180
		else:
			angle_servo4 = 180
		velocidad.angular.x = angle_servo4
		pressP = True

	elif key == keyboard.KeyCode.from_char('ñ'):
		if angle_servo4 > 0:
			angle_servo4 = angle_servo4-(1*lin_vel_input4)
			if angle_servo4 <= 0:
				angle_servo4 = 0
		else:
			angle_servo4 = 0
		velocidad.angular.x = angle_servo4
		pressÑ = True

	else:	
		velocidad.linear.x = angle_servo1
		velocidad.linear.y = angle_servo2
		velocidad.linear.z = angle_servo3
		velocidad.angular.x = angle_servo4




	#Esta parte del código llena el archivo.txt con las teclas que se presionaron


	
	#Publica el formato Twist al nodo 
	#print(velocidad)
	sendMov = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion publica el estado de reposo cuando se deja de presionar una tecla
def on_release(key):
	global pressU
	global pressJ
	global pressI
	global pressK
	global pressO
	global pressL
	global pressP
	global pressÑ
	global velocidad
	pressU = False
	pressJ = False
	pressI = False
	pressK = False
	pressO = False
	pressL = False
	pressP = False
	pressÑ = False
	velocidad.linear.x = angle_servo1
	velocidad.linear.y = angle_servo2
	velocidad.linear.z = angle_servo3
	velocidad.angular.x = angle_servo4
	#print("puse0")
	sendMov = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion junta las acciones de presionar y soltar con la funcion de leer teclado
def teclas():
	with keyboard.Listener(on_press = on_press, on_release = on_release) as listen:
		listen.join()


#Esta funcion es la que va a crear el nodo y va a publicar en el topico basadose en las funciones anteriormente creadas
def publicar_mov():
	global angle_servo1
	global angle_servo2
	global angle_servo3
	global angle_servo4
	#global rot_vel_input
	global velocidad
	rospy.init_node('turtlebot_teleop')
	pub = rospy.Publisher('robot_manipulator_angles', Twist, queue_size = 10)
	rate = rospy.Rate(10)
	#vel = Twist()
	set_vel = Twist()
	while not rospy.is_shutdown():
		velocidad.linear.x = angle_servo1
		velocidad.linear.y = angle_servo2
		velocidad.linear.z = angle_servo3
		velocidad.angular.x = angle_servo4
		#print(mov_actual)
		#print(rot_actual)
		pub.publish(velocidad)
		teclas()		
		rate.sleep()
		
		#file.close()






if __name__ == '__main__':
	try:
		publicar_mov()
	except rospy.ROSInterruptException:
		pass

