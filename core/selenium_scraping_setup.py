from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from shutil import which
from core.loadcarkeys import load_car_keys




def login_with_selenium():
    try:
        url = 'https://www.battleforthehill.com/login'
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)

        # Your login credentials
        email = load_car_keys()['user']
        password = load_car_keys()['pass']

        # Open the login page
        driver.get(url)

        # Wait for email and password input fields to be present
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_field.send_keys(email)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        print('Login successful!')

        return driver
    except Exception as e:
        raise e
