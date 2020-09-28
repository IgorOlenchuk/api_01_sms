import time
import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

api_version = 5.9
TOKEN = os.getenv('access_token')
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
url_base = 'https://api.vk.com/method/users.get'
client = Client(account_sid, auth_token)

def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': api_version,
        'access_token': TOKEN
    }
    try:
        get_status = requests.post(url_base, params=params)
    except NameError:
        print("Нет такой страницы")
    try:
        return get_status.json()['response'][0]['online']  # Верните статус пользователя в ВК
    except ValueError:
        print("Такого пользователя не существует")

def sms_sender(sms_text):
    sms_text = client.messages.create(
        to=os.getenv('NUMBER_TO'),
        from_=os.getenv('NUMBER_FROM'),
        body=sms_text)
    return sms_text.sid # Верните sid отправленного сообщения из Twilio

# Download the helper library from https://www.twilio.com/docs/python/install

if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
