import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from actions.tour import skip_input_tutorial


def input_activity(driver: WebDriver, hour_start: str, hour_end: str, minute_start: str, minute_end: str,
                   activity: str, sasaran_kerja_id: str):
    report = WebDriverWait(driver, 5).until(
        element_to_be_clickable((By.XPATH, '//*[@id="pilih-aktivitas-scroller"]/div[1]/a')))
    report.click()

    select_sasaran_kerja = WebDriverWait(driver, 5).until(
        visibility_of_element_located((By.ID, 'sasaran_kerja_id')))

    Select(select_sasaran_kerja).select_by_value(sasaran_kerja_id)

    hour_start_form = driver.find_element(By.XPATH, '//*[@id="jam_mulai"]')
    hour_start_form.send_keys(hour_start)

    minute_start_form = driver.find_element(By.XPATH, '//*[@id="menit_mulai"]')
    minute_start_form.send_keys(minute_start)

    hour_end_form = driver.find_element(By.XPATH, '//*[@id="jam_selesai"]')
    hour_end_form.send_keys(hour_end)

    minute_end_form = driver.find_element(By.XPATH, '//*[@id="menit_selesai"]')
    minute_end_form.send_keys(minute_end)

    description_form = driver.find_element(By.XPATH, '//*[@id="keterangan"]')
    description_form.send_keys(activity)

    submit = driver.find_element(By.XPATH, '//*[@id="simpan-btn-utama"]')
    submit.click()

    toast = driver.find_element(By.CLASS_NAME, 'toast-close-button')
    toast.click()

    print(f"Activity: {activity}: {hour_start}:{minute_start}-{hour_end}:{minute_end} inputted")

    time.sleep(2)


def find_activity(driver: WebDriver, activity: str):
    activity_search = driver.find_element(By.XPATH, '//*[@id="tab-1"]/div[2]/input')
    activity_search.send_keys(activity)


def select_activity_menu(driver: WebDriver):
    menu = WebDriverWait(driver, 5).until(
        element_to_be_clickable((By.XPATH, '//*[@id="aside"]/div/div[1]/nav/ul[1]/li[5]/a/span')))
    menu.click()
    
    skip_input_tutorial(driver)


def close_activity_modal(driver: WebDriver):
    modal_activity = driver.find_element(By.XPATH, '//*[@id="modal-laporkan"]/div/div/div/button')
    modal_activity.click()
