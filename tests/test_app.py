import unittest
import logging
from webdriver.webdriver_setup import WebDriverSetup
from pages.login_page import LoginPage
from utils.logger import setup_logger

logger = setup_logger()


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up WebDriver")
        cls.webdriver_setup = WebDriverSetup()
        cls.driver = cls.webdriver_setup.setup_driver()
        cls.login_page = LoginPage(cls.driver)

    def test_app_flow(self):
        logger.info("Starting test_app_flow")
        #self.login_page.double_click_to_open_app()
        self.login_page.login_with_standard_user()

    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down WebDriver")
        cls.webdriver_setup.teardown_driver()


if __name__ == '__main__':
    unittest.main()
