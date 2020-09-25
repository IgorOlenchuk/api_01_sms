import time
import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': 5.92,
        'access_token': os.getenv('access_token')
    }
    get_status = requests.post('https://api.vk.com/method/users.get', params=params)
    return get_status.json()['response'][0]['online']  # Верните статус пользователя в ВК

def sms_sender(sms_text):
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    client = Client(account_sid, auth_token)
    sms_text = client.messages.create(
        to=os.getenv('NUMBER_TO'),
        from_=os.getenv('NUMBER_FROM'),
        body="Hello from Python!")
    return sms_text.sid # Верните sid отправленного сообщения из Twilio

# Download the helper library from https://www.twilio.com/docs/python/install

if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
