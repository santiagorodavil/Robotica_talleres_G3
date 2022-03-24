#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from matplotlib import pyplot as plt

pos_x = 0.0
pos_y = 0.0
def callback(data):
    global pos_x
    global pos_y
    rospy.loginfo(rospy.get_caller_id()+ "Estoy escuchando: %s", data)
    pos_x = data.linear.x
    pos_y = data.linear.y

def plotPoint():
    global pos_y
    global pos_x
    pos_act = [0, 0]
    m =0
    while m<=100:
        pos_act = [pos_x, pos_y]
        plt.plot(pos_act, marker = 'o', color ='red')
        plt.hold(True)
        m = m+1
    plt.show()

def listener():
    rospy.init_node('listener')
    rospy.Subscriber("turtlebot_position", Twist, callback)
    rospy.spin()
    #plotPoint()

if __name__=='__main__':
    listener()
