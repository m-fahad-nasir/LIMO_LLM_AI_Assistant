# LIMO_LLM_AI_Assistant
Implement an AI assistant on LIMO Robot that uses speech recognition to process voice commands and control a LIMO Robot in Real Time. It allows to implement commands like movement, SLAM exploration, navigation, etc. via the Gemini AI service. 


This document outlines the setup and usage instructions for the LIMO AI Assistant.

### 1. Introduction

LIMO AI Assistant is a speech-controlled robot companion powered by Gemini, Google's large language model. It can perform various tasks and respond to your voice commands in multiple languages (currently set to English).

### 2. Download and Setup

**2.1. Code Acquisition**

1. Clone the Git Repo:

```
git clone https://github.com/m-fahad-nasir/LIMO_LLM_AI_Assistant
```

**2.2. Environment Setup**

1. Create a new virtual environment on your machine.
2. Activate the environment.
3. Install the required dependencies:

```bash
pip install python-gemini-api
pip install speechrecognition requests
```

**2.3. Gemini Cookie Acquisition**

1. Open Google Chrome and search for "Gemini."
2. Log in to your Gemini account or create a new one.
3. Open the Gemini homepage ([https://gemini.google.com/app](https://gemini.google.com/app)).
4. Press F12 to access the developer tools.
5. Navigate to the "Application" menu bar and "Cookies" sidebar (see Figure 1).

**Figure 1: Extracting Cookies from Gemini Manually**
![image](https://github.com/user-attachments/assets/37ddcdaa-c085-4c79-9711-ae8710265b48)

6. Copy the values of the following cookies:
    - `__Secure-1PSID`
    - `__Secure-1PSIDTS`
    - `NID`
    - `__Secure-1PSIDCC`

**2.4. Code Modification**

1. Open the downloaded code files, specifically `LLM_Gemini_Eng.py`.
2. Paste the copied cookie values into the designated sections of the code, replacing the placeholders within quotation marks (see Figure 2).

**Figure 2: Paste the cookies into the code.**
![image](https://github.com/user-attachments/assets/38289879-7395-4989-bec9-e15f2476fbdd)



3. Update the IP address of the LIMO device in both the PC and LIMO code files (see Figures 3 and 4).
**Figure 3: Update IP Address of LIMO in (PC) Code file.**
![image](https://github.com/user-attachments/assets/c845be21-0700-424e-8b70-09f823c68a9e)



**Figure 4: Update IP Address of LIMO in (LIMO) Code file.**
![image](https://github.com/user-attachments/assets/940ea030-3598-41fa-ab7c-c46aa6f5ec17)

**2.5. Deployment**

**On No Machine (Terminal 2):**

1. Open Terminal 2.
2. Navigate to the `agilex_ws` directory:

```bash
cd agilex_ws
```

3. Source the development setup:

```bash
source devel/setup.bash
```

4. Launch the camera and robot:

```bash
roslaunch astra_camera dabai_u3.launch
```

**On No Machine (Terminal 3):**

1. Open Terminal 3.
2. Navigate to the `Bard_ws` directory:

```bash
cd Bard_ws
```

3. Source the development setup:

```bash
source devel/setup.bash
```

4. Run the LIMO speech engine:

```bash
python3 eng_limo_speak.py
```

**On PC:**

1. Open the `LLM_Gemini_Eng.py` file on your PC.
2. Activate the virtual environment where the dependencies were installed.
3. Run the script.

### 3. Usage

**3.1. AI Assistant Mode Selection**

The script will prompt you to select the AI Assistant mode:

- **General Mode (0):** Ask anything, and Gemini will respond through LIMO's narration.
- **Specific Mode (1):** Give commands to control LIMO's movements and operations.

**3.2. Specific Mode Commands**

In Specific Mode, you can use voice commands to control LIMO. You have a 2-second window to speak after the prompt "Listening...". Commands include:

- **Move Forward:** Makes LIMO move forward.
- **Move Backward:** Makes LIMO move backward.
- **Move Right:** Makes LIMO move right.
- **Move Left:** Makes LIMO move left.
- **Camera:** Initializes and displays the camera feed.
- **SLAM:** Initiates Autonomous Explore SLAM Mapping.
- **Save:** Saves the generated SLAM map.
- **Navigate:** Navigates LIMO to a pre-defined point in a saved map file.

**3.3. Command Dependencies**

- Movement commands (forward, backward, left, right) are independent but cannot be used simultaneously.
- The camera command is independent and can be used with other commands.
- The SLAM command operates in autonomous mode until the "Save" command is issued. Saving closes all associated processes.
- The Navigate command requires a saved SLAM map and pre-defined coordinates within its code file.

**4. Additional Notes**

- The wake word to
