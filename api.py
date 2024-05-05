import datetime
import json

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from actions.auth import login


def holiday():
    dates = []

    with open('data/calendar.json') as file:
        data = json.load(file)

        for key in data["items"]:
            start_date = datetime.date.fromisoformat(key["start"]["date"])
            current_year = datetime.date.today().year
            cal_year = start_date.year

            if cal_year >= current_year:
                dates.append(start_date.strftime("%Y-%m-%d"))

    return dates


def api():
    holidays = holiday()
    current_date = datetime.datetime.now()
    full_date_formatted = current_date.strftime("%Y-%m-%d")
    date_formatted = int(current_date.strftime("%d"))

    day_name = current_date.strftime("%A").lower()

    if day_name == "sunday":
        print("Current is weekend!")
        return True

    with open('./data/payload.json') as file:
        payload_data = json.load(file)

    print(f"Today is: {day_name} - {full_date_formatted}")

    base_url = payload_data['elokUrl']

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless=new")

    additional_activity_data = payload_data['additionalActivity']

    for payload in payload_data['asn']:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("webdriver installed")
        driver.get(base_url)

        username = payload['nip']
        password = payload['password']
        activity_code = payload['activityCode']
        sasaran_kerja = payload['sasaranKerjaId']

        login(driver, username, password)

        csrf_token = driver.execute_script("return window.csrf_token;")
        cookies = driver.get_cookies()
        cookie_string = "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies)

        print("Cookie: ", cookie_string)
        print("CSRF: ", csrf_token)

        url = f"{base_url}/input/isiaktifitas"

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie_string,
            'Origin': 'https://tkd.bkpsdmcloud.com',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

        main_activity = payload['mainActivities'][day_name]

        activity_front = True

        for activity in main_activity:

            menit_mulai = activity['menitMulai'] if (
                    full_date_formatted not in holidays or day_name != "saturday") else "00"

            if activity["loopActivity"]:
                if activity_front:
                    select_activity = payload['arrayActivity'][date_formatted]
                    activity_front = False
                else:
                    select_activity = payload['arrayActivity'][-date_formatted]
                    activity_front = True
            else:
                select_activity = activity['activity']

            data = {
                'tanggal': full_date_formatted,
                'kode_aktifitas': activity_code,
                'volume': '1',
                'keterangan': select_activity,
                'sasaran_kerja_id': sasaran_kerja,
                'jenis': 'kinerja',
                'jam_mulai': activity['jamMulai'],
                'jam_selesai': activity['jamSelesai'],
                'menit_mulai': menit_mulai,
                'menit_selesai': activity['menitSelesai'],
                'id_input': '',
                'id_rencana_kinerja': sasaran_kerja
            }

            success_activity = (f"Aktifitas ({activity['jamMulai']}:{activity['menitMulai']} - {activity['jamSelesai']}"
                                f":{activity['menitSelesai']}): {activity['activity']} selesai diinput")

            try:
                response = requests.post(url, headers=headers, data=data)

                if response.status_code == 200:
                    content = response.json()
                    print(success_activity)
                    print(content)
                else:
                    print(f"Error: {response.status_code}")
            except Exception as e:
                print("Error post request, ", e)

        if day_name != "saturday" or full_date_formatted not in holidays:
            data = {
                'tanggal': full_date_formatted,
                'kode_aktifitas': additional_activity_data['activityCode'],
                'volume': '1',
                'keterangan': additional_activity_data['activity'],
                'sasaran_kerja_tambahan_id': 0,
                'jenis': 'umum',
                'jam_mulai': additional_activity_data['jamMulai'],
                'jam_selesai': additional_activity_data['jamSelesai'],
                'menit_mulai': additional_activity_data['menitMulai'],
                'menit_selesai': additional_activity_data['menitSelesai'],
                'id_input': '',
                'kode_kegiatan': ''
            }

            try:
                response = requests.post(url, headers=headers, data=data)

                if response.status_code == 200:
                    content = response.json()
                    print("Aktifitas tambahan selesai diinput")
                    print(content)
                else:
                    print(f"Error: {response.status_code}")
            except Exception as e:
                print("Error post request, ", e)

        driver.close()
        print("webdriver closed")


if __name__ == '__main__':
    api()
