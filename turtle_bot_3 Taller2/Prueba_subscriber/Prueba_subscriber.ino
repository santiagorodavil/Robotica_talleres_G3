#include <ros.h>
#include <std_msgs/Int8.h>

ros::NodeHandle nodoPrueba;

int led1 = 7;
int led2 = 8;
int var;

void messageCb(const std_msgs::Int8 &msg)
{
        var = msg.data;
        if (var == 0)
        {
          digitalWrite(led1, HIGH);
          digitalWrite(led2, LOW);
        }
        else if (var == 1)
        {
          digitalWrite(led1, LOW);
          digitalWrite(led2, HIGH);                    
        }
        else if (var == 2)
        {
          digitalWrite(led1, HIGH);
          digitalWrite(led2, HIGH);                    
        }
        else if (var == 3)
        {
          digitalWrite(led1, LOW);
          digitalWrite(led2, LOW);                    
        }
          
}


ros::Subscriber<std_msgs::Int8> sub("topic_prueba",&messageCb);

void setup() 
{
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  nodoPrueba.initNode();
  nodoPrueba.subscribe(sub); 
}

void loop() 
{
  nodoPrueba.spinOnce();
}
