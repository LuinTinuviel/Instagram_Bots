import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from random import randint, choice


WEBSITE = "https://instagram.com"
USERNAME = "koszernapantera"
PASSWORD = "Q*Ac2Yc~$5NydVe"
TARGET_ACCOUNT = "9gag"

class InstaFollower:
    def __init__(self):
        self.driver = None
        self.start_driver()

    def start_driver(self):
        # Keep browser open so you can manually log out
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        if sys.platform == "win32":
            chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
    def login(self, username, password):
        # Click "decline cookies"
        self.driver.get(WEBSITE)
        time.sleep(self.getRandomTime(5, 10))

        # Disabling cookies
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'))).click()
        except exceptions.TimeoutException:
            print(f'No cookies to accept')
            try:
                print("Retrying cookies denial")
                self.driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]").click()
            except exceptions.ElementClickInterceptedException:
                print("Cookies pop up has won /// ")
        else:
            print("Cookies declined")

        try:
            # Type username
            self.driver.find_element(by=By.NAME, value="username").send_keys(username)
            # Type password
            self.driver.find_element(by=By.NAME, value="password").send_keys(password)
        except Exception as e:
            print(f"Problem with typing credentials: {e}")
        else:
            time.sleep(self.getRandomTime())

        # Click "Submit"
        try:
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        except exceptions.NoSuchElementException:
            print(f'Error when clicking on "Submit"')
            # Trying other way:
            try:
                self.driver.find_element(by=By.NAME, value="password").send_keys(Keys.ENTER)
            except:
                print('Error when clicking enter :/')
                print("Give up of trying to log in ... ")
                return
        else:
            time.sleep(self.getRandomTime(25,30))

        # Click "Do not save credentials"
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
            time.sleep(self.getRandomTime(5, 10))
        except exceptions.TimeoutException:
            print(f"No such element - do not save credentials")
        except exceptions.ElementClickInterceptedException:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]"))).click()
            except exceptions.ElementClickInterceptedException:
                print("Save creedentials has won /// ")


    def turn_off_notifications(self):
        # Click no to notifications
        try:
            notification_off = self.driver.find_elements('css selector', 'button')
        except exceptions.NoSuchElementException:
            print("notification element not found")
        else:
            not_off = [item for item in notification_off if item.text == "Not Now"]
            if not_off:
                not_off[0].click()
                print("Clicking on 'Not Now'")
            else:
                print("No button 'Not now'")

    def go_to_account(self, account):
        self.turn_off_notifications()
        try:
            # click on search
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[1]/div/div'))).click()
            except exceptions.TimeoutException:
                print("Click on search failed")
                return

            try:
                search = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input')))
            except:
                print("Finding search bar failed")
            else:
                search.send_keys(
                    account)
                time.sleep(self.getRandomTime())
                search.send_keys(
                    Keys.ENTER)
                print("Fiiling search bar")
                time.sleep(self.getRandomTime(10, 15))
        except:
            print("Failed to go to the target account")
            self.turn_off_notifications()
            return False
        else:
            print(f"Trying Going to account: {account}")
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[3]/div/a[1]/div[1]"))).click()
            except exceptions.TimeoutException:
                print("Failed to go to account")
            else:
                print(f"Went to account: {account}")
                return True

    def find_followers(self, account):
        # wait for account to be loaded
        if not self.go_to_account(account):
            print("Going to account has failed... Finishing")
            return

        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                             "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a/h2")))
        except exceptions.TimeoutException:
            print("Account page not loaded correctly")
            return



    def follow(self):

        # click on followers:
        try:
            followers_links = self.driver.find_elements('css selector', 'a')
        except exceptions.NoSuchElementException:
            print("followers element not found")
            return
        else:
            followers_link = [item for item in followers_links if " followers" in item.text]
            if followers_link:
                followers_link[0].click()
                print("Clicking on 'Followers'")
            else:
                print("Link to followers not found")
                return

        popup = '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]'
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, popup)))
        except exceptions.TimeoutException:
            print("Timeout waiting for the followers pop up")
            return
        else:
            time.sleep(self.getRandomTime(2, 5))

        followed_count = 0

        for i in range(5):
            try:
                follow_button = self.driver.find_elements('css selector', 'button')
            except exceptions.NoSuchElementException:
                print("follow element not found")
            else:
                to_follow = [item for item in follow_button if item.text == "Follow"]
                for button in to_follow:
                    try:
                        button.click()
                    except exceptions.ElementClickInterceptedException:
                        print("Instagram banned following new accounts :)")
                        current_buttons = self.driver.find_elements('css selector', 'button')
                        print("Alternative buttons which were visible")
                        for buttons in current_buttons:
                            if buttons.text != "Follow" and buttons.text != "":
                                print(buttons.text)
                        time.sleep(self.getRandomTime(2, 5))
                    else:
                        time.sleep(self.getRandomTime(2, 5))
                        followed_count += 1
                else:
                    print("No button 'Follow'")

            # Scrolling down
            try:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            except:
                print("Failed to scroll down...")
                time.sleep(self.getRandomTime(2, 5))
            else:
                print("Pop up scrolled")

        print(f"Followed accounts: {followed_count}")

        try:
            self.driver.find_element(By.CLASS_NAME, '_abl-').click()
            # to_close = [item for item in buttons if item.name == "Close"]
            # if to_close:
            #     to_close[0].click()
            #     print("Closed Followers pop-up")
            # else:
            #     print("No close button")
        except:
            print("Failed to close Followers list")
        else:
            print("Closed followers pop up")
            time.sleep(self.getRandomTime(2, 5))

    @staticmethod
    def getRandomTime(min=3, max=5):
        rand_time = randint(min,max)
        return rand_time


if __name__ == '__main__':
    bot = InstaFollower()
    bot.login(USERNAME, PASSWORD)
    bot.find_followers(TARGET_ACCOUNT)
    for i in range(5):
        bot.follow()






    
