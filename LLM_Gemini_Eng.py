import speech_recognition as sr
from gemini import Gemini, Headers
import socket
import time
from time import sleep
import requests

def initialize_client():
    # New Cookies for Gemini
    #"__Secure-1PSID": "g.a000jwiD2EIqj6QLabBYOhsRPkrLNyqpQxACejbq7q4LCTlDMO0sSq_d4v85kp4AEez09QEVaAACgYKAUUSAQASFQHGX2Mi4DIunYAkV1H9JCGRgfbDwBoVAUF8yKofqvNWWLW2QvGYzfGs41K-0076",
    #"__Secure-1PSIDTS": "sidts-CjEB4E2dkTxCIJPGDNd60FcAOkCvEsrtLU8TlagY9WCTdjUDg7iHGdWxg9JYKkA7nnS6EAA",
    #"NID": "516=EOdkYWJSIDkd3vR9N7Yx1zBoGFdBT-euqGcYDtjXDlTmkor7T6PlEwHK7pp9i_C7K6XaydiGYDn50Y9U-3B6QowaGB7KKaQNpmj5tyUYPLyR61PRz4Ii3nLxkii2jPrlNYMfMYA7GMPxGZmO486MJlkg1b9hszDbqQwkJmkfOqITVPgJ9K-NXL0_vxPm3dhwFFObWesQXk-i5HKqqcVTLHQ-JqdCJskIh_QfFmAg7f-SEjzYoaGfjhNPhdJL_LcPEQL7Nzd36hf_imNgtnzfOcRD2mG8tGQLkiflPQzuVhtsHh39Ogz_mXVrfLVh4n_-GoZj-aG390G0BRmUZEhGoBrlhv9y1MF783UQ2CnzDEGiU5etvPTBiQsybPRaSqXAniKnVMQ7SaQr60Q4778sGRZ_F4Gv",
    #"__Secure-1PSIDCC": "AKEyXzVeaK_nQHC_yl8dk8qE2HZ0O9SSeyN7-96ycgVZ1zxIKixT3vKGd_v4QrWfmOHp-hRS1rDp"

    cookie_dict = {
        "__Secure-1PSID": "",
        "__Secure-1PSIDTS": "",
        "NID": "",
        "__Secure-1PSIDCC": ""
    }

    session = requests.Session()
    session.headers = Headers.MAIN

    client = Gemini(cookies=cookie_dict)
    return client

client = initialize_client()
listening = True

def general():
    response = client.generate_content("Act as an AI assistant named LIMO. Respond within 2 lines only. Recorrect if there is any typo or errors in questions.")
    answer = response.payload
    print(answer['candidates'][0]['text'])

def specific():
    print('Specific Mode Initiated')

def get_response(user_input):
    Text = "I want single digit as your Response. If I say 'move forward' generate the Output 0 nothing else. If I say 'move backward' generate the output 1, if I say 'move right' output digit 2, and if I say 'move left' the output digit 3. If I say is 'camera' output digit 4. If I say 'slam' then output the digit 5,  If I say 'save' output the digit 6, if I say 'navigate' then output the digit 7. If I say anything else output digit 10. Please make sure to respond with digits only (0, 1, 2, 3, 4 ,5, 6, 7 or 10). Don't output any text in response or keycap digits. I Just want a single Number as Output. Now, Give me the response to the following :  "
    user_input = Text + user_input
    
    try:
        # Re-initialize the client to refresh cookies/session
        global client
        client = initialize_client()
        
        limo_response = client.generate_content(user_input)
        output = limo_response.payload['candidates'][0]['text']
        print('Waiting for Gemini ...')
        print(output)
        return output
    
    except requests.exceptions.HTTPError as e:
        print(f"Failed to generate content due to an error: {e}")
        return "10"  # Return a default value or handle the error accordingly
    

def send_response(response_from_limo):
    HOST = '192.168.0.194'  # IP address of the other PC/LIMO
    PORT = 65432            # Choose a port that's not in use
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(response_from_limo.encode())
            print("Response sent to LIMO.")
            
        except:
            print("LIMO Inactive!")

intro = "Hello, I'm LIMO your AI assistant. How may I help you. I have two modes General and Specific. In general mode you can as me anything and in specific mode you can give commands. Enter 0 for General and 1 for specific mode"
send_response(intro)

print("AI Assisant (Select Mode):")
print("0: General Mode")
print("1: Specific")
print("Enter your choice (0 or 1): ")

user_choice = input()
if user_choice == '0':
    general()
elif user_choice == '1':
    specific()
else:
    print("Invalid choice. Please enter 0 or 1.")

print("Please wait a moment Gemini is getting started")

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=2)
            response_wake = recognizer.recognize_google(audio, language='en-US')
            print(response_wake)


            if "limo" in response_wake.lower():     
                sleep(1.5)
                print("LIMO ACTIVE - What kind of help do you need?")                 
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                response = recognizer.recognize_google(audio, language='en-US')
                
                response_from_limo = get_response(response)
                
                send_response(response_from_limo)
                print("This is LIMO Stating ---->>>", response)


            else:
                print("I couldn't catch the word!")                
        except sr.WaitTimeoutError:
            print("Response time exceeded")                                
        except sr.UnknownValueError:
            print("Could you say that again?")
