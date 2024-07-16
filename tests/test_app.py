import unittest
import logging
from webdriver.webdriver_setup import WebDriverSetup
from pages.home_page import HomePage
from utils.logger import setup_logger

logger = setup_logger()


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.webdriver_setup = WebDriverSetup()
        cls.driver = cls.webdriver_setup.setup_driver()
        cls.home_page = HomePage(cls.driver)

    def test_app_flow(self):
        logger.info("Starting test_app_flow")
        self.home_page.click_search()
        logger.info("Clicked search button")
        self.home_page.verify_search_bar()
        logger.info("Verified search bar")
        self.home_page.navigate_back()
        logger.info("Navigated back")
        self.home_page.verify_uicatalog()
        logger.info("Verified UI catalog")
        self.home_page.swipe('up')
        logger.info("Swiped up")
        self.home_page.swipe('down')
        logger.info("Swiped down")
        self.home_page.scroll_to_webview()
        logger.info("Scrolled to WebView")
        self.home_page.switch_to_webview()
        logger.info("Switched to WebView")
        self.home_page.switch_to_native()
        logger.info("Switched to native")
        self.home_page.swipe('right')
        logger.info("Swiped right")
        self.home_page.swipe('left')
        logger.info("Swiped left")
        logger.info("Completed test_app_flow")

    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down WebDriver")
        cls.webdriver_setup.teardown_driver()


if __name__ == '__main__':
    unittest.main()
