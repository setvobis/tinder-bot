from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchWindowException, \
    WebDriverException
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class TinderSwindler:
    def __init__(self):
        self.homepage = "https://tinder.com"
        # replace `path` with path for chromedriver.exe, e.g. "D:/Users/user/ChromeDriver/chromedriver.exe"
        self.service = Service(r"path")
        self.ids = None
        self.driver = None
        self.end_time = None
        self.wait_1 = 1
        self.wait_2 = 2
        self.wait_5 = 5
        self.wait_15 = 15

    def login(self, email, password):
        """Connect to Tinder using email and password provided"""
        self.driver = Chrome(service=self.service)
        url = requests.get(self.homepage).text
        soup = BeautifulSoup(url, "html.parser")
        self.ids = [tag['id'] for tag in soup.select('div[id]')]
        self.driver.get(self.homepage)
        base_window = self.driver.window_handles[0]
        # --- log in button ---
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[0]}"]/'
                       f'div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'))).click()
        # --- use fb ---
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[1]/div/div/div[3]/span/div[2]/button'))).click()
        sleep(8)
        fb_login_window = self.driver.window_handles[1]
        self.driver.switch_to.window(fb_login_window)
        # sleep(7)
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "[id^=u_0_8"))).click()
        # self.driver.find_element(By.CSS_SELECTOR, "[id^=u_0_8").click()
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(email)
        password_form = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
        password_form.send_keys(password)
        password_form.submit()
        self.driver.switch_to.window(base_window)
        # --- dealing with requests ---
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[2]/div/div/div[1]/div[1]/button'))).click()
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/div/div[3]/button[1]'))).click()
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/div/div[3]/button[2]'))).click()

        # new: dark_mode skip
        ui.WebDriverWait(self.driver, self.wait_15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[2]/button'))).click()
        sleep(self.wait_5)

    def swipe(self):
        """Deals with popups that may occur during swiping process and is responsible for swiping"""
        end = False
        while not end:
            sleep(self.wait_5)
            # any pop up on the screen?
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[2]/button[2]').click()
                sleep(self.wait_1)
            except NoSuchElementException:
                pass
            except NoSuchWindowException:
                break

            # you've got x likes pop up
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/div[3]/button[2]').click()
                sleep(self.wait_1)
            except NoSuchElementException:
                pass
            except NoSuchWindowException:
                break

            # matched
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[1]/div/'
                                                   f'div[4]/button').click()
                sleep(self.wait_1)
            except NoSuchElementException:
                pass
            except NoSuchWindowException:
                break

            # do I have likes left
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[3]/button[2]').click()
                self.end_time = datetime.now()
                self.driver.close()
                break
            except NoSuchElementException:
                pass
            except NoSuchWindowException:
                break

            # successfully can reach like button
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[1]/div/main/div[1]/'
                                                   f'div/div/div[1]/div[1]/div/div[3]/div[3]/button').click()
                sleep(self.wait_2)
                # depends on if you want to press 'like' or 'dislike' swap `number` div[`number`] at the very
                # end of next line: div[2] for 'dislike' and div[4] for 'like'
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[1]/div/main/div[1]/'
                                                   f'div/div/div[1]/div[2]/div/div/div[4]/button').click()
            except ElementNotInteractableException:
                self.driver.refresh()
            except NoSuchWindowException:
                break

        try:
            self.driver.close()
        except WebDriverException:
            pass
        return self.end_time
