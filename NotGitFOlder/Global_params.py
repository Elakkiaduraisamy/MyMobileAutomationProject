import os
import json
import pandas as pd
import threading

class GlobalParams:
    def __init__(self, excel_file=None, config_file=None):
        self.platform_name = threading.local()
        self.udid = threading.local()
        self.device_name = threading.local()
        self.system_port = threading.local()
        self.chrome_driver_port = threading.local()
        self.wda_local_port = threading.local()
        self.webkit_debug_proxy_port = threading.local()
        self.no_reset = threading.local()
        self.full_reset = threading.local()
        self.appium_server_url = threading.local()

        self.params_from_excel = self.read_params_from_excel(excel_file) if excel_file else {}
        self.params_from_config = self.read_params_from_config(config_file) if config_file else {}

    def read_params_from_excel(self, file_path):
        """Read parameters from an Excel file."""
        try:
            df = pd.read_excel(file_path)
            params = df.to_dict(orient='records')[0]  # Assuming single row of configuration
            return params
        except Exception as e:
            print(f"Failed to read from Excel file: {e}")
            return {}

    def read_params_from_config(self, file_path):
        """Read parameters from a JSON configuration file."""
        try:
            with open(file_path, 'r') as file:
                params = json.load(file)
            return params
        except Exception as e:
            print(f"Failed to read from JSON configuration file: {e}")
            return {}

    def get_param(self, key, default):
        """Get parameter value from Excel, config file, environment variable or return default."""
        return (self.params_from_excel.get(key) or
                self.params_from_config.get(key) or
                os.getenv(key) or
                default)

    def set_platform_name(self, platform_name):
        self.platform_name.value = platform_name

    def get_platform_name(self):
        return getattr(self.platform_name, 'value', None)

    def set_udid(self, udid):
        self.udid.value = udid

    def get_udid(self):
        return getattr(self.udid, 'value', None)

    def set_device_name(self, device_name):
        self.device_name.value = device_name

    def get_device_name(self):
        return getattr(self.device_name, 'value', None)

    def set_system_port(self, system_port):
        self.system_port.value = system_port

    def get_system_port(self):
        return getattr(self.system_port, 'value', None)

    def set_chrome_driver_port(self, chrome_driver_port):
        self.chrome_driver_port.value = chrome_driver_port

    def get_chrome_driver_port(self):
        return getattr(self.chrome_driver_port, 'value', None)

    def set_wda_local_port(self, wda_local_port):
        self.wda_local_port.value = wda_local_port

    def get_wda_local_port(self):
        return getattr(self.wda_local_port, 'value', None)

    def set_webkit_debug_proxy_port(self, webkit_debug_proxy_port):
        self.webkit_debug_proxy_port.value = webkit_debug_proxy_port

    def get_webkit_debug_proxy_port(self):
        return getattr(self.webkit_debug_proxy_port, 'value', None)

    def set_no_reset(self, no_reset):
        self.no_reset.value = no_reset

    def get_no_reset(self):
        return getattr(self.no_reset, 'value', None)

    def set_full_reset(self, full_reset):
        self.full_reset.value = full_reset

    def get_full_reset(self):
        return getattr(self.full_reset, 'value', None)

    def set_appium_server_url(self, appium_server_url):
        self.appium_server_url.value = appium_server_url

    def get_appium_server_url(self):
        return getattr(self.appium_server_url, 'value', None)

    def initialize_global_params(self):
        self.set_platform_name(self.get_param('PLATFORM_NAME', 'Android'))
        self.set_udid(self.get_param('UDID', '<enter_device_udid_here>'))
        self.set_device_name(self.get_param('DEVICE_NAME', 'OnePlus'))
        self.set_no_reset(self.get_param('NO_RESET', 'true'))
        self.set_full_reset(self.get_param('FULL_RESET', 'false'))
        self.set_appium_server_url(self.get_param('APPIUM_SERVER_URL', 'http://127.0.0.1:4723/wd/hub'))

        if self.get_platform_name() == 'Android':
            self.set_system_port(self.get_param('SYSTEM_PORT', '10000'))
            self.set_chrome_driver_port(self.get_param('CHROME_DRIVER_PORT', '11000'))
        elif self.get_platform_name() == 'iOS':
            self.set_wda_local_port(self.get_param('WDA_LOCAL_PORT', '10001'))
            self.set_webkit_debug_proxy_port(self.get_param('WEBKIT_DEBUG_PROXY_PORT', '11001'))
        else:
            raise ValueError("Invalid Platform Name!")

# Example usage
if __name__ == '__main__':
    params = GlobalParams(excel_file='config.xlsx', config_file='config_server.json')
    params.initialize_global_params()
    print("Platform Name:", params.get_platform_name())
    print("UDID:", params.get_udid())
    print("Device Name:", params.get_device_name())
    print("Appium Server URL:", params.get_appium_server_url())
    if params.get_platform_name() == 'Android':
        print("System Port:", params.get_system_port())
        print("Chrome Driver Port:", params.get_chrome_driver_port())
    elif params.get_platform_name() == 'iOS':
        print("WDA Local Port:", params.get_wda_local_port())
        print("Webkit Debug Proxy Port:", params.get_webkit_debug_proxy_port())
