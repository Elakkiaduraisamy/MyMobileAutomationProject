from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.appium_utilities import swipe_with_action_chains_using_coordinates, swipe_down, scroll_to_element
from utils.logger import logger


class IOSProductPage:
    def __init__(self, driver, wait):
        self.expected_product_name = None
        print("IOS page is used in product page")
        self.driver = driver
        self.wait = wait
        self.select_product_locator = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "test-Item '
                                                                 'title"`][1]')
        self.navigated_product_page_title_locator = (AppiumBy.IOS_PREDICATE, 'name == "test-BACK TO PRODUCTS"')
        self.product_title_locator = (AppiumBy.IOS_PREDICATE, 'name == "Sauce Labs Backpack"')
        self.product_description_locator = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == '
                                                                      '"carry.allTheThings() with the sleek, '
                                                                      'streamlined Sly Pack that melds uncompromising '
                                                                      'style with unequaled laptop and tablet '
                                                                      'protection."`]')
        self.product_price_locator = (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="test-Price"]')
        self.add_to_cart_locator = (AppiumBy.IOS_PREDICATE, 'name == "test-ADD TO CART"')
        self.remove_from_cart_locator = (AppiumBy.IOS_PREDICATE, 'name == "test-REMOVE"')
        self.cpy_right_locator = (AppiumBy.IOS_PREDICATE, 'name == "© 2024 Sauce Labs. All Rights Reserved."')
    def user_selects_products(self):
        try:
            logger.info("Trying to find product to select: ")
            select_product = self.wait.until(EC.presence_of_element_located(self.select_product_locator))
            self.expected_product_name = select_product.get_attribute("value")
            print(self.expected_product_name)
            select_product.click()
        except (NoSuchElementException, TimeoutException):
            logger.info("Product is not selected")

    def user_navigate_products_page(self):

        navigated_product_page_title = None
        try:
            logger.info("Trying to find title of product page  selected ")
            navigated_product_page_title = self.wait.until(
                EC.presence_of_element_located(self.navigated_product_page_title_locator))
        except (NoSuchElementException, TimeoutException):
            logger.info("product page is not displayed")
        logger.info("Trying to find title of selected products page")
        actual_navigated_page_title = navigated_product_page_title.get_attribute("label")
        print(actual_navigated_page_title)
        assert (actual_navigated_page_title == "BACK TO PRODUCTS")

    def verify_product_page(self):
        product_page_name = None
        self.driver.implicitly_wait(20)
        try:
            logger.info("Trying to find title of product selected ")
            product_page_name = self.wait.until(EC.presence_of_element_located(self.product_title_locator))
        except (NoSuchElementException, TimeoutException):
            logger.info("product page is not displayed")
        actual_product_title = product_page_name.get_attribute('name')
        logger.info(" Verified - title of the product selected")
        assert (actual_product_title == self.expected_product_name)

    def get_product_price(self):
        product_description = None
        product_price = None
        self.driver.implicitly_wait(1000)
        try:
            logger.info("Trying to find description of product selected ")
            product_description = self.wait.until(EC.presence_of_element_located(self.product_description_locator))
        except (NoSuchElementException, TimeoutException):
            logger.info("product page is not displayed")

        actual_product_description = product_description.get_attribute('name')
        print(actual_product_description)
        logger.info("Trying to find product price")
        try:
            product_price = self.wait.until(EC.presence_of_element_located(self.product_price_locator))
        except TimeoutException:
            logger.inf("Product price element not found")
            raise

        self.driver.implicitly_wait(20)

        actual_product_price = product_price.get_attribute('label')
        logger.info(" after verify - title of the product")
        assert "carry.allTheThings()" in actual_product_description
        assert actual_product_price == '$29.99'
        print(actual_product_price)

    def add_to_cart(self):
        logger.info("Clicking the add to cart button")
        swipe_down(self.driver)
        try:
            add_to_cart = self.wait.until(EC.presence_of_element_located(self.add_to_cart_locator))
            add_to_cart.click()

            remove_button = self.wait.until(EC.presence_of_element_located(self.remove_from_cart_locator))
            if remove_button.is_enabled:
                remove_button.click()

            add_to_cart = self.wait.until(EC.presence_of_element_located(self.add_to_cart_locator))
            add_to_cart.click()
            logger.info("Product selected is added to the cart")

        except NoSuchElementException:
            logger.info("add to cart button is not found")
            raise

    def social_media_copyright_links(self):
        cpy_right_string = None
        self.driver.implicitly_wait(50)
        logger.info(" scrolling to find the copy rights below the app")
        try:
            print("inside scroll to element method")
            scroll_to_element(self.driver,self.cpy_right_locator,"down")
            cpy_right = self.wait.until(EC.presence_of_element_located(self.cpy_right_locator))
            cpy_right_string = cpy_right.get_attribute("value")
            print(cpy_right_string)
        except (NoSuchElementException, TimeoutException):
            logger.info("copyrights is not found")

        assert "© 2024 Sauce Labs." in cpy_right_string
        logger.info("copy rights are found below the app")


