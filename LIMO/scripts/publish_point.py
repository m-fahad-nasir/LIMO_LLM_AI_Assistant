#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PointStamped

def publish_point(x, y, z):
    rospy.init_node('publish_point')

    point_pub = rospy.Publisher('/clicked_point', PointStamped, queue_size=10)
    rate = rospy.Rate(1)

    point = PointStamped()
    point.header.frame_id = "map"
    point.point.x = x
    point.point.y = y
    point.point.z = z

    for _ in range(5):  # Publish the point 5 times
        point.header.stamp = rospy.Time.now()
        point_pub.publish(point)
        rate.sleep()

if __name__ == "__main__":
    x = -2.17  # Example value for the point x position
    y = -0.0527  # Example value for the point y position
    z = 0.994  # Example value for the point z position

    publish_point(x, y, z)

