import os
import subprocess

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
        self.driver.implicitly_wait(40)
        return self.driver

    def is_app_installed(self, bundle_id):
        try:
            result = self.driver.execute_script('mobile: isAppInstalled', {'bundleId': bundle_id})
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_config(self,key):
        return self.config['key']

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
        if self.appium_service:
            self.appium_service.stop()

            # Close the iOS simulator
            if self.config['platform_name'].lower() == 'ios':
                self.shutdown_ios_simulator()

    def shutdown_ios_simulator(self):
        try:
            ud_id = self.config.get('udid')
            if ud_id:
                subprocess.run(['xcrun', 'simctl', 'shutdown', ud_id], check=True)
                logger.info(f"Simulator with UDID {ud_id} has been shut down.")
            else:
                logger.error("UDID is not provided in the config to shut down the simulator.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to shut down the simulator: {e}")
