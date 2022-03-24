#! /usr/bin/env python3
import rospy
from pynput import keyboard
import math as m
from geometry_msgs.msg import Twist

'''
Las teclas que se usaran para mover el robot son las siguientes:
Tecla W => Adelante
Tecla S => Atras
Tecla A => Girar 90 grados a izquierda
Tecla d => Girar 90 grados a la derecha
'''
lin_vel_input = input("Ingrese la velocidad velocidad lineal: ") 
rot_vel_input = input("Ingrese la velocidad angular: ")
mov_actual = [0.0]
rot_actual = [0.0]
pressW = False
pressS = False
pressA = False
pressD = False

#Se crea un archivo .txt en donde se guardara el recorrido realizado por las teclas
file = open ("./src/turtle_bot_3/results/info_recorrido.txt", 'w')
file.close()



# Esta función asigna los valores  de velocidad que tomara el robot cuando se vaya a mover
def movimiento(num):
	'''
	Significado cada valor de num:
	num = 0 => TurtleBot en reposo
	num = 1 => TurtleBot avanza hacia adelante
	num = 2 => TurtleBot avanza hacia atrás
	num = 3 => TurtleBot gira 90 grados a la derecha
	num = 4 => Turtlebot gira 90 grados a la izquierda	 
	'''
	global mov_actual
	global lin_vel_input
	
	if num == 0:
		mov_actual = [0.0]

	elif num == 1:
		mov_actual = [float(lin_vel_input)]

	elif num == 2:
		mov_actual = [-(float(lin_vel_input))]

	elif num == 3:
		mov_actual = [0.0] 

	elif num == 4:
		mov_actual = [0.0] 

	else:
		mov_actual = [0.0]

	return mov_actual

# Esta función asigna los valores  de velocidad angular que tomara el robot cuando se vaya a mover
def rotacion(num):
	global rot_actual
	global rot_vel_input
	'''
	Significado cada valor de num:
	num = 0 => TurtleBot en reposo
	num = 1 => TurtleBot avanza hacia adelante
	num = 2 => TurtleBot avanza hacia atrás
	num = 3 => TurtleBot gira 90 grados a la derecha
	num = 4 => Turtlebot gira 90 grados a la izquierda	 
	'''
	if num == 0:
		rot_actual = [0.0]

	elif num == 1:
		rot_actual = [0.0]

	elif num == 2:
		rot_actual = [0.0]

	elif num == 3:
		rot_actual = [-(float(rot_vel_input))]  

	elif num == 4:
		rot_actual = [float(rot_vel_input)] 

	else:
		rot_actual = [0.0]

	return rot_actual

#Esta funcion publica en el nodo turtlebot_cmdVel el movimiento cuando se presiona una tecla
def on_press(key):

	global mov_actual
	global rot_actual
	global pressW
	global pressS
	global pressA
	global pressD
	

	if key == keyboard.KeyCode.from_char('w'):
		mov_actual = movimiento(1)
		rot_actual = rotacion(1)
		pressW = True

	elif key == keyboard.KeyCode.from_char('s'):
		mov_actual = movimiento(2) 
		rot_actual =rotacion(2)
		pressS = True

	elif key == keyboard.KeyCode.from_char('d'):
		mov_actual = movimiento(3)
		rot_actual = rotacion(3)
		pressD = True

	elif key == keyboard.KeyCode.from_char('a'):
		mov_actual = movimiento(4)
		rot_actual = rotacion(4)
		pressA = True

	else:
		mov_actual = movimiento(0)
		rot_actual = rotacion(0)



	#Esta parte del código llena el archivo.txt con las teclas que se presionaron
	keydata = str(key)
	flag = True
	if keydata != 'g' and flag == True:
		with open("./src/turtle_bot_3/results/info_recorrido.txt", "a") as f:
			f.write(keydata + '\n')
	else:
		flag = False
		f.close()

	#Crea un objeto de tipo Twist para poder asignar a cada vector la velocidad deseada
	velocidad = Twist()
	velocidad.linear.x = mov_actual[0]
	velocidad.angular.z = rot_actual[0]

	#Publica el formato Twist al nodo 
	sendMov = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion publica el estado de reposo cuando se deja de presionar una tecla
def on_release(key):
	global mov_actual
	global rot_actual
	global pressW
	global pressS
	global pressA
	global pressD

	pressW = False
	pressS = False
	pressA = False
	pressD = False
	mov_actual = movimiento(0)
	rot_actual = rotacion(0)

	velocidad = Twist()
	velocidad.linear.x = mov_actual[0]
	velocidad.angular.z = rot_actual[0]

	sendMov = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	sendMov.publish(velocidad)



#Esta funcion junta las acciones de presionar y soltar con la funcion de leer teclado
def teclas():
	with keyboard.Listener(on_press = on_press, on_release = on_release) as listen:
		listen.join()

def escribirArchivo(key):
	keydata = str(key)
	flag = True
	if keydata != 'g' and flag == True:
		with open("./src/turtle_bot_3/scripts/info_recorrido.txt", "a") as f:
			f.write(keydata + '\n')
		f.close()
	else:
		flag = False
		f.close()

#Esta funcion es la que va a crear el nodo y va a publicar en el topico basadose en las funciones anteriormente creadas
def publicar_mov():
	global mov_actual
	global rot_actual
	rospy.init_node('turtlebot_teleop')
	pub = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size = 10)
	rate = rospy.Rate(10)
	velocidad = Twist()
	while not rospy.is_shutdown():
		velocidad.linear.x = mov_actual[0]
		velocidad.angular.z = rot_actual[0]	
		#print(mov_actual)
		#print(rot_actual)
		pub.publish(velocidad)		
		rate.sleep()
		teclas()
		file.close()






if __name__ == '__main__':
	try:
		publicar_mov()
	except rospy.ROSInterruptException:
		pass
