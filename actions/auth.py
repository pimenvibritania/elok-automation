from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait

from actions.tour import skip_welcome_tutorial


def login(driver: WebDriver, username: str, password: str):
    username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    username_field.send_keys(username)

    password_field = driver.find_element(By.XPATH, '//*[@id="pass"]')
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, '//*[@id="lojin"]')
    print("Logged in as ", username)
    login_button.click()
    skip_welcome_tutorial(driver)


def logout(driver: WebDriver):
    dropdown = WebDriverWait(driver, 10).until(
        element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[2]/ul/li[3]')))

    dropdown.click()

    logout_btn = WebDriverWait(driver, 10).until(
        element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[2]/ul/li[3]/ul/li[4]')))
    logout_btn.click()
    print("Successfully logout")
