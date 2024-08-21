#!/usr/bin/env python3

import subprocess
import time

def source_workspace_and_run_command(workspace_setup, ros_command):
    """
    Function to source a ROS workspace and run a command.
    """
    command = f"source {workspace_setup} && {ros_command}"
    process = subprocess.Popen(command, shell=True, executable='/bin/bash')
    return process

def main():
    # Define the workspaces and commands
    ros_commands = [
        {
            "workspace_setup": "~/agilex_ws/devel/setup.bash",
            "commands": [
                "roslaunch limo_bringup limo_gmapping.launch",
                "roslaunch limo_bringup explore.launch"
            ]
        },
        {
            "workspace_setup": "~/Bard_ws/devel/setup.bash",
            "commands": [
                "roslaunch explore_lite explore_costmap.launch"
            ]
        }
    ]

    processes = []

    for command_set in ros_commands:
        workspace_setup = command_set["workspace_setup"]
        for command in command_set["commands"]:
            print(f"Running: {command} from {workspace_setup}")
            process = source_workspace_and_run_command(workspace_setup, command)
            processes.append(process)
            time.sleep(4)  # Add a 4-second delay between each command

    # Wait for all processes to complete
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    main()

