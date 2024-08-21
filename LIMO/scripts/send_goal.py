#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def send_goal(x, y, yaw):
    rospy.init_node('send_goal')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = yaw
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    client.wait_for_result()
    return client.get_result()

if __name__ == "__main__":
    x = -2.17  # Example value for the goal x position
    y = -0.527  # Example value for the goal y position
    yaw = 0.994  # Example value for the goal yaw orientation

    result = send_goal(x, y, yaw)
    if result:
        rospy.loginfo("Goal reached!")
    else:
        rospy.loginfo("Failed to reach goal.")

