from core.selenium_scraping_setup import login_with_selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

def parse_race(state_var, race):
    driver = login_with_selenium()
    base_url = 'https://www.battleforthehill.com/states/'
    url = f'{base_url}{state_var}/elections'
    print(url)
    driver.get(url)

    table_xpath = "(//table[@class='w-full bg-gray-900 text-gray-300'])"
    print(f"Saved screenshot of race to race_screenshot.png")

    race_indices = {
        "sen2": 2,
        "s2": 2,
        "senator2": 2,
        "sen1": 0,
        "s1": 0,
        "senator1": 0,
        "house": 3,
        "h": 3,
        "reps": 3,
        "rep": 3,
        "governor": 1,
        "gov": 1,
        "gubernatorial": 1,
        "g": 1
    }

    try:
        table_index = race_indices.get(race.lower())
        if table_index is not None:
            button_xpath = ".//button[not(@disabled)] | .//input[@type='button' and not(@disabled)]"
            table = driver.find_elements(By.XPATH, table_xpath)[table_index]
            button = table.find_element(By.XPATH, button_xpath)
            button.click()
        else:
            raise ValueError("Invalid race name")

        race_table = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[3]/div[2]/div[1]/div/table/tbody")
        poll_close = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[3]/div[1]/div[1]/div/table/tbody/tr[3]/td[2]')

        return race_table, poll_close

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
