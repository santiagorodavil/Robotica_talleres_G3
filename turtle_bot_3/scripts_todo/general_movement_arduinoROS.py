#! /usr/bin/env python3
import rospy
from pynput import keyboard
from geometry_msgs.msg import Twist

'''
Las teclas que se usaran para mover el robot son las siguientes:
Tecla W => Adelante
Tecla S => Atras
Tecla A => Girar 90 grados a izquierda
Tecla d => Girar 90 grados a la derecha
'''
lin_input = input("Ingrese la velocidad velocidad lineal: ") 
rot_input = input("Ingrese la velocidad angular: ")
lin_vel_input = float(lin_input)
rot_vel_input = float(rot_input)
velocidad = Twist()
pressW = False
pressS = False
pressA = False
pressD = False

#Se crea un archivo .txt en donde se guardara el recorrido realizado por las teclas
file = open ("./src/turtle_bot_3/results/info_recorrido.txt", 'w')
file.close()




#Esta funcion publica en el nodo turtlebot_cmdVel el movimiento cuando se presiona una tecla
def on_press(key):

	global lin_vel_input
	global rot_vel_input
	global pressW
	global pressS
	global pressA
	global pressD
	global velocidad
	
	
	if key == keyboard.KeyCode.from_char('w'):
		velocidad.linear.x = lin_vel_input
		velocidad.angular.z = 0
		pressW = True

	elif key == keyboard.KeyCode.from_char('s'):
		velocidad.linear.x = -lin_vel_input
		velocidad.angular.z = 0
		pressS = True

	elif key == keyboard.KeyCode.from_char('a'):
		velocidad.linear.x = 0
		velocidad.angular.z = rot_vel_input
		pressD = True

	elif key == keyboard.KeyCode.from_char('d'):
		velocidad.linear.x = 0
		velocidad.angular.z = -rot_vel_input
		pressA = True

	else:	
		velocidad.linear.x = 0
		velocidad.angular.z = 0



	#Esta parte del código llena el archivo.txt con las teclas que se presionaron
	keydata = str(key)
	flag = True
	if keydata != 'g' and flag == True:
		with open("./src/turtle_bot_3/results/info_recorrido.txt", "a") as f:
			f.write(keydata + '\n')
	else:
		flag = False
		f.close()

	
	#Publica el formato Twist al nodo 
	#print(velocidad)
	sendMov = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion publica el estado de reposo cuando se deja de presionar una tecla
def on_release(key):
	global pressW
	global pressS
	global pressA
	global pressD
	global velocidad
	pressW = False
	pressS = False
	pressA = False
	pressD = False
	velocidad.linear.x = 0
	velocidad.angular.z = 0
	#print("puse0")
	sendMov = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion junta las acciones de presionar y soltar con la funcion de leer teclado
def teclas():
	with keyboard.Listener(on_press = on_press, on_release = on_release) as listen:
		listen.join()


#Esta funcion es la que va a crear el nodo y va a publicar en el topico basadose en las funciones anteriormente creadas
def publicar_mov():
	global lin_vel_input
	global rot_vel_input
	global velocidad
	rospy.init_node('turtlebot_teleop')
	pub = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	rate = rospy.Rate(10)
	#vel = Twist()
	while not rospy.is_shutdown():
		velocidad.linear.x = lin_vel_input
		velocidad.angular.z = rot_vel_input
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

