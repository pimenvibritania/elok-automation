from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def skip_welcome_tutorial(driver: WebDriver):
    try:
        driver.implicitly_wait(10)
        skip = driver.find_element(By.XPATH, '//*[@id="step-0"]/nav/button')
        skip.click()
    except Exception:
        print("Skipping welcome tutorial fail....")

    try:
        driver.implicitly_wait(10)
        skip = driver.find_element(By.XPATH, '//*[@id="peringatan"]/div/div/div[1]/button')
        skip.click()
    except Exception:
        print("Skipping welcome warning fail....")


def skip_input_tutorial(driver: WebDriver):
    try:
        skip = driver.find_element(By.XPATH, '//*[@id="step-0"]/nav/button')
        skip.click()
    except Exception:
        print("Skipping input tutorial fail....")
