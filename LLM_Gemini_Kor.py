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
    response = client.generate_content("AI 비서 LIMO로 활동하십시오. 질문에 오타 또는 오류가 있는 경우 재수정하여 두 줄 이내로 응답하십시오.")
    answer = response.payload
    print(answer['candidates'][0]['text'])

def specific():
    print('Specific Mode Initiated')

def get_response(user_input):
    Text = "반응으로 한 자리 숫자를 원합니다. '앞으로 이동'이라고 말하면 0, '뒤로 이동'이라고 말하면 1, '오른쪽으로 이동'이라고 말하면 2, '왼쪽으로 이동'이라고 말하면 3을 출력하십시오. '카메라'라고 하면 4를 출력하십시오. 'SLAM'이라고 말하면 5를 출력하십시오. '저장'이라고 말하면 6을 출력하십시오. '네비게이트'라고 말하면 7을 출력하십시오. 다른 말을 하면 10을 출력하십시오. 응답에 숫자만 응답하십시오 (0, 1, 2, 3, 4, 5, 6, 7 또는 10). 응답에 텍스트나 키캡 숫자를 포함하지 마십시오. 이제 다음에 대한 응답을 제공하십시오: "
    user_input = Text + user_input
    
    try:
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

intro = "안녕하세요, 저는 AI 비서 LIMO입니다. 무엇을 도와드릴까요? 두 가지 모드가 있습니다. 일반 모드에서는 무엇이든 질문할 수 있고, 특정 모드에서는 명령을 내릴 수 있습니다. 일반 모드는 0, 특정 모드는 1을 입력하세요."
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

print("잠시만 기다려 주십시오, Gemini가 시작됩니다.")

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=2)
            response_wake = recognizer.recognize_google(audio, language='ko-KR')
            print(response_wake)


            if "리모" in response_wake.lower():     
                sleep(1.5)
                print("LIMO 활성화 - 어떻게 도와드릴까요?")                 
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                response = recognizer.recognize_google(audio, language='ko-KR')
                
                response_from_limo = get_response(response)
                
                send_response(response_from_limo)
                print("LIMO ---->>>", response)


            else:
                print("단어를 잡지 못했습니다!")                
        except sr.WaitTimeoutError:
            print("응답 시간이 초과되었습니다.")                                
        except sr.UnknownValueError:
            print("다시 말씀해주시겠습니까?")
