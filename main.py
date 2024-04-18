import datetime
import json

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from actions.activity import input_activity, select_activity_menu, find_activity, close_activity_modal
from actions.auth import login, logout


def main():
    with open('./data/payload.json') as f:
        payload_data = json.load(f)

    current_date = datetime.datetime.now()

    day_name = current_date.strftime("%A").lower()

    print("Today is:", day_name)

    base_url = payload_data['elokUrl']

    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(base_url)
    driver.maximize_window()

    for payload in payload_data['asn']:
        username = payload['nip']
        password = payload['password']

        login(driver, username, password)

        activities = payload['mainActivities'][day_name]
        keyword_activity = payload['mainActivitiesFilter']
        sasaran_kerja_id = payload['sasaranKerjaId']

        select_activity_menu(driver)
        find_activity(driver, keyword_activity)

        for activity in activities:
            hour_start = activity['jamMulai']
            hour_end = activity['jamSelesai']
            minute_start = activity['menitMulai']
            minute_end = activity['menitSelesai']
            activity_name = activity['activity']

            try:
                input_activity(driver, hour_start, hour_end, minute_start, minute_end, activity_name,
                               sasaran_kerja_id)
            except ElementClickInterceptedException as e:
                print(e)

                toast = driver.find_element(By.CLASS_NAME, 'toast-close-button')
                toast.click()

                close_activity_modal(driver)
            except NoSuchElementException as e:
                print(e)
                close_activity_modal(driver)

            try:
                close_activity_modal(driver)
            except Exception as e:
                print("Modal not closed, because submit success...")
                print(e)

        logout(driver)
        # break

    driver.close()


if __name__ == '__main__':
    main()
