from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
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
        self.menu_bar = (AppiumBy.XPATH, '//XCUIElementTypeOther[@name="Username Password LOGIN The currently '
                                         'accepted usernames for this application are (tap to autofill): '
                                         'standard_user locked_out_user problem_user And the password for all users '
                                         'is: secret_sauce Vertical scroll bar, 2 pages Horizontal scroll bar, '
                                         '1 page"]')
        self.login_out_locator = (AppiumBy.ACCESSIBILITY_ID, 'test-LOGOUT')
        self.login_title_locator = (AppiumBy.ACCESSIBILITY_ID, 'test-Username')

        self.wrong_user_link_locator = (AppiumBy.ACCESSIBILITY_ID, 'test-locked_out_user')
        self.error_message_locator = (AppiumBy.ACCESSIBILITY_ID, 'Sorry, this user has been locked out.')

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

    def user_log_out(self):
        self.driver.implicitly_wait(10)
        logger.info("trying ot logout")
        self.driver.execute_script('mobile: tap', {'x': 44, 'y': 65})
        logger.info("trying ot logout is clicked")

        """ 
        touch_action = TouchAction(self.driver)
        touch_action.tap(x=-117, y=0).perform()
        try:
            menu_bar = self.wait.until(EC.presence_of_element_located(self.menu_bar))
            menu_bar.click()
        except NoSuchElementException:
            logger.info("no menu bar found to logout")
            raise
        self.driver.implicitly_wait(10)
        logger.info("checking for logout button")
        
        """

        try:
            logout = self.wait.until(EC.presence_of_element_located(self.login_out_locator))
            logout.click()
            logger.info(" logout button is clicked")
        except NoSuchElementException:
            logger.info("no logout option is listed")
            raise

    def verify_login_page(self):
        try:
            login_title = self.wait.until(EC.presence_of_element_located(self.login_title_locator))
            login_page_field = login_title.get_attribute('value')
            print(login_page_field)
        except NoSuchElementException:
            logger.info("no user name field found, not in login page")
            raise

        assert login_page_field == 'Username'

    def login_with_wrong_user(self):
        wrong_user_link = None
        try:
            logger.info("Trying to find element by ios predicate: 'wrong user'")
            wrong_user_link = self.wait.until(EC.presence_of_element_located(
                self.wrong_user_link_locator))
        except (NoSuchElementException, TimeoutException):
            logger.warning("Element not found with  for wrong user'")

        wrong_user_link.click()
        logger.info("trying to find login button")
        login_button = self.wait.until(EC.presence_of_element_located(self.login_button_locator))
        login_button.click()
        self.driver.implicitly_wait(10)

    def verify_wrong_error_msg(self):
        actual_error_message = None
        error_message_text = None
        try:
            logger.info("Trying to find error message'")
            error_message= self.wait.until(EC.presence_of_element_located(
                self.error_message_locator))
            actual_error_message = error_message.get_attribute('value')
        except (NoSuchElementException, TimeoutException):
            logger.warning("Element not found with  ios predicate: 'test-standard_user'")

        assert actual_error_message == 'Sorry, this user has been locked out.'
