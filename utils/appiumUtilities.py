from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium import webdriver
from appium.webdriver.appium_service import AppiumService


def start_appium_server():
    appium_service = AppiumService()
    appium_service.start(args=['--address', '127.0.0.1', '--port', '4723'])

    if appium_service.is_running:
        print('Appium server is running')

    return appium_service


def launch_appium_options(app_path):
    try:
        options = XCUITestOptions()
        options.set_capability('platformName', 'iOS')
        options.set_capability('platformVersion', '17.5')  # Specify the iOS version
        options.set_capability('deviceName', 'iPhone 15')  # Specify the device name
        options.set_capability('automationName', 'XCUITest')
        options.set_capability('app', app_path)
        options.set_capability('wdaLaunchTimeout', 120000)
        options.set_capability('udid', '1EAC3323-4716-4A35-8BC4-C3102B8AD09E')
        print(f"Appium options created: {options}")

        if not hasattr(options, 'to_capabilities'):
            raise AttributeError("XCUITestOptions object does not have 'to_capabilities' attribute")

        return options
    except Exception as e:
        print(f"Error in creating Appium options: {e}")
        return XCUITestOptions()


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


def switch_to_native(driver):
    driver.switch_to.context('NATIVE_APP')
    print("Switched to context: NATIVE_APP")


def swipe_with_action_chains_using_coordinates(driver, direction):
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
    actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), start_x, start_y)
    actions.click_and_hold()
    actions.move_by_offset(end_x - start_x, end_y - start_y)
    actions.release()
    actions.perform()
