#! /usr/bin/env python3
import rospy
from pynput import keyboard
from std_msgs.msg import Int8

'''
Las teclas que se usaran para mover el robot son las siguientes:
Tecla W => Adelante
Tecla S => Atras
Tecla A => Girar 90 grados a izquierda
Tecla d => Girar 90 grados a la derecha
'''
#lin_vel_input = input("Ingrese la velocidad velocidad lineal: ") 
#rot_vel_input = input("Ingrese la velocidad angular: ")
mov_actual = 0
pressW = False
pressS = False
pressA = False
pressD = False

#Se crea un archivo .txt en donde se guardara el recorrido realizado por las teclas
#file = open ("./src/turtle_bot_3/results/info_recorrido.txt", 'w')
#file.close()




#Esta funcion publica en el nodo turtlebot_cmdVel el movimiento cuando se presiona una tecla
def on_press(key):

	global mov_actual
	global pressW
	global pressS
	global pressA
	global pressD
	

	if key == keyboard.KeyCode.from_char('w'):
		mov_actual = 1
		pressW = True

	elif key == keyboard.KeyCode.from_char('s'):
		mov_actual = 2
		pressS = True

	elif key == keyboard.KeyCode.from_char('a'):
		mov_actual = 3
		pressD = True

	elif key == keyboard.KeyCode.from_char('d'):
		mov_actual = 4
		pressA = True

	else:
		mov_actual = 0



	#Esta parte del código llena el archivo.txt con las teclas que se presionaron
	#keydata = str(key)
	#flag = True
	#if keydata != 'g' and flag == True:
		#with open("./src/turtle_bot_3/results/info_recorrido.txt", "a") as f:
			#f.write(keydata + '\n')
	#else:
		#flag = False
		#f.close()

	#Crea un objeto de tipo Twist para poder asignar a cada vector la velocidad deseada
	var = Int8()
	var = mov_actual
	#Publica el formato Twist al nodo 
	sendMov = rospy.Publisher('topic_prueba', Int8, queue_size = 10)
	sendMov.publish(var)



#Esta funcion publica el estado de reposo cuando se deja de presionar una tecla
def on_release(key):
	global mov_actual
	global pressW
	global pressS
	global pressA
	global pressD

	pressW = False
	pressS = False
	pressA = False
	pressD = False
	mov_actual = 0

	var = Int8()
	var = mov_actual
	sendMov = rospy.Publisher('topic_prueba', Int8, queue_size = 10)
	sendMov.publish(var)



#Esta funcion junta las acciones de presionar y soltar con la funcion de leer teclado
def teclas():
	with keyboard.Listener(on_press = on_press, on_release = on_release) as listen:
		listen.join()


#Esta funcion es la que va a crear el nodo y va a publicar en el topico basadose en las funciones anteriormente creadas
def publicar_mov():
	global mov_actual
	rospy.init_node('turtlebot_teleop')
	pub = rospy.Publisher('topic_prueba', Int8, queue_size = 10)
	rate = rospy.Rate(10)
	var = Int8()
	while not rospy.is_shutdown():
		var = mov_actual
		#print(mov_actual)
		#print(rot_actual)
		pub.publish(var)
		teclas()		
		rate.sleep()
		
		#file.close()






if __name__ == '__main__':
	try:
		publicar_mov()
	except rospy.ROSInterruptException:
		pass
