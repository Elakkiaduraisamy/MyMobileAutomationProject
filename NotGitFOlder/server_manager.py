import threading
import time
import json
from typing import List, Dict
from appium.webdriver.appium_service import AppiumService
from NotGitFOlder.log import setup_logger # Import the logging setup function
from NotGitFOlder.webdriver_setup_manager import WebDriverSetup

# Import the WebDriverSetup class

# Thread-local storage for server instances and loggers
thread_local = threading.local()


class AppiumServerManager:
    def __init__(self, config_file: str, excel_file: str = None):
        self.servers = self.read_config(config_file)
        self.excel_file = excel_file
        self.config_file = config_file

    def read_config(self, config_file: str) -> List[Dict]:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config.get('servers', [])

    def start_server(self, index: int, log_file: str, **kwargs):
        """Start an individual Appium server instance."""
        service = AppiumService()
        args = [
            '--address', kwargs.get('address', '127.0.0.1'),
            '--port', str(kwargs['port']),
            '--log-level', kwargs.get('log_level', 'info'),
            '--base-path', kwargs.get('base_path', '/wd/hub'),
            '--session-override' if kwargs.get('session_override', False) else '',
            '--relaxed-security' if kwargs.get('relaxed_security', False) else ''
        ]
        # Filter out empty strings
        args = [arg for arg in args if arg]

        # Setup logger for this thread
        logger = setup_logger(f'AppiumServerManager_{index}', log_file)
        thread_local.logger = logger

        try:
            logger.info(f'Starting Appium server with args: {args}')
            service.start(args=args)
            while not service.is_running:
                logger.debug('Waiting for Appium server to start...')
                time.sleep(1)
            logger.info(f'Appium server started on port {kwargs["port"]}')
            # Store the service in thread-local storage
            if not hasattr(thread_local, 'services'):
                thread_local.services = []
            thread_local.services.append(service)

            # Pass the Appium server URL to WebDriverSetup
            appium_server_url = f"http://{kwargs.get('address', '127.0.0.1')}:{kwargs['port']}/wd/hub"
            self.initialize_webdriver(appium_server_url)

        except Exception as e:
            logger.error(f'Failed to start Appium server on port {kwargs["port"]}: {e}')
            raise

    def initialize_webdriver(self, appium_server_url):
        """Initialize WebDriver session using WebDriverSetup."""
        webdriver_setup = WebDriverSetup(excel_file=self.excel_file, config_file=self.config_file)
        driver = webdriver_setup.start_webdriver_session(appium_server_url, app_path='path/to/your/app',
                                                         app_activity='your.app.activity')
        thread_local.driver = driver

    def start(self):
        """Start all Appium server instances in parallel."""
        threads = []
        for index, server in enumerate(self.servers):
            log_file = f'appium_server_{server["port"]}.log'
            thread = threading.Thread(target=self.start_server, args=(index, log_file), kwargs=server)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def stop(self):
        """Stop all Appium server instances."""
        if hasattr(thread_local, 'services'):
            for service in thread_local.services:
                if service.is_running:
                    service.stop()
                    thread_local.logger.info(f'Appium server stopped on port {service.service_url}')

        # Quit WebDriver sessions
        if hasattr(thread_local, 'driver'):
            thread_local.driver.quit()
            thread_local.logger.info(f'WebDriver session terminated')
