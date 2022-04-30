#! /usr/bin/env python3
import cv2
import numpy as np


from geometry_msgs.msg import Point
from std_msgs.msg import String
import rospy

lim_low_color = np.array([0,100,20],np.uint8)
lim_upp_color = np.array([1,255,255], np.uint8)

x = 0
y = 0


########################################################
# funcion que recibe el nombre del color que se va a recibir
# (RGB), dependiendo del color se va a asignar la mascara que
# se va a utilizar para identificar el color
########################################################
def identifyColor(color):
    global lim_low_color
    global lim_upp_color

    if color.data == "green":
        lim_low_color = np.array([40,100,20], np.uint8)
        lim_upp_color = np.array([80,255,255], np.uint8)

    elif color.data =="red":
        lim_low_color = np.array([150,100,20], np.uint8)
        lim_upp_color = np.array([180,255,255], np.uint8)

    elif color.data == "blue":
        lim_low_color = np.array([90,100,20], np.uint8)
        lim_upp_color = np.array([120,255,255], np.uint8)
    else:
        lim_low_color = np.array([0,100,20], np.uint8)
        lim_upp_color = np.array([1,255,255], np.uint8)





def detection(cap):
    global lim_low_color
    global lim_upp_color
    global x
    global y
    ret, frame = cap.read()
    #print(cap)
    if ret:
        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(frameHSV, lim_low_color, lim_upp_color)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 4000:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1
                
                x = int(M["m10"] / M["m00"])
                y = int(M['m01'] / M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)
                print(x,y)


        position = Point()
        position.x = x
        position.y = y

        sendPos = rospy.Publisher('robot_manipulator_goal', Point, queue_size = 10)
        sendPos.publish(position)

        # cv2.imshow('mascaraAzul', mascara)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            ser.close()




def robotCamera():
    global x
    global y
    rospy.init_node('robot_manipulator_camera')
    rospy.Subscriber('robot_manipulator_ping_pong',String, identifyColor)
    cap = cv2.VideoCapture(0)
    pub = rospy.Publisher('robot_manipulator_goal', Point, queue_size = 10)
    rate = rospy.Rate(10)
    position = Point()
    while not rospy.is_shutdown():
        position.x = x
        position.y = y
        pub.publish(position)
        rate.sleep()
        detection(cap)

    cap.release()
    cv2.destroyAllWindows()
if __name__ =='__main__':
    robotCamera()
