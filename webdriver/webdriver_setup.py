import json
import os

from appium import webdriver
from utils.appium_utilities import start_appium_server, launch_appium_options, load_config


class WebDriverSetup:
    def __init__(self, config_file='config/config.json'):
        config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
        self.config = load_config(config_path)
        self.appium_service = None
        self.driver = None

    def setup_driver(self):
        self.appium_service = start_appium_server(self.config)
        options = launch_appium_options(self.config)
        if options is None:
            raise Exception("Failed to create Appium options")

        self.driver = webdriver.Remote(self.config['appium_server_url'], options=options)
        return self.driver

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
        if self.appium_service:
            self.appium_service.stop()
