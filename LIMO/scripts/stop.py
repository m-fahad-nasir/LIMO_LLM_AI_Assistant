#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def publish_velocity(linear_vel, angular_vel):
    twist = Twist()
    twist.linear.x = linear_vel
    twist.angular.z = angular_vel
    vel_pub.publish(twist)

if __name__ == '__main__':
    try:
        rospy.init_node('velocity_publisher', anonymous=True)
        vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


        linear_velocity = 0.0
        angular_velocity = 0

        rate = rospy.Rate(10) 

        while not rospy.is_shutdown():
            publish_velocity(linear_velocity, angular_velocity)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
