from selenium.webdriver.support.ui import WebDriverWait
from pages.android.AndroidLoginPage import AndroidLoginPage
from pages.ios.iOSLoginPage import IOSLoginPage
import logging

from pages.ios.iOSProductPage import IOSProductPage
from utils.logger import logger


class ProductPage:
    def __init__(self, driver, platform_name):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.platform_name = platform_name.lower()  # Increased timeout to 20 seconds

        if self.platform_name == 'android':
            logger.info("inside product Page - Platform is Android")
            #self.page = AndroidProductPage(driver, self.wait)
        elif self.platform_name == 'ios':
            logger.info("inside product Page - Platform is iOS")
            self.page = IOSProductPage(driver, self.wait)
        else:
            raise ValueError(f"Unsupported platform: {self.platform_name}")

    def user_selects_products(self):
        self.page.user_selects_products()

    def user_navigate_products_page(self):
        self.page.user_navigate_products_page()

    def verify_product_page(self):
        self.page.verify_product_page()

    def get_product_price(self):
        self.page.get_product_price()

    def add_to_cart(self):
        self.page.add_to_cart()

    def social_media_copyright_links(self):
        self.page.social_media_copyright_links()
