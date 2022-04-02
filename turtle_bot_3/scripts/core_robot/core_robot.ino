#include <ros.h>
#include <geometry_msgs/Pose2D.h>
#include <geometry_msgs/Twist.h>
//#include <std_msgs/Int8.h>
#include <math.h>                                        // necesaria para utilizar función atan()
#define PI 3.1415926535897932384626433832795     


/*******************************************************************************
 ***      Se dividira el codigo en dos partes principales:                   ***
 ***        - Uso de los encoders                                            ***
 ***        - Movimiento de los motores                                      ***
 *******************************************************************************
 */






/*********************************************************************************************************************************************************************
 ******************************************************** Aqui va todo lo de los encoders y odometria ****************************************************************
 *********************************************************************************************************************************************************************
 */

 int N = 20;                                              // nùmero de ranuras del encoder
float diametro = 6.8;                                    // diametro de la llanta cm
float longitud = 13.4;                                   // longitud del robot entre llantas
int contadorTicks = 1;                                  // número de ticks para cálculo de velocidad (recordar que entre menor sea el valor mayor ruido de la medida)
int tam = 10;                                           // tamaño del vector del calculo de promedio (Este valor depende del tamaño de los vectores de promedio vectorL y vectorR)
int k = 10;                                             // tiempo de muestreo

float Cdistancia = 0;                                   // distancia recorrido punto central
float x = 0;                                            // distancia recorrida eje X
float y = 0;                                            // distancia recorrida eje Y
float phi = 0;                                          // posición angular

volatile unsigned muestreoActual = 0;                     // variables para definiciòn del tiempo de muestreo
volatile unsigned muestreoAnterior = 0;
volatile unsigned deltaMuestreo = 0;

///------------------------------- Variables de motor derecho---------------------------------------------

volatile unsigned muestreoActualInterrupcionR = 0;        // variables para definiciòn del tiempo de interrupciòn y calculo de la velocidad motor derecho
volatile unsigned muestreoAnteriorInterrupcionR = 0;
double deltaMuestreoInterrupcionR = 0;

int encoderR = 3;   // pin de conexiòn del encoder derecho

double frecuenciaR = 0;                                  // frecuencia de interrupciòn llanta R
double Wr = 0;                                           // Velocidad angular R
double Vr = 0;                                           // velocidad Lineal
int CR = 0;                                             // contador ticks
float vectorR[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};    // vector de almacenamiento de datos para promedio del tiempo de interrupciones

float Rdistancia = 0;                                    // distancia recorrida llanta derecha
int Rtick = 0;                                           // ticks del encoder derecho
int RtickAnt = 0;                                        // ticks del encoder derecho anteriores
int deltaRtick = 0;                                      // diferencia del encoder derecho

//------------------------------  Variables de motor Izquierdo ------------------------------------------------

volatile unsigned muestreoActualInterrupcionL = 0;        // variables para definiciòn del tiempo de interrupciòn y calculo de la velocidad motor Izquierdo
volatile unsigned muestreoAnteriorInterrupcionL = 0;
double deltaMuestreoInterrupcionL = 0;

int encoderL = 2;   // pin de conexiòn del encoder Izquierdo

double frecuenciaL = 0;                                  // frecuencia de interrupciòn llanta Izquierda
double Wl = 0;                                           // Velocidad angular L
double Vl = 0;                                           // velocidad Lineal
int CL = 0;                                              // contador Ticks
float vectorL[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};    // vector de almacenamiento de datos para promedio del tiempo de interrupciones

float Ldistancia = 0;                                    // distancia recorrida llanta izquierda
int Ltick = 0;                                           // ticks del encoder izquierdo
int LtickAnt = 0;                                        // ticks del encoder izquier anteriores
int deltaLtick = 0;                                      // diferencia del encoder izquierdo




/*********************************************************************************************************************************************************************
 ******************************************************** Aqui va todo lo de movimiento los motores ******************************************************************
 *********************************************************************************************************************************************************************
 */

