from time import sleep
from typing import NoReturn, Optional

from loguru import logger
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from module.data_objtects import Account, Post


class Browser:

    def __init__(self, account: Account):
        self.account = account
        opts = ChromeOptions()
        if self.account.user_agent:
            opts.add_argument(f'--user-agent={self.account.user_agent}')
        opts.add_argument(f'--proxy-server={self.account.proxy}')
        self.driver = Chrome()
        self.driver.maximize_window()

    def login(self) -> bool:
        try:
            self.driver.get('https://twitter.com/i/flow/login')
            self.__wait_for_element_to_click('//input[@name="text"]').send_keys(self.account.username)
            self.driver.find_element(By.XPATH, '//div[6]/div/span/span').click()
            self.__wait_for_element_to_click('//input[@type="password"]').send_keys(self.account.password)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                self.driver.find_element(By.XPATH, '//div[2]/div/div[1]/div/div/div/span/span')
            )).click()
            sleep(1)
            return True
        except Exception as error:
            logger.exception(error)
            return False

    def home_page(self) -> NoReturn:
        url = f'https://twitter.com/home'
        self.driver.get(url)

    def __wait_for_element_to_click(self, xpath, timeout: int = 10) -> Optional[WebElement]:
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element

    def tweet(self, tweet: Post) -> bool:
        text_input_field = '//div[@aria-controls="typeaheadDropdownWrapped-0"]'
        photo_input = '//input[@data-testid="fileInput"]'
        tweet_button_span = '//div[@data-testid="tweetButtonInline"]/div/span/span'
        try:
            text_input_element = self.__wait_for_element_to_click(text_input_field)
            for char in tweet.text:
                text_input_element.send_keys(char)
            self.driver.find_element(By.XPATH, photo_input).send_keys(tweet.photo_path)
            tweet_button_element = self.driver.find_element(By.XPATH, tweet_button_span)
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            sleep(1)
            tweet_button_element.click()
            return True
        except Exception as error:
            logger.exception(error)
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
