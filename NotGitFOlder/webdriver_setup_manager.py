from appium import webdriver
from NotGitFOlder.Global_params import GlobalParams
import threading

thread_local = threading.local()

class WebDriverSetup:
    def __init__(self, excel_file=None, config_file=None):
        self.global_params = GlobalParams(excel_file, config_file)
        self.global_params.initialize_global_params()

    def start_webdriver_session(self, appium_server_url, app_path=None, app_activity=None):
        platform_name = self.global_params.get_platform_name()

        if platform_name == 'Android':
            return self.get_android_driver(appium_server_url, app_path, app_activity)
        elif platform_name == 'iOS':
            return self.get_ios_driver(appium_server_url, app_path)
        else:
            raise ValueError("Invalid Platform Name!")

    def get_android_driver(self, appium_server_url, app_path, app_activity):
        caps = {
            'platformName': 'Android',
            'deviceName': self.global_params.get_device_name(),
            'udid': self.global_params.get_udid(),
            'app': app_path,
            'appActivity': app_activity,
            'noReset': self.global_params.get_no_reset(),
            'fullReset': self.global_params.get_full_reset()
        }
        thread_local.driver = webdriver.Remote(appium_server_url, caps)
        return thread_local.driver

    def get_ios_driver(self, appium_server_url, app_path):
        caps = {
            'platformName': 'iOS',
            'deviceName': self.global_params.get_device_name(),
            'udid': self.global_params.get_udid(),
            'app': app_path,
            'noReset': self.global_params.get_no_reset(),
            'fullReset': self.global_params.get_full_reset(),
            'wdaLocalPort': self.global_params.get_wda_local_port(),
            'webkitDebugProxyPort': self.global_params.get_webkit_debug_proxy_port()
        }
        thread_local.driver = webdriver.Remote(appium_server_url, caps)
        return thread_local.driver

    def quit_driver(self):
        if hasattr(thread_local, 'driver'):
            thread_local.driver.quit()

# Example usage
if __name__ == '__main__':
    setup = WebDriverSetup(excel_file='config.xlsx', config_file='config_server.json')
    driver = setup.start_webdriver_session(appium_server_url='http://127.0.0.1:4723/wd/hub', app_path='path/to/your/app', app_activity='your.app.activity')
    # Perform your tests here
    setup.quit_driver()
