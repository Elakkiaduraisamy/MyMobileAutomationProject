import os
from appium import webdriver
from utils.appium_utilities import (
    start_appium_server,
    launch_appium_options,
    uninstall_app,
    install_app,
    is_app_installed
)
from utils.logger import logger
from utils.config_loader import load_config


class WebDriverSetup:
    def __init__(self, config_file='config/config.json'):
        config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
        self.config = load_config(config_path)
        self.appium_service = None
        self.driver = None

    def setup_driver(self):
        self.appium_service = start_appium_server(self.config)

        # Resolve the app path to an absolute path
        app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.config['app_path']))
        self.config['app_path'] = app_path
        logger.info(f"Resolved app path: {app_path}")

        options = launch_appium_options(self.config)
        if options is None:
            raise Exception("Failed to create Appium options")

        server_url = f"http://{self.config['appium_server_address']}:{self.config['appium_server_port']}"
        logger.info(f"Connecting to Appium server at {server_url}")
        self.driver = webdriver.Remote(server_url, options=options)

        # Uninstall and reinstall the app
        if is_app_installed(self.driver, self.config['bundle_id']):
            uninstall_app(self.driver, self.config['bundle_id'])
        install_app(self.driver, self.config['app_path'])
        return self.driver

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
        if self.appium_service:
            self.appium_service.stop()
