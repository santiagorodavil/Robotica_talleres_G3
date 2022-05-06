# Taller 3 Robótica
*** Grupo 3 ***

Dentro de este README se encontraráun paso a paso de cómo probar el funcionamiento de nuestro taller 2. Este taller se divide en 4 puntos, cabe resaltar que **todos los puntos deben ejectuarse desde el *workspace* donde se encuentre el taller**.  Otra cosa que se debe tener en cuenta es que ahora se van a depender del hardware del robot.


[TOC]




Las siguientes dependencias son necesarias para el funcionamiento del proyecto:

#### Dependencias 
---
Si se está corriendo desde Ubuntu 20.04, omitir el siguiente comando. De lo contrario, correr el comando:

`$ sudo apt install python3-opencv `

Para esto basta solo con copiar y pegar los comandos a continuación en una terminal de comandos:
**pip**

`$ sudo apt-get -y install python3-pip  `

**Matplotlib**

`$ pip3 install matplotlib  `

O también se puede

`$   sudo apt-get install python3-matplotlib`

**Pynput**

`$ python -m pip install pynput  `

**tkinter**

`$ sudo apt install python-tk  `

**rosserial**

`$ sudo apt-get install ros-noetic-rosserial-arduino  `
`$ sudo apt-get install ros-noetic-rosserial  `


Adicionalmente, es necesario descargar la libreria de ros para el entorno arduino:
`$ cd Arduino/libraries  `
`$ rm -rf ros_lib `
`$ rosrun rosserial_arduino make_libraries.py  `
Donde "Arduino" es la carpeta que se crea por defecto en el directorio de inicio

Para vincular la cámara web en conexión SSH se deben correr los comandos:
  
  `$ sudo apt install ros-noetic-usb-cam `

Luego de descargar todas las dependecias es posible seguir con el desarrollo del taller.

Iniciar robot
---
Para iniciar el robot se deben hacer los siguientes pasos:

Iniciar roscore:

`$  roscore`

En otra terminal iniciar el ROSserial:

`$  rosrun rosserial_pyhton serial_node <Nombre del puerto del arduino>`

Donde se debe reemplazar <Nombre del puerto del arduino> por el que corresponda. Para verificar que el proceso se hizo correctamente se puede ejecutar en una terminal `$ rostopic list`. Y deberían aparecer los tópicos /turtlebot_position y /turtlebot_cmdVel. Si se desea disminuir los recursos de operación de la Raspberry, se puede iniciar una conexión SSH entre un computador (master) y la Raspberry (slave) conociendo la dirección IP de cada dispositivo y configurandolo como se describe en el siguiente video: https://www.youtube.com/watch?v=StHfHCPrHOw&list=LL&index=1. 
  
Antes de correr los archivos cuando se requiera la cámara (puntos 3 y 4) se debe ejecutar roscore en el master:
  
`$  roscore `
  
En slave se debe correr el comando:
  
 `$  roslaunch usb_cam usb_cam-test.launch `

Desarrollo del taller
---

##### Punto 1
 
  Este punto pide crear un nodo llamado /robot_manipulator_teleop, el cual permite al usuario controlar el manipulador sobre el robot con las velocidades de cada una de las junturas que tiene el manipulador (entran por parámetro del usuario) con las teclas del computador. Si no se presiona ninguna tecla el robot se debe quedar quieto. 
  
Estando en una terminal se entrará en el ws y se ejecutarán las siguientes líneas:

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  robot_manipulator_teleop.py`

Acto seguido, debe aparecer en la terminal lo siguiente:

`Ingrese la velocidad servo 1: `

`Ingrese la velocidad servo 2: `
 
`Ingrese la velocidad servo 3: `
  
`Ingrese la velocidad servo 4: `
  

Como se indica, en cada espacio se debe ingresar la velocidad lineal deseada para cada servomotor seguido de la tecla enter.

Luego de esto ya debería ser posible presionar las teclas *u, j, i, k, o, l p, ñ* para mover el manipulador. Las parejas de comandos corresponden a movimientos hacia un lado y otro de los servos. Los servos están ubicados en la junturas del manipulador y la velocidad de cada juntura está en el marco de referencia local de cada una de ellas al iniciar el nodo. 


##### Punto 2
Para este punto se pedía crear un nodo llamado *robot_manipulator_interface3d*, en donde se pueda ver en tiempo real la posición del end-effector del manipulador.  Esto debe poder verse dentro de una interfaz y poder guardar como una imagen el recorrido del robot. Se presenta en tiempo real en el marco global de referencia. Además, muestra el camino recorrido por el mismo desde donde inició. La interfaz cuenta con el espacio para asignarle un nombre a la gráfica y poderlo guardar en el directorio deseado, al finalizar el recorrido.
  
Para esto se debe hacer lo siguiente en una terminal nueva (cabe resaltar que la terminal debe estar en el ws):

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  robot_manipulator_odometry.py`  

Para esto se debe hacer lo siguiente en una terminal nueva (cabe resaltar que la terminal debe estar en el ws):

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  robot_manipulator_interface3d.py`

Luego de esto, debería aparecer una interfaz con 3 botones: *Guardar recorrido*, *Usar recorrido guardado*  y  *pagina de gráfica*.

Si se presiona el botón de "página de gráfica" debería aparecer la gráfica en donde se muestra la posición actual del robot. Esta gráfica tiene la opción de poder guardar la imagen del recorrido que se realizó desde el momento que se inició la interfaz hasta el momento en el que se guarda la imagen.


##### Punto 3
 
Este punto pide crear un nodo en ROS, llamado */robot_manipulator_planner*, que permita a un usuario llevar el end-effector del robot a una posición destino deseada dentro de su volumen de trabajo. Se realiza el cálculo de cinemática inversa o de planeación de trayectorias para alcanzar esta posición. La posición a alcanzar será publicada en el tópico llamado: */robot_manipulator_goal* .
  
**Importante:** es necesario que cuando se vaya a correr este punto (en general, todos los puntos), se encuentre la terminal en el *workspace* donde se encuentra el paquete.

Teniendo en cuenta lo anterior, si aún no se han cerrado las terminales de *general_movemet_send_vel.py* y *robot_manipulator3dbot_interface*, diríjase a la ventana de la interfaz. En caso de que se hayan detenido los procesos, repita los pasos de los puntos 1 y 2.
************** COMPLETAR

##### Punto 4
Para este punto se pedía hacer un nodo llamado *robot_manipulator_ping_pong* el cual permite, a través de este tópico, tomar un ping pong del color especificado.
 
