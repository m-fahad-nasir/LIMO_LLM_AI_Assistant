#!/usr/bin/env python3

import subprocess
import rospy
from std_srvs.srv import Empty

def save_map():
    try:
        # Calling the map_saver node to save the map
        subprocess.call(['rosrun', 'map_server', 'map_saver', '-f', 'Map_Scan_File'])
        print("Map saved successfully as 'Map_Scan_File'.")
    except Exception as e:
        print(f"Failed to save the map: {e}")
        
    try:
        # Specify the directory where you want to save the map
        directory_path = "~/agilex_ws/src/limo_ros/limo_bringup/"
        # Calling the map_saver node to save the map in the specified directory
        subprocess.call(['rosrun', 'map_server', 'map_saver', '-f', directory_path])
        print(f"Map saved successfully as '{directory_path}'.")
    except Exception as e:
        print(f"Failed to save the map: {e}")

def close_rviz():
    try:
        # Terminate ROS nodes
        nodes_to_terminate = [
            "explore",
            "slam_gmapping",
            "robot_pose_ekf",
            "move_base",
            "rviz"
        ]

        for node in nodes_to_terminate:
            subprocess.call(["rosnode", "kill", node])
            rospy.loginfo(f"Terminated node: {node}")
            
            
        # Closing the RViz Window
        # subprocess.call(['pkill', 'rviz'])
      
        print("RViz closed successfully.")
    except Exception as e:
        print(f"Failed to close Nodes: {e}")
        
       

if __name__ == "__main__":
    # Initialize the ROS node
    rospy.init_node('save_and_close_rviz', anonymous=True)
    
    save_map()
    close_rviz()

