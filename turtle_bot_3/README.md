# Taller 2 Robótica
*** Grupo 3 ***

Dentro de este README se encontraráun paso a paso de cómo probar el funcionamiento de nuestro taller 2. Este taller se divide en 4 puntos, cabe resaltar que **todos los puntos deben ejectuarse desde el *workspace* donde se encuentre el taller**.  Otra cosa que se debe tener en cuenta es que ahora se van a depender del hardware del robot.


[TOC]




Antes que nada, es necesario descargar ciertas dependecias para que pueda funcionar el proyecto:

#### Dependencias 
---
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

Luego de descargar todas las dependecias es posible seguir con el desarrollo del taller.

Iniciar robot
---
Para iniciar el robot se deben hacer los siguientes pasos:
Iniciar roscore:

`$  roscore`

En otra terminal iniciar el ROSserial:

`$  rosrun rosserial_pyhton serial_node <Nombre del puerto del aruino>`

Donde se debe reemplazar <Nombre del puerto del arduino> por el que corresponda. Para verificar que el proceso se hizo correctamente se puede ejecutar en una terminal `$ rostopic list`. Y deberían aparecer los tópicos /turtlebot_position y /turtlebot_cmdVel


Desarrollo del taller
---

##### Punto 1
En este punto se pedía crear un nodo llamado *general_movemet_send_vel* en donde se le pudiera ingresar la velocidad lineal y angular deseada para mover al robot.

Estando en una terminal se entrará en el ws y se ejecutarán las siguientes líneas:

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  general_movemet_send_vel.py`

Acto seguido, debe aparecer en la terminal lo siguiente:

`Ingrese la velocidad velocidad lineal: `

`Ingrese la velocidad angular: `

Como se indica, en cada espacio se debe ingresar la velocidad lineal y angular y presionar la tecla enter.

Luego de esto ya debería ser posible presionar las teclas *a, s, d, w *   para mover al robot de la simulación y se daría por terminado el punto 1. 


##### Punto 2
Para este punto se pedía crear un nodo llamado *Turtle_bot_interface* , en donde se pueda ver en tiempo real la posición del robot.  Esto debe poder verse dentro de una interfaz y poder guardar como una imagen el recorrido del robot.
  
Para esto se debe hacer lo siguiente en una terminal nueva (cabe resaltar que la terminal debe estar en el ws):

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  odometria.py`  

Para esto se debe hacer lo siguiente en una terminal nueva (cabe resaltar que la terminal debe estar en el ws):

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  turtlebot_interface.py`

Luego de esto, debería aparecer una interfaz con 3 botones: *Guardar recorrido*, *Usar recorrido guardado*  y  *pagina de grafica*.

Si se presiona el botón de "página de gráfica" debería aparecer la gráfica en donde se muestra la posición actual del robot. Esta gráfica tiene la opción de poder guardar la imagen del recorrido que se realizó desde el momento que se inició la interfaz hasta el momento en el que se guarda la imagen. Por lo que se puede decir que se daría por terminado el punto 2.


##### Punto 3
Lo que se pedía para este punto era modificar los nodos ateriormente creados para guardar el recorrido que realizó  en robot dentro de un archivo *.txt*. Cabe aclarar que el nobre del archivo se le pedirá al usuario y este archivo se guardará dentro de la carpeta  **results** que se encuentra dentro del paquete *turtle_bot_3*.

**Importante:** es necesario que cuando se vaya a correr este punto (en general, todos los puntos), se encuentre la terminal en el *workspace* donde se encuentra el paquete.

Teniendo en cuenta lo anterior, si aún no se han cerrado las terminales de *general_movemet_send_vel.py* y *Turtle_bot_interface*, diríjase a la ventana de la interfaz. En caso de que se hayan detenido los procesos, repita los pasos de los puntos 1 y 2.

Ahora que se está en la interfaz, lo que se debe hacer ahora es presionar el botón de "Guardar recorrido", una vez presionado aparecerán otros dos botones. Si desea guardar el archivo, presione el botón que diga "Guardar archivo" y en la ventana que surge escriba el nombre con el cual quiere guardar el archivo del recorrido.

Finalmente, para revisar si se guardó el recorrido con el nombre deseado puede dirijirse a la carpeta de **results** y verificar si allí se encuentra el documento. 


Teniendo en cuenta TODAS las advertencias y notas que se plantean se puede dar por terminado el punto 3.



##### Punto 4
Para este punto se pedía hacer un nodo llamado *turtle_bot_player* el cual recibirá como parámetro el nombre de un archivo donde se encuentren las acciones del robot.

En la terminal, estando en el ws donde se encuentra el paquete se debe colocar lo siguiente:

`$  source devel/setup.bash`

`$  rosrun turtle_bot_3  turtlebot_player.py`

Acto seguido, dentro de esa terminal debería aparecer un mensaje que dice lo siguiente:

`Listo para recibir nombre`

Cuando esto aparezca dentro de la termial,  en una nueva terminal se debe ejecutar lo siguiente:

`$  source devel/setup.bash`

`$ rosservice call /cambiar_nombre <nombre_archivo>`

Donde "nombre_archivo" sería el nombre del archivo que se quiere correr. Cabe resaltar que este nombre archivo va a ser **únicamente** lo que se escribió a la hora de guardar el archivo en el punto 3. Es decir, **NO** se debe añadir ni *.txt* ni la ruta completa del archivo para que este funcione. Únicamente el nombre del archivo que se quiere correr y luego presionar la tecla enter.

**NOTA:** Es posible utilizar cualquier archivo que cumpla con la misma estructura que tiene el archivo que se guardó en la interfaz. Pero es **importante** que dicho archivo se encuentre dentro de la carpeta **results**, esto para que el programa pueda reconocer el archivo.



Por último, cabe aclarar que cuado se ejecute el último comando realizado (rosservice call), este pueda mostrar un error en la terminal. Dicho error es irrelevante debido a que no obstruye el funcionamiento del nodo. Por lo que se puede dar por terminado el cuarto y el último punto del taller.
