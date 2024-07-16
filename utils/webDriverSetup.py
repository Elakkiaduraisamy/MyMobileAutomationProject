from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import webdriver
import os
from appium.options.ios import XCUITestOptions
from utils.appiumUtilities import *


def main():
    appium_service = start_appium_server()
    appium_server_url = 'http://127.0.0.1:4723'

    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'apps', 'MyRNDemoApp.app'))
    print(f"App path: {app_path}")

    options = launch_appium_options(app_path)
    if options is not None:
        driver = None  # Initialize driver to None
        capabilities = options.to_capabilities()
        print(f"Appium capabilities: {capabilities}")
        print(f"Appium options: {options}")
        driver = webdriver.Remote(appium_server_url, options=options)
        print("App installed successfully")
        try:

            # Verify the app is installed
            is_installed = is_app_installed(driver, 'com.example.apple1-samplecode.UICatalog')
            print(f"Is app installed: {is_installed}")

            # Click on an element using accessibility ID
            search_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search')
            element_click(driver, (AppiumBy.ACCESSIBILITY_ID, 'Search'))

            # Verify the title after clicking
            actual_title = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search Bar').text
            assert actual_title == "Search Bar", f"Expected title 'Search Bar', but got '{actual_title}'"

            # Navigate back to main page
            back_button = driver.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="UICatalog"]')
            element_click(driver, (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="UICatalog"]'))
            actual_title = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'UICatalog').text
            assert actual_title == "UICatalog", f"Expected title 'UICatalog', but got '{actual_title}'"

            # Swipe the screen in different directions
            swipe_with_action_chains_using_coordinates(driver, 'up')
            swipe_with_action_chains_using_coordinates(driver, 'down')

            # Scroll to find the webview element and click it
            webview_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Web View")
            scrolldown_to_element_click(driver, (AppiumBy.ACCESSIBILITY_ID, "Web View"))

            # Switch to webview and back to native app
            switch_to_webview(driver)
            switch_to_native(driver)

            # Put the app in the background
            driver.background_app(-1)

            # Perform left and right swipe on the phone
            swipe_with_action_chains_using_coordinates(driver, 'right')
            swipe_with_action_chains_using_coordinates(driver, 'left')
        except Exception as e:
            print(f"Error : {e}")
            return
        finally:
            if driver:
                driver.quit()
            # End the server session
            appium_service.stop()
    else:
        print("Failed to create Appium options")
        return


if __name__ == '__main__':
    main()