// Motor A Derecho
int ENA = 10;
int IN1 = 9;
int IN2 = 8;
float lin_vel = 0.0;
float rot_vel = 0.0;
int analog_vel = 0;
int analog_rot = 0;
// Motor B Izquierdo
int ENB = 5;
int IN3 = 7;
int IN4 = 6;
int lin_vel_l = 0;
int rot_vel_l = 0;

/*********************************************************************************************************************************************************************
 *************************************************************** Aqui va todo lo de ROS ******************************************************************************
 *********************************************************************************************************************************************************************
 */

ros::NodeHandle  nh;


void messageCb( const geometry_msgs::Twist& cmd_vel){
  //conversion del input velocidad a analogo. Valor max 180, valor min 80
  lin_vel = (((cmd_vel.linear.x)*100)/10);
  rot_vel = (((cmd_vel.angular.z)*100)/10);

  //Asigna valor analogo para motores y da direcciones 
  //Adelante
  if(lin_vel > 0){
     //Direccion motor A   Derecho
     digitalWrite (IN1, HIGH);
     digitalWrite (IN2, LOW);
     analogWrite (ENA, (int)lin_vel +110); //Velocidad motor A
     //Direccion motor B Izquierdo
     digitalWrite (IN3, HIGH);
     digitalWrite (IN4, LOW);
     analogWrite (ENB, (int)lin_vel+95); //Velocidad motor B
  }
  //Atras
  else if(lin_vel < 0){
     //Direccion motor A   Derecho
     digitalWrite (IN1, LOW);
     digitalWrite (IN2, HIGH);
     analogWrite (ENA, (int)-lin_vel+100); //Velocidad motor A
     //Direccion motor B Izquierdo
     digitalWrite (IN3, LOW);
     digitalWrite (IN4, HIGH);
     analogWrite (ENB, (int)-lin_vel+95); //Velocidad motor B
  }
  //Derecha
  else if(rot_vel < 0){
     //Direccion motor A   Derecho
     digitalWrite (IN1, LOW);
     digitalWrite (IN2, HIGH);
     analogWrite (ENA, (int)-rot_vel+100); //Velocidad motor A
     //Direccion motor B Izquierdo  
     digitalWrite (IN3, HIGH);
     digitalWrite (IN4, LOW);
     analogWrite (ENB, (int)-rot_vel+100); //Velocidad motor B
  }
  //izquierda
  else if(rot_vel > 0){
    //Direccion motor A
    digitalWrite (IN1, HIGH);
    digitalWrite (IN2, LOW);
    analogWrite (ENA,(int)rot_vel+100); //Velocidad motor A
    //Direccion motor B
    digitalWrite (IN3, LOW);
    digitalWrite (IN4, HIGH);
    analogWrite (ENB, (int)rot_vel+100); //Velocidad motor A
  }
  //parar
  else
  {
    digitalWrite (IN1, LOW);
    digitalWrite (IN2, LOW);
    analogWrite (ENA, 0); //Velocidad motor A
    //Direccion motor B
    digitalWrite (IN3, LOW);
    digitalWrite (IN4, LOW);
    analogWrite (ENB, 0); //Velocidad motor A
  }
  
  
}

ros::Subscriber<geometry_msgs::Twist> sub_mov_motor("turtlebot_cmdVel", messageCb );


geometry_msgs::Pose2D position_msg;                       // Crear mensaje de posicion tipo Pose2D
ros::Publisher pub_distance("turtlebot_position", &position_msg); 


void setup() 
{
   attachInterrupt(digitalPinToInterrupt(encoderR),REncoder,FALLING);                // linea para añadir una interrupciòn a un PIN
   attachInterrupt(digitalPinToInterrupt(encoderL),LEncoder,FALLING);                // linea para añadir una interrupciòn a un PIN

   pinMode (ENA, OUTPUT);
   pinMode (ENB, OUTPUT);
   pinMode (IN1, OUTPUT);
   pinMode (IN2, OUTPUT);
   pinMode (IN3, OUTPUT);
   pinMode (IN4, OUTPUT);

   nh.initNode();
   nh.subscribe(sub_mov_motor);
   nh.advertise(pub_distance);
}







/*********************************************************************************************************************************************************************
 ******************************************************** Aqui va todo lo de los encoders y odometria ****************************************************************
 *********************************************************************************************************************************************************************
 */

