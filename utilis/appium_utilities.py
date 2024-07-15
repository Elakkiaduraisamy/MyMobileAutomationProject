import os
from telnetlib import EC

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.ios.xcuitest import app
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium import webdriver as selenium_webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from appium.options.common import AppiumOptions
from selenium import *

def start_appium_server():
    # Start Appium service
    appium_service = AppiumService()
    appium_service.start(args=['--address', '127.0.0.1', '--port', '4723'])

    # Check if Appium service is running
    if appium_service.is_running:
        print('Appium server is running')

    return appium_service

def launch_appium_options(app_path):
    options = XCUITestOptions()
    options.set_capability('platformName', 'iOS')
    options.set_capability('platformVersion', '17.5')  # Specify the iOS version
    options.set_capability('deviceName', 'iPhone 15')  # Specify the device name
    options.set_capability('automationName', 'XCUITest')
   # options.set_capability('app',app_path)
    options.set_capability('wdaLaunchTimeout', 120000)
    options.set_capability('udid', '248E0AF0-F804-43C1-B4F9-D3EAA68605C7')
    options.set_capability('bundleId', 'com.example.apple1-samplecode.UICatalog')
    return options

def is_app_installed(driver, bundle_id):
    try:
        result = driver.execute_script('mobile: isAppInstalled', {'bundleId': bundle_id})
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def element_click(driver, element_name, timeout=10):
    """
    Attempts to click on an element under specific conditions to handle simulator interactions.

    This method:
    - Waits for the element to be present, visible, and clickable.
    - Raises a TimeoutException if the element is not clickable within the specified timeout period.
    - Raises a NoSuchElementException if the element is not found.

    These exceptions help to explicitly identify issues in the script related to element interaction.
    args passed and its description:
    :driver: The Appium driver instance.
    :locator: The locator tuple for the element (By, value).
    :timeout: The maximum time to wait for the element to be clickable.
    :raises TimeoutException: If the element is not clickable within the timeout.
    :raises NoSuchElementException: If the element is not found.
"""
    try:
        # Wait for the element to be present and visible
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(element_name))
        # Wait for the element to be clickable
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element_name))
        # Find and click the element
        element = driver.find_element(*element_name)
        element.click()
        print(f"Clicked on element: {element_name}")
    except TimeoutException:
        print(f"Timeout: Element not clickable after {timeout} seconds: {element_name}")
        raise
    except NoSuchElementException:
        print(f"Error: Element not found: {element_name}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def scrolldown_to_element_click(driver, element_name):
    """
    Attempts to scroll and try to find the element and click

    raises TimeoutException, NoSuchElementException
    args passed and its description:
    :param driver:
    :param element_name:
    """
    while True:
        try:
            element_click(driver, element_name)
            break  # Break the loop if the element is found and clicked
        except (TimeoutException, NoSuchElementException):
            # If element is not found, perform a scroll
            driver.execute_script("mobile: scroll", {"direction": "down"})

# Function to switch context to webview
def switch_to_webview(driver):
    """
    This method helps to switch from native app to webview of the application
    and moves back to native
    Raises exceptions  and uses the args
    :param driver:
    :return:
    """
    # Get the available contexts
    contexts = driver.contexts
    print("Available contexts:", contexts)
    # Switch to the webview context
    for context in contexts:
        if 'WEBVIEW' in context:
            driver.switch_to.context(context)
            print(f"Switched to context: {context}")
            return
    raise Exception("No WEBVIEW context found")

# Function to switch context to native app
def switch_to_native(driver):
    driver.switch_to.context('NATIVE_APP')
    print("Switched to context: NATIVE_AP")

def swipe_with_action_chains_using_coordinates(driver, direction):
    """
    Perform swipe action using ActionChains.

    :param driver: The Appium driver instance.
    :param direction: The direction to swipe ('up', 'down', 'left', 'right').
    """
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    start_x = width / 2
    start_y = height / 2
    end_x = start_x
    end_y = start_y

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
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    actions.w3c_actions.pointer_action.pointer_up()
    actions.perform()


def swipe_with_touch_action_using_coordinates(driver, direction):
    """
    Perform swipe action using TouchAction.

    :param driver: The Appium driver instance.
    :param direction: The direction to swipe ('up', 'down', 'left', 'right').
    """
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    start_x = width / 2
    start_y = height / 2
    end_x = start_x
    end_y = start_y

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

    touch_action = TouchAction(driver)
    touch_action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()


