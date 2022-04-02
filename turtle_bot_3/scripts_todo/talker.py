#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Int8

def talker():
    pub = rospy.Publisher('chatter', Int8, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        nums=[1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4]
        for n in nums:
            hello_str = n
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