void REncoder() {                                                                                         // función de interrupción del enconder llanta derecha
      Rtick++;                                                                                           // Nùmero de ticks llanta derecha
      CR++;                                                                                               // incremento del contador de ticks
      if (CR == contadorTicks){                                                                           // si el contador de ticks alcanza el valor de ticks determinado para el cálculo del tiempo
          float media = 0;                                                                                // variable creada para cálculo del promedio  
//-------------------------------------- -----------------------------    Filtro promedio    -----------------------------------------------------------------------------//
          for(int i=0;i < tam-1;i++){                                                                    // relleno del vector para cálculo posterior del promedio
              vectorR[i]=vectorR[i+1];                                                                   
          }
          vectorR[tam-1]=deltaMuestreoInterrupcionR ;                                                     // ùltimo dato del vector (medida actual) 

          for(int i=0;i<tam;i++){                                                                        // Suma de los valores del vector
              media = vectorR[i]+ media;
          }
          media = media/tam;                                                                             //división por el total de datos del vector
          deltaMuestreoInterrupcionR = media;                                                            // se reemplaza por el valor de su medío. 
//-------------------------------------- ----------------------------- ---------------------------------------------------------------------------------------------------//           
          frecuenciaR = (1000)/ deltaMuestreoInterrupcionR;                                              // frecuencia de interrupciòn      
          muestreoAnteriorInterrupcionR = muestreoActualInterrupcionR;                                   // se actualiza el tiempo de interrupciòn anterior
          CR = 0;                                                                                        //Reinicio de contador de ticks
      } 
 } 

void LEncoder() {                                                                                       // funciòn de interrupciòn del enconder llanta izquierda
      Ltick++;                                                                                           // Nùmero de ticks llanta izquierda
      CL++;                                                                                             // incremento del contador de ticks
      if (CL == contadorTicks){                                                                         // si el contador de ticks alcanza el valor de ticks determinado para el cálculo del tiempo
          float media = 0;                                                                              // variable creada para cálculo del promedio
//-------------------------------------- -----------------------------    Filtro promedio    -----------------------------------------------------------------------------//
          for(int i=0;i < tam-1;i++){                                                                    // relleno del vector para calculo posterior del promedio
              vectorL[i]=vectorL[i+1];
          }
          vectorL[tam-1]=deltaMuestreoInterrupcionL;                                                     // último dato del vector (medida actual) 

          for(int i=0;i<tam;i++){                                                                        // Suma de los valores del vector
              media = vectorL[i]+ media;
          }
          media = media/tam;                                                                             //división por el total de datos del vector
          deltaMuestreoInterrupcionL = media;                                                            // se reemplaza por el valor de su medío. 
//-------------------------------------- ----------------------------- ---------------------------------------------------------------------------------------------------//      
          frecuenciaL = (1000)/ deltaMuestreoInterrupcionL;                                              // frecuencia de interrupciòn 
          muestreoAnteriorInterrupcionL = muestreoActualInterrupcionL;                                   // se actualiza el tiempo de interrupciòn anterior
          CL = 0;                                                                                        // Reinicio de contador de ticks
       } 
 } 


/*********************************************************************************************************************************************************************
 ******************************************************** Aqui va todo lo de movimiento los motores ******************************************************************
 *********************************************************************************************************************************************************************
 */

/* 
 void Adelante ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, sol); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, sol); //Velocidad motor B
}

void Atras ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, sol); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, sol); //Velocidad motor B
}

void Derecha ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, velAngular); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, velAngular); //Velocidad motor A
}

void Izquierda ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, velAngular); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, velAngular); //Velocidad motor A
}

void Parar ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 0); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 0); //Velocidad motor A
}

*/



