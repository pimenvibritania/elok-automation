import requests


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


if __name__ == '__main__':
    main()
