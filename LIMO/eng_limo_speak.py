# -*- coding: utf-8 -*-
import socket
import subprocess
import threading
import queue
from gtts import gTTS
import os

HOST = '192.168.0.194'  # Listen on all available interfaces
PORT = 65432  # Same port as used in the sending code

# Define a mapping of numbers to ROS commands
ros_commands = {
    '0': ["rosrun", "bard", "forward.py"],
    '1': ["rosrun", "bard", "backward.py"],
    '2': ["rosrun", "bard", "right.py"],
    '3': ["rosrun", "bard", "left.py"],
    '4': ["rosrun", "bard", "cam.py"],
    '5': ["rosrun", "bard", "mapping.py"],
    '6': ["rosrun", "bard", "save_and_close_rviz.py"],
    '7': ["rosrun", "bard", "navigate.py"],
    '8': ["rosrun", "bard", "nav_B.py"],
    '10': ["rosrun", "bard", "battery.py"],

    # Add more mappings as needed
}

# Variable to store the subprocess
current_subprocess = None

# Queue to pass lines from stdout to the audio playback thread
audio_queue = queue.Queue()

def play_response(response):
    global current_subprocess

    # Terminate the previous subprocess (if exists)
    if current_subprocess:
        try:
            current_subprocess.terminate()
            current_subprocess.wait(timeout=0.1)
        except subprocess.TimeoutExpired:
            current_subprocess.kill()
            current_subprocess.wait()

    # Save the response to a text file
    with open("response.txt", "w") as file:
        file.write(response)

    # Check the content of the file
    with open("response.txt", "r") as file:
        content = file.read().strip()



    if content in ros_commands:
        # Execute the corresponding ROS command and capture stdout
        try:
            tts = gTTS(text="Please wait for a moment. The command is being processed.", lang='en')
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")
            process = subprocess.Popen(ros_commands[content], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Start a thread to read stdout line by line
            stdout_thread = threading.Thread(target=read_stdout, args=(process,))
            stdout_thread.start()

            # Store the current subprocess
            current_subprocess = process
        except subprocess.CalledProcessError as e:
            print("Error executing ROS command:", e)
    else:
        # Use mpg321 subprocess if no matching ROS command
        try:
            subprocess.run(["pkill", "mpg321"], check=True)
        except subprocess.CalledProcessError:
            pass  # No previous espeak process found

        tts = gTTS(text=response, lang='en')
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")

def read_stdout(process):
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        print("ROS Command Output:", line)
        # Put the line in the audio queue for playback
        audio_queue.put(line)

# Function for audio playback in a separate thread
def play_audio():
    while True:
        try:
            line = audio_queue.get(timeout=0.1)  # Check for new lines every 0.1 seconds
            print(line)
            tts = gTTS(text=line, lang='en')
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")
        except queue.Empty:
            pass

# Create a socket to listen for responses
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening for responses on port", PORT)

    # Start the audio playback thread
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(1024)  # Receive up to 1024 bytes
            response = data.decode()

            # Update the response_thread with the new response
            play_response(response)

