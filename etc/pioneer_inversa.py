#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def circle():
    vel_msg = Twist()

    vel_msg.linear.x = 1.0
    vel_msg.linear.y = 0.0
    vel_msg.linear.z = 0.0
    vel_msg.angular.x = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.z = 2.0

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish(vel_msg)
        rate.sleep()

def square():
    vel_msg_forward = Twist()
    vel_msg_turn = Twist()

    vel_msg_forward.linear.x = 1.0
    vel_msg_forward.linear.y = 0.0
    vel_msg_forward.linear.z = 0.0
    vel_msg_forward.angular.x = 0.0
    vel_msg_forward.angular.y = 0.0
    vel_msg_forward.angular.z = 0.0

    vel_msg_turn.linear.x = 0.0
    vel_msg_turn.linear.y = 0.0
    vel_msg_turn.linear.z = 0.0
    vel_msg_turn.angular.x = 0.0
    vel_msg_turn.angular.y = 0.0
    vel_msg_turn.angular.z = 2.0

    rot = 0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if rot <= 10:
            pub.publish(vel_msg_forward)
            rot += 1
        else:
            if(rot <= 19):
                pub.publish(vel_msg_turn)
                rot += 1
            else:
                rot = 0
        rate.sleep()

if __name__ == '__main__':
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('lab1', anonymous=True)
    try:
        x = 0
        while x == 0:
            x = input('[1] to circle, [2] to square: ')
            if x == 1:
                print('[Ctrl]+[C] to finish. ')
                circle()
            else:
                if x == 2:
                    print('[Ctrl]+[C] to finish. ')
                    square()
                else:
                    x = 0
    except rospy.ROSInterruptException:
        pass
