import datetime
from os import environ

import requests
from twilio.rest import Client


def main():
    log = "logs/log_20240506_192539.log"

    with open(log, 'r') as file:
        payload = file.read()

    url = "https://pastebin.com/api/api_post.php"
    data = {
        'api_dev_key': '213dVWNQLBgw2ebDVRYImITn6mU83a9I',
        'api_paste_code': payload,
        'api_paste_name': 'log',
        'api_paste_private': '0',
        'api_option': 'paste',
        'api_user_key': '1390377dc9385f62d4d59012e1510691'
    }

    response = requests.post(url, data=data)

    print(response.text)


def send_wa(paste_url):
    auth_token = environ.get('TWILIO_TOKEN')
    account_sid = 'ACc7aaf48f5866730b1b4b6106a1d1f1d4'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        # media_url=[paste_url],
        body=f"*:::::{datetime.datetime.now().strftime("%Y-%m-%d")}:::::"
             f"*\n*Elok berhasil diinput!*\nLog bisa diakses di: {paste_url}",
        to='whatsapp:+6285723660012'
    )

    print(message.sid)


if __name__ == '__main__':
    # main()
    send_wa("https://pastebin.com/D1Lamc4u")
