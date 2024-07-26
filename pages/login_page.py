from selenium.webdriver.support.ui import WebDriverWait
from pages.android.AndroidLoginPage import AndroidLoginPage
from pages.ios.iOSLoginPage import IOSLoginPage
import logging
from utils.logger import logger


class LoginPage:
    def __init__(self, driver, platform_name):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.platform_name = platform_name.lower()  # Increased timeout to 20 seconds

        if self.platform_name == 'android':
            logger.info("inside Login Page - Platform is Android")
            self.page = AndroidLoginPage(driver, self.wait)
        elif self.platform_name == 'ios':
            logger.info("inside Login Page - Platform is iOS")
            self.page = IOSLoginPage(driver, self.wait)
        else:
            raise ValueError(f"Unsupported platform: {self.platform_name}")

    def login_with_standard_user(self):
        self.page.login_with_standard_user()

    def is_user_logged_in(self):
        self.page.is_user_logged_in()

    def user_log_out(self):
        self.page.user_log_out()

    def verify_login_page(self):
        self.page.verify_login_page()

    def login_with_wrong_user(self):
        self.page.login_with_wrong_user()

    def verify_wrong_error_msg(self):
        self.page.verify_wrong_error_msg()
