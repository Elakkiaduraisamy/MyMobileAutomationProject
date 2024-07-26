import logging
import time

from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utils.logger import logger
from utils.config_loader import load_config


def start_appium_server(config):
    print(config)
    appium_service = AppiumService()
    appium_service.start(args=[
        '--address', config['appium_server_address'],
        '--port', config['appium_server_port'],
        '--log', config['log_file_path'],  # Add the log argument here
        '--log-level', config['log_level'],
        '--log-timestamp',
        '--local-timezone'
    ])

    timeout = 120
    start_time = time.time()
    while not appium_service.is_running and (time.time() - start_time) < timeout:
        time.sleep(1)

    if appium_service.is_running:
        logger.info('Appium server is running')
    else:
        logger.error('Failed to start Appium server within the timeout')

    return appium_service


"""
def launch_appium_options(platform_config, user_passed_platform_name, config):
    
        try:
            options = XCUITestOptions()
            options.set_capability('platformName', config['platform_name'])
            options.set_capability('platformVersion', config['platform_version'])
            options.set_capability('deviceName', config['device_name'])
            options.set_capability('automationName', config['automation_name'])
            options.set_capability('app', config['app_path'])
            options.set_capability('wdaLaunchTimeout', 120000)
            options.set_capability('udid', config['udid'])
            options.set_capability('bundleId', config['bundle_id'])
            options.no_reset = True

    try:
        if user_passed_platform_name'.lower()] == 'ios':
            options = XCUITestOptions()
            options.set_capability('platformName', platform_config['platform_name'])
            options.set_capability('platformVersion', platform_config['platform_version'])
            options.set_capability('deviceName', platform_config['device_name'])
            options.set_capability('automationName', platform_config['automation_name'])
            options.set_capability('app', platform_config['app_path'])
            options.set_capability('wdaLaunchTimeout', 120000)
            options.set_capability('bundleId', platform_config['bundle_id'])
            options.set_capability('wdaLocalPort', platform_config['wda_local_port'])
            options.set_capability('useNewWDA', True)
            options.set_capability('xcodeOrgId', platform_config['xcode_org_id'])
            options.set_capability('xcodeSigningId', platform_config['xcode_signing_id'])
            options.set_capability('resetOnSessionStartOnly', True)
        elif config['user_passed_platform_name'.lower()] == 'android':
            options = UiAutomator2Options()
            options.set_capability('platformName', platform_config['platform_name'])
            options.set_capability('platformVersion', platform_config['platform_version'])
            options.set_capability('deviceName', platform_config['device_name'])
            options.set_capability('automationName', platform_config['automation_name'])
            options.set_capability('app', platform_config['app_path'])
            options.set_capability('appPackage', platform_config['app_package'])
            options.set_capability('appActivity', platform_config['app_activity'])
            options.set_capability('newCommandTimeout', 300)
        else:
            raise ValueError(f"Unsupported platform: {config['platform_name']}")

        logger.info(f"Appium options created: {options}")
        return options
    except Exception as e:
        logger.error(f"Error in creating Appium options: {e}")
        return None
"""


def launch_appium_options(platform_config, platform_name):
    print("entering the launch option method")
    try:
        if platform_name.lower() == 'ios':
            options = XCUITestOptions()
            options.set_capability('platformName', platform_config['platform_name'])
            options.set_capability('platformVersion', platform_config['platform_version'])
            options.set_capability('deviceName', platform_config['device_name'])
            options.set_capability('automationName', platform_config['automation_name'])
            options.set_capability('app', platform_config['app_path'])
            options.set_capability('wdaLaunchTimeout', 120000)
            options.set_capability('bundleId', platform_config['bundle_id'])
            options.set_capability('resetOnSessionStartOnly', False)
        elif platform_name.lower() == 'android':
            options = UiAutomator2Options()
            options.set_capability('platformName', platform_config['platform_name'])
            options.set_capability('platformVersion', platform_config['platform_version'])
            options.set_capability('deviceName', platform_config['device_name'])
            options.set_capability('automationName', platform_config['automation_name'])
            options.set_capability('app', platform_config['app_path'])
            options.set_capability('appPackage', platform_config['app_package'])
            options.set_capability('appActivity', platform_config['app_activity'])
            options.set_capability('newCommandTimeout', 300)
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")

        logger.info(f"Appium options created: {options}")
        return options
    except Exception as e:
        logger.error(f"Error in creating Appium options: {e}")
        return None


