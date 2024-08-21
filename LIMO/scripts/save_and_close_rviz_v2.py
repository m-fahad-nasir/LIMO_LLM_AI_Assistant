#!/usr/bin/env python3

import subprocess
import rospy
import os
from std_srvs.srv import Empty

def save_map(filename="Map_Scanned_File", directory_path="~/agilex_ws/src/limo_ros/limo_bringup/"):
    """
    Saves the map using map_saver node.

    Args:
        filename (str, optional): The filename to save the map as. Defaults to "Map_Scan_File".
        directory_path (str, optional): The directory path to save the map in. Defaults to "~/agilex_ws/src/limo_ros/limo_bringup/".
    """
    try:
        # Expand user path and create full file path
        full_path = os.path.join(os.path.expanduser(directory_path), filename)

        # Save map to the specified directory and filename
        subprocess.call(['rosrun', 'map_server', 'map_saver', '-f', full_path])
        print(f"Map saved successfully as '{full_path}'.")

    except Exception as e:
        print(f"Failed to save the map: {e}")

def close_rviz(nodes_to_terminate=["slam_gmapping", "rviz", "move_base", "robot_pose_ekf", "explore"]):
    """
    Terminates ROS nodes and closes RViz.

    Args:
        nodes_to_terminate (list, optional): List of ROS nodes to terminate. Defaults to ["explore", "slam_gmapping", "robot_pose_ekf", "limo_base_node", "move_base", "rviz"].
    """
    try:
        for node in nodes_to_terminate:
            subprocess.call(["rosnode", "kill", node])
            rospy.loginfo(f"Terminated node: {node}")

        print("RViz closed successfully.")
    except Exception as e:
        print(f"Failed to close nodes: {e}")

if __name__ == "__main__":
    # Initialize ROS node
    rospy.init_node('save_and_close_rviz', anonymous=True)

    save_map()
    close_rviz()
