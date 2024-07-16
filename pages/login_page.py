from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.appium_utilities import enter_text
import logging

logger = logging.getLogger('app_logger')


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def double_click_to_open_app(self):
        wait = WebDriverWait(self.driver, 20)

        # Locate the app icon or element to double-click
        app_icon = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                              '//XCUIElementTypeApplication[@name=" "]/XCUIElementTypeWindow[5]/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]')))

        # Perform a double-click action
        action = ActionChains(self.driver)
        action.double_click(app_icon).perform()
        logger.info("Double-clicked on the app icon to open the app")

    def login_with_standard_user(self):

        wait = WebDriverWait(self.driver, 25)  # Increased timeout to 20 seconds
        # Add detailed logs for element finding
        print('driver' ,self.driver)
        try:
            logger.info("Trying to find element by IOS_PREDICATE: 'test-standard_user'")
            standard_user_link = wait.until(
                EC.presence_of_element_located((AppiumBy.IOS_PREDICATE, 'name == "test-standard_user"')))
        except (NoSuchElementException, TimeoutException):
            logger.warning("Element not found with ACCESSIBILITY_ID: 'test-standard_user'. Trying by NAME.")
            try:
                standard_user_link = wait.until(EC.presence_of_element_located((AppiumBy.NAME, 'standard_user')))
            except (NoSuchElementException, TimeoutException):
                logger.error("Element not found with NAME: 'standard_user'. Trying by XPATH.")
                standard_user_link = wait.until(
                    EC.presence_of_element_located((AppiumBy.XPATH, '//*[@label="standard_user"]')))

        standard_user_link.click()

        login_button = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN')))
        login_button.click()
        print("getting the title of the page")
        logger.info("getting the title of the page")
        actual_title_image = wait.until(EC.presence_of_element_located(
            (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "PRODUCTS"`]')))

        actual_title = actual_title_image.get_attribute("name")
        logger.info("getting the title of the page:")
        assert actual_title == "PRODUCTS"
