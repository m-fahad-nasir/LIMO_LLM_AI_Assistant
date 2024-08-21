#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from limo_base.msg import LimoStatus
import sys

i = 0

def battery_state_callback(data):
    global i
    if i == 0:
        print("현재 나의 베터리는 {:.1f} volts야".format(data.battery_voltage))
        i = 1
        # Add the line below to shut down the ROS node after printing the voltage
        rospy.signal_shutdown("Battery voltage printed.")
        # Terminate the script after shutting down the ROS node
        sys.exit()

def battery_status_node():
    rospy.init_node('battery_status_node', anonymous=True)
    rospy.Subscriber("/limo_status", LimoStatus, battery_state_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        battery_status_node()
    except rospy.ROSInterruptException:
        pass

