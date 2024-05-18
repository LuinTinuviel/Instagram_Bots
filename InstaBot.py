from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.common import exceptions
import chromedriver_autoinstaller
import time
from random import randint, choice

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

class InstaBot:
    def __init__(self, username, password, tags):

        self.driver = launchBrowser("https://instagram.com")
        self.tags = tags
        no_like_streak = 0
        like_streak = 0

        # Click "allow cookies"
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/button[1]").click()
        time.sleep(getRandomTime())

        # Type username
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
        # Type password
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        time.sleep(getRandomTime())

        # Click "Submit"
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        time.sleep(getRandomTime(10,15))

        # Click "Do not save credentials"
        try:
            self.driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
            "/html/body/div[6]/div/div/div/div[3]/button[2]"
            time.sleep(getRandomTime(5, 10))
        except exceptions.NoSuchElementException:
            print(f"No such element - do not save credentials")
            time.sleep(getRandomTime(10, 15))

        # Click no to notifications
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]').click()
            time.sleep(getRandomTime())
        except exceptions.NoSuchElementException:
            print(f"No such element - notifications pop up")
            time.sleep(getRandomTime(10, 15))

        # Go to tag
        tag_ready = False
        while not tag_ready:
            tag_ready = self.go_to_tag()
            time.sleep(getRandomTime(3, 5))

        while True:

            if no_like_streak > 2 or like_streak > 20:
                no_like_streak = 0
                like_streak = 0
                tag_ready = False
                while not tag_ready:
                    tag_ready = self.go_to_tag()
                    time.sleep(getRandomTime(3, 5))
            else:
                self.driver.refresh()
            time.sleep(getRandomTime(5, 10))
            # Find a photo:
            select_photo = f'//*[@id="react-root"]/section/main/article/div[2]/div/div[{randint(1,6)}]/div[{randint(1,3)}]/a/div/div[2]'
            try:
                self.driver.find_element(By.XPATH, select_photo).click()
            except exceptions.NoSuchElementException as e:
                print(f"No such element: {select_photo}\n{e}")
                self.driver.refresh()
                tag_ready = False
                while not tag_ready:
                    tag_ready = self.go_to_tag()
                    time.sleep(getRandomTime(3, 5))
                continue
            except exceptions.ElementClickInterceptedException as e:
                print(f"Element not clickable: {select_photo}\n{e}")
                time.sleep(getRandomTime(5, 10))
                continue

            time.sleep(getRandomTime(5, 10))

            # Click like:
            try:
                like_area = self.driver.find_element(By.CLASS_NAME, "fr66n")
            except exceptions.NoSuchElementException as e:
                print(f"Something went wrong:\n{e}")
                self.driver.refresh()
            else:
                try:
                    heart = like_area.find_element(By.TAG_NAME, 'svg')
                    like_button = like_area.find_element(By.TAG_NAME, 'button')
                    if heart.value_of_css_property('color') == 'rgba(142, 142, 142, 1)':
                        like_button.click()
                        print("Liked")
                        like_streak += 1
                        no_like_streak = 0
                    else:
                        print("Like already given")
                        no_like_streak += 1
                except exceptions.NoSuchElementException as e:
                    print(f"Something went wrong:\n{e}")
                else:
                    time.sleep(getRandomTime(10, 15))
                    try:
                        self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/button').click()
                    except exceptions.NoSuchElementException as e:
                        print(f"Something went wrong:\n{e}")

    def go_to_tag(self):
        # Go to tag
        try:
            tag = choice(self.tags)
            self.driver.find_element(By.XPATH,
                                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(
                tag)
            time.sleep(getRandomTime())
            self.driver.find_element(By.XPATH,
                                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
            time.sleep(getRandomTime(10, 15))
        except:
            self.driver.refresh()
            return False
        else:
            print(f"Going to tag: {tag}")
            return True

def launchBrowser(website=""):
    driver = webdriver.Chrome()
    driver.get(website)
    return driver

def getRandomTime(min=3, max=5):
    rand_time = randint(min,max)
    return rand_time

hashtags = ["#catsofinstagram", "#Siberiancat", "#siberiancatsofinstagram", "#siberiancats", "#siberiancatsofinstagram", "#catlife", "#catphotos", "#siberiancatlover"]
InstaBot("login", "pass", hashtags)
