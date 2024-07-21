import os
import sys
from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup
from utils.config_loader import load_config, get_platform_config

# Add steps directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'steps')))


def before_all(context):
    logger.info("Initializing test run")
    context.driver = None  # Initialize driver to None
    context.appium_service = None  # Initialize appium service to None
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json'))
    print("envir config path: " + config_path)
    appconfig = load_config(config_path)
    context.appconfig = appconfig
    if appconfig is None:
        logger.error("Failed to load configuration. Aborting test run.")
        return

    input_platform_name = context.config.userdata.get('platform', 'iOS')  # Default to iOS if not specified
    context.input_platform_name = input_platform_name
    logger.info(f"Platform name: {input_platform_name}")

    app_platform_config = get_platform_config(appconfig, input_platform_name)
    context.app_platform_config = app_platform_config
    logger.info(f"Platform_config: {app_platform_config}")

    if app_platform_config is None:
        logger.error(f"Failed to get platform configuration for '{input_platform_name}'. Aborting test run.")
        return

    context.webdriver_setup = WebDriverSetup(context)


def before_scenario(context, scenario):
    if not hasattr(context, 'webdriver_setup'):
        logger.error(f"WebDriver setup is not initialized. Skipping scenario: {scenario.name}")
        return
    logger.info(f"Setting up WebDriver for scenario: {scenario.name}")
    context.driver = context.webdriver_setup.setup_driver()
    context.allure_report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../reports'))
    if not os.path.exists(context.allure_report_dir):
        os.makedirs(context.allure_report_dir)


def after_scenario(context, scenario):
    logger.info(f"Tearing down WebDriver for scenario: {scenario.name}")
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
        context.driver = None


def after_all(context):
    logger.info("Tearing down after all tests")
    if hasattr(context, 'webdriver_setup') and context.webdriver_setup:
        context.webdriver_setup.teardown_driver
