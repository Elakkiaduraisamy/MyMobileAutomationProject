from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger


class AndroidLoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.standard_user_link_locator = (By.XPATH, '//android.widget.TextView[@text="standard_user"]')
        self.login_button_locator = (By.XPATH, '//android.view.ViewGroup[@content-desc="test-LOGIN"]')
        self.actual_title_image_locator = (By.XPATH, '//android.widget.TextView[@text="PRODUCTS"]')

    def login_with_standard_user(self):
        standard_user_link = None
        login_button = None

        try:
            logger.info("Trying to find element by android xpath: 'test-standard_user'")
            standard_user_link = self.wait.until(EC.presence_of_element_located(self.standard_user_link_locator))
        except (NoSuchElementException, TimeoutException):
            logger.warning("Element not found with XPATH: 'test-standard_user'. Trying by NAME.")

        standard_user_link.click()
        logger.info("trying to find login button")
        login_button = self.wait.until(EC.presence_of_element_located(self.login_button_locator))
        login_button.click()

    def is_user_logged_in(self):
        print("getting the title of the page")
        logger.info("getting the title of the page")
        actual_title_image = self.wait.until(EC.presence_of_element_located(self.actual_title_image_locator))

        actual_title = actual_title_image.get_attribute("name")
        print(actual_title)

        assert actual_title == "PRODUCTS"
