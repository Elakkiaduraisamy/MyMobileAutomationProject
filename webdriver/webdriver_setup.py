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

from utils.config_loader import load_config, get_platform_config


class WebDriverSetup:

    def __init__(self, context):
        self.appconfig = context.appconfig
        self.input_platform_name = context.input_platform_name
        self.app_platform_config = context.app_platform_config
        self.appium_service = context.appium_service
        self.driver = context.driver

    def setup_driver(self):
        self.appium_service = start_appium_server(self.appconfig)
        print("print config: ")
        # Resolve the app path to an absolute path
        app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.app_platform_config['app_path']))
        self.app_platform_config['app_path'] = app_path
        logger.info(f"Resolved app path: {app_path}")
        options = launch_appium_options(self.app_platform_config, self.input_platform_name)
        if options is None:
            raise Exception("Failed to create Appium options")

        server_url = f"http://{self.appconfig['appium_server_address']}:{self.appconfig['appium_server_port']}"
        logger.info(f"Connecting to Appium server at {server_url}")
        self.driver = webdriver.Remote(server_url, options=options)
        print("driver is set for testing")
        self.driver.implicitly_wait(20)
        return self.driver

    def is_app_installed(self, bundle_id):
        try:
            result = self.driver.execute_script('mobile: isAppInstalled', {'bundleId': bundle_id})
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_config(self, key):
        return self.appconfig['key']

    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
        if self.appium_service:
            self.appium_service.stop()

        if self.input_platform_name == 'ios':
            self.shutdown_ios_simulator()
            # Close the Android emulator
        elif self.input_platform_name == 'android':
            self.shutdown_android_emulator()
        else:
            logger.error(f"Unsupported platform: {self.input_platform_name}")

    def shutdown_ios_simulator(self):
        try:
            ud_id = self.appconfig.get('udid')
            if ud_id:
                subprocess.run(['xcrun', 'simctl', 'shutdown', ud_id], check=True)
                logger.info(f"Simulator with UDID {ud_id} has been shut down.")
            else:
                logger.error("UDID is not provided in the config to shut down the simulator.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to shut down the simulator: {e}")

    def shutdown_android_emulator(self):
        try:
            device_name = self.app_platform_config.get('device_name')
            if device_name:
                subprocess.run(['adb', '-s', device_name, 'emu', 'kill'], check=True)
                logger.info(f"Emulator with device name {device_name} has been shut down.")
            else:
                logger.error("Device name is not provided in the config to shut down the emulator.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to shut down the emulator: {e}")
