from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import logger


class IOSLoginPage:
    def __init__(self, driver, wait):
        print("IOS page is used in login page")
        self.driver = driver
        self.wait = wait
        self.standard_user_link_locator_ios_predicate = (AppiumBy.IOS_PREDICATE, 'name == "test-standard_user"')
        self.login_button_locator = (AppiumBy.XPATH, '//XCUIElementTypeOther[@name="test-LOGIN"]')
        self.actual_title_image_locator = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == '
                                                                     '"PRODUCTS"`]')

    def login_with_standard_user(self):
        standard_user_link = None
        try:
            logger.info("Trying to find element by ios predicate: 'test-standard_user'")
            standard_user_link = self.wait.until(EC.presence_of_element_located(
                self.standard_user_link_locator_ios_predicate))
        except (NoSuchElementException, TimeoutException):
            logger.warning("Element not found with  ios predicate: 'test-standard_user'")

        standard_user_link.click()
        logger.info("trying to find login button")
        login_button = self.wait.until(EC.presence_of_element_located(self.login_button_locator))
        login_button.click()
        self.driver.implicitly_wait(10)

    def is_user_logged_in(self):
        print("getting the title of the page")
        logger.info("getting the title of the page")
        actual_title_image = self.wait.until(EC.presence_of_element_located(self.actual_title_image_locator))

        actual_title = actual_title_image.get_attribute("name")
        print(actual_title)

        assert actual_title == "PRODUCTS"
