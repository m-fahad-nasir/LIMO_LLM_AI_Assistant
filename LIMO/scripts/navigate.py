#!/usr/bin/env python3

import subprocess
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PointStamped

def source_workspace_and_run_command(workspace_setup, ros_command):
    command = f"source {workspace_setup} && {ros_command}"
    process = subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def send_goal(x, y, yaw):
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

def main():
    rospy.init_node('send_goal', anonymous=True)

    workspace_setup = "~/agilex_ws/devel/setup.bash"
    roslaunch_cmd = "roslaunch limo_bringup limo_navigation_diff.launch"

    # Start the launch file
    launch_process = source_workspace_and_run_command(workspace_setup, roslaunch_cmd)
    
    time.sleep(10)  # Give some time for all nodes to start

    # Predefined goal values
    x = 6.69  # Example value for the goal x position
    y = -1.55 # Example value for the goal y position
    yaw = -0.00143  # Example value for the goal yaw orientation

    result = send_goal(x, y, yaw)
    if result:
        print("Goal reached!")
    else:
        print("Failed to reach goal.")

    # Terminate the launch process
    launch_process.terminate()

if __name__ == "__main__":
    main()