void loop() { 
    muestreoActual = millis();                                                                           //Tiempo actual de muestreo
    muestreoActualInterrupcionR = millis();                                                              // se asigna el tiempo de ejecuciòn a el muestreo actual
    muestreoActualInterrupcionL = millis();                                                              // se asigna el tiempo de ejecuciòn a el muestreo actual
    position_msg.x = x;
    position_msg.y = y;
    position_msg.theta = phi;
    pub_distance.publish(&position_msg);

    deltaMuestreo =(double) muestreoActual - muestreoAnterior;                                           // delta de muestreo 
    if ( deltaMuestreo >= k)                                                                             // se asegura el tiempo de muestreo
    {   
        deltaMuestreoInterrupcionR = muestreoActualInterrupcionR -  muestreoAnteriorInterrupcionR;       // diferencia tiempos de interruciones de ticks del motor     
        deltaMuestreoInterrupcionL = muestreoActualInterrupcionL -  muestreoAnteriorInterrupcionL;       // diferencia tiempos de interruciones de ticks del motor     

        if(deltaMuestreoInterrupcionR >= 200*contadorTicks){                                              // Esta es la forma de definir cuando el motor se encuentra quieto. Si deltaMuestreoInterrupcionR es mayor a 40 milisegundos por el preescalado de ticks
          frecuenciaR=0;                                                                                  // 40 mS es el tiempo que màximo se tarda un tick a la menor velocidad del motor
        }
        if(deltaMuestreoInterrupcionL >= 200*contadorTicks){                                              // Esta es la forma de definir cuando el motor se encuentra quieto. Si deltaMuestreoInterrupcionR es mayor a 40 milisegundos por el preescalado de ticks
          frecuenciaL=0;                                                                                  // 40 mS es el tiempo que màximo se tarda un tick a la menor velocidad del motor
        }

        Wr = contadorTicks*((2*PI)/N)*frecuenciaR;                                                        // frecuencia angular Rad/s
        Vr= Wr*(diametro/2);                                                                              // velocidad lineal cm/s
        Wl = contadorTicks*((2*PI)/N)*frecuenciaL;                                                        // frecuencia angular Rad/s
        Vl= Wl*(diametro/2);                                                                              // velocidad lineal cm/s     
    
        Serial.println(Wr);
        odometria();                                                                                      // cálculo de la odometría                 
        
        
       
        muestreoAnterior = muestreoActual;                                                                 // actualización del muestreo anterior
     }
     //////////////////////////////////////////////////////////////////////////////////////////////
    nh.spinOnce();
}




/*********************************************************************************************************************************************************************
 ******************************************************** Aqui va todo lo de los encoders y odometria ****************************************************************
 *********************************************************************************************************************************************************************
 */

void odometria(){ 

   deltaRtick = Rtick - RtickAnt;                                                                         // comparación de los ticks recorridos desde el último cálculo llanta derecha               
   Rdistancia = PI*diametro*(deltaRtick/(double) 20);                                                     // distancia recorrida por la llanta derecha desde el último cálculo

   deltaLtick = Ltick - LtickAnt;                                                                         // comparación de los ticks recorridos desde el último cálculo llanta izquierda      
   Ldistancia = PI*diametro*(deltaLtick/(double) 20);                                                     // distancia recorrida por la llanta izquierda desde el último cálculo   

   Cdistancia = (Rdistancia + Ldistancia)/2;                                                               // distancia recorrida por el punto central desde el último cálculo  

   x = x + Cdistancia*cos(phi);                                                                            // posición del punto X actual
   y = y + Cdistancia*sin(phi);                                                                            // posición del punto Y actual
   
   phi = phi + ((Rdistancia - Ldistancia)/longitud);                                                       // posición Angular actual
   phi = atan2(sin(phi),cos(phi));                                                                         //transformación de la posición angular entre -PI y PI

   RtickAnt = Rtick;                                                                                       // actualización de la variable RtickAnt con los valores de Rtick
   LtickAnt = Ltick;                                                                                       // actualización de la variable LtickAnt con los valores de Ltick
 } 
 /*
  * void messageCb( const geometry_msgs::Twist& cmd_vel){
  sol = (cmd_vel.linear.x*250)/10;
  if(cmd_vel.linear.x==4) {
    Izquierda();
  }
  else if(cmd_vel.linear.x==2) {
    Atras();
  }
  else if(cmd_vel.linear.x==3) {
    Derecha();
  }
  else if(cmd_vel.linear.x==1) {
    Adelante();
  }
  else{
    Parar();
  }
  velAngular=(cmd_vel.angular.y*longitud)/2;
}
*/
  