def is_app_installed(driver, bundle_id):
    try:
        result = driver.execute_script('mobile: isAppInstalled', {'bundleId': bundle_id})
        return result
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False


def enter_text(self, locator, text, timeout=10):
    element = self.find_element(*locator, timeout)
    element.clear()
    element.send_keys(text)
    return element


def element_click(driver, locator, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        print("element located")
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element = driver.find_element(*locator)
        element.click()
        logger.info(f"Clicked on element: {locator}")
    except TimeoutException:
        logger.error(f"Timeout: Element not clickable after {timeout} seconds: {locator}")
        raise
    except NoSuchElementException:
        logger.error(f"Error: Element not found: {locator}")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def scrolldown_to_element_click(driver, locator):
    while True:
        try:
            element_click(driver, locator)
            break
        except (TimeoutException, NoSuchElementException):
            driver.execute_script("mobile: scroll", {"direction": "down"})


def switch_to_webview(driver):
    contexts = driver.contexts
    logger.info(f"Available contexts: {contexts}")
    for context in contexts:
        if 'WEBVIEW' in context:
            driver.switch_to.context(context)
            logger.info(f"Switched to context: {context}")
            return
    raise Exception("No WEBVIEW context found")


def switch_to_native(driver):
    driver.switch_to.context('NATIVE_APP')
    logger.info("Switched to context: NATIVE_APP")


def swipe_with_action_chains_using_coordinates(driver, direction):
    logger.info("i am in swipe method")
    window_size = driver.get_window_size()
    print(window_size)
    width = window_size['width']
    height = window_size['height']

    start_x = width / 2
    start_y = height / 2
    end_x = start_x
    end_y = start_y
    start_x = width / 2
    start_x = width / 2
    print(start_x)
    if direction == 'up':
        end_y = start_y - (height / 4)
    elif direction == 'down':
        end_y = start_y + (height / 4)
    elif direction == 'left':
        end_x = start_x - (width / 4)
    elif direction == 'right':
        end_x = start_x + (width / 4)
    else:
        raise ValueError("Invalid direction: choose from 'up', 'down', 'left', 'right'")

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), start_x, start_y)
    actions.click_and_hold()
    actions.move_by_offset(end_x - start_x, end_y - start_y)
    actions.release()
    actions.perform()
    logger.info(f"Swiped {direction}")


def swipe_down(driver, duration=800):
    """
    Swipe down the screen.
    param driver: The WebDriver instance.
    param duration: Duration of the swipe in milliseconds.
    """
    size = driver.get_window_size()
    start_x = size['width'] // 2
    start_y = int(size['height'] * 0.2)
    end_y = int(size['height'] * 0.05)

    actions = ActionChains(driver)
    pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

    # Perform the swipe action
    actions = ActionChains(driver)
    pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

    # Perform the swipe action
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down(button=0)
    actions.w3c_actions.pointer_action.pause(duration / 1000)  # duration should be in seconds
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.pointer_up(button=0)
    actions.perform()


def scroll_to_element(driver, element_locator,direction):
    driver.execute_script('mobile: scroll', {"direction": direction})
    try:
        element = driver.find_element(*element_locator)
    except:
        driver.execute_script('mobile: scroll', {"direction": direction})
        element = driver.find_element(*element_locator)
    return element


def uninstall_app(driver, bundle_id):
    try:
        driver.remove_app(bundle_id)
        logger.info(f"App with bundleId {bundle_id} uninstalled successfully")
    except Exception as e:
        logger.error(f"An error occurred while uninstalling the app: {e}")


def install_app(driver, app_path):
    try:
        driver.install_app(app_path)
        logger.info(f"App at {app_path} installed successfully")
    except Exception as e:
        logger.error(f"An error occurred while installing the app: {e}")
