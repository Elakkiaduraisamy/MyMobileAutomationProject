import json
import os
import subprocess
import sys

from selenium.common.exceptions import WebDriverException

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
    context.app_logger = logger
    if appconfig is None:
        context.app_logger.error("Failed to load configuration. Aborting test run.")
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

    webdriver_setup = WebDriverSetup(context)
    context.driver = webdriver_setup.setup_driver()


def before_scenario(context, scenario):
    print("entering before scenario")
    """ 
    if not hasattr(context, 'webdriver_setup'):
        context.app_logger.error(f"WebDriver setup is not initialized. Skipping scenario: {scenario.name}")
        return

    if context.app_platform_config is None:
        logger.error(f"Failed to get platform configuration for '{context.input_platform_name}'. Aborting test run.")
        return
"""
    if context.driver is None:
        context.app_logger.info(f"Setting up WebDriver for scenario: {scenario.name}")
        context.driver = context.webdriver_setup.setup_driver()

    context.allure_report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../reports'))
    if not os.path.exists(context.allure_report_dir):
        os.makedirs(context.allure_report_dir)


def after_scenario(context, scenario):
    context.app_logger.info(f"Finished scenario: {scenario.name}")

    """
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except WebDriverException as e:
            context.app_logger.error(f"Error during scenario WebDriver quit: {e}")
        finally:
            context.driver = None
"""


def after_all(context):
    logger.info("Tearing down after all tests ****")
    if hasattr(context, 'webdriver_setup') and context.webdriver_setup:
        logger.info("inside after_all hasattr condition")
        context.webdriver_setup.teardown_driver()
    else:
        logger.info("inside after_all else condition")
        # Close the simulator or emulator
        if context.app_platform_config['platform_name'].lower() == 'ios':
            shutdown_ios_simulator(context.app_platform_config['udid'])
        elif context.app_platform_config['platform_name'].lower() == 'android':
            shutdown_android_emulator()


def check_simulator_state(udid):
    try:
        output = subprocess.check_output(['xcrun', 'simctl', 'list', 'devices', '--json'])
        devices = json.loads(output)
        for runtime, sims in devices['devices'].items():
            for sim in sims:
                if sim['udid'] == udid:
                    logger.info("sim['state']" + sim['state'])
                    return sim['state']
    except Exception as e:
        logger.error(f"Failed to check simulator state: {e}")
    return None


def shutdown_ios_simulator(udid):
    state = check_simulator_state(udid)
    if state == 'Shutdown':
        logger.info(f"Simulator {udid} is already shut down.")
        return
    try:
        subprocess.check_call(['xcrun', 'simctl', 'shutdown', udid])
        logger.info(f"Simulator {udid} shut down successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to shut down the simulator: {e}")


def shutdown_android_emulator():
    try:
        subprocess.run(['adb', 'emu', 'kill'], check=True)
        logger.info("Android emulator has been shut down.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to shut down the emulator: {e}")
