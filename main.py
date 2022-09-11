from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from time import sleep
from bs4 import BeautifulSoup
import requests


class TinderSwindler:
    def __init__(self):
        self.homepage = "https://tinder.com"
        self.service = Service(r"D:/Users/setvo/ChromeDriver/chromedriver.exe")
        self.driver = Chrome(service=self.service)
        url = requests.get(self.homepage).text
        soup = BeautifulSoup(url, "html.parser")
        self.ids = [tag['id'] for tag in soup.select('div[id]')]
        self.driver.get(self.homepage)

    def login(self, email, password):
        base_window = self.driver.window_handles[0]
        # --- log in button ---
        ui.WebDriverWait(self.driver, 24).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[0]}"]/'
                       f'div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'))).click()
        # --- use fb ---
        ui.WebDriverWait(self.driver, 24).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[1]/div/div/div[3]/span/div[2]/button'))).click()
        sleep(9)
        fb_login_window = self.driver.window_handles[1]
        self.driver.switch_to.window(fb_login_window)
        sleep(8.5)
        self.driver.find_element(By.CSS_SELECTOR, "[id^=u_0_8").click()
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(email)
        password_form = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
        password_form.send_keys(password)
        password_form.submit()
        self.driver.switch_to.window(base_window)
        # --- dealing with requests ---
        ui.WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[2]/div/div/div[1]/div[1]/button'))).click()
        ui.WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/div/div[3]/button[1]'))).click()
        ui.WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable(
            (By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/div/div[3]/button[2]'))).click()
        sleep(6)

    def swipe(self):
        end = False
        profile = 0
        while not end:
            sleep(7)
            # any pop up on the screen?
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[2]/button[2]').click()
                print(f"There was a pop-up")
                sleep(1)
            except NoSuchElementException:
                pass

            # you've got x likes pop up
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div/'
                                                   f'div[3]/button[2]').click()
                sleep(1)
            except NoSuchElementException:
                pass

            # matched
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[1]/'
                                                   f'div/div[4]/button').click()
                print(f"Match")
                sleep(2)
            except NoSuchElementException:
                pass

            # do i have likes left
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[1]}"]/main/div/div[3]/button[2]').click()
                print(f"{profile}. profile intercepted, you have no likes to give")
                self.driver.close()
                break
            except NoSuchElementException:
                profile += 1

            # successfully can reach like button
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[1]/div/main/div[1]/'
                                                   f'div/div/div[1]/div[1]/div/div[3]/div[3]/button').click()
                sleep(3.5)
                self.driver.find_element(By.XPATH, f'//*[@id="{self.ids[0]}"]/div/div[1]/div/main/div[1]/'
                                                   f'div/div/div[1]/div[2]/div/div/div[4]/button').click()
            except ElementNotInteractableException:
                self.driver.refresh()
                print(f"{profile}. profile intercepted")
            print(f"{profile}. profile")


EMAIL = "your_facebook_email_or_phone_number"
PASSWORD = "your_facebook_password"

bot = TinderSwindler()
bot.login(EMAIL, PASSWORD)
bot.swipe()
