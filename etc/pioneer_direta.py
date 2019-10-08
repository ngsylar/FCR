#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32

def circle(): #circulo
    rate = rospy.Rate(1)
    for x in range(0, 2):
        pubr.publish(0.5)
        publ.publish(1.0)
        rate.sleep()

    stop = 0
    while stop != 1:
        stop = input('[1] to stop? ')

    for x in range(0, 2):
        pubr.publish(0.0)
        publ.publish(0.0)
        rate.sleep()

def square(): #quadrado
    print('[Ctrl]+[C] to finish? ')
    rot = 0
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        if rot == 0 :
            pubr.publish(1.0)
            publ.publish(1.0)
            rot += 1
        else:
            pubr.publish(-1.0)
            publ.publish(1.0)
            rot = 0
        rate.sleep()

def stop(): #parar
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        pubr.publish(0.0)
        publ.publish(0.0)
        rate.sleep()

if __name__ == '__main__':
    publ = rospy.Publisher('v_left', Float32, queue_size=10)
    pubr = rospy.Publisher('v_right', Float32, queue_size=10)
    rospy.init_node('lab1', anonymous=True)
    try:
#        stop()
        circle()
        square()
    except rospy.ROSInterruptException:
        pass
