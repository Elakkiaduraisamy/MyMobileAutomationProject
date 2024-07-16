from appium.webdriver.common.appiumby import AppiumBy
from utils.appium_utilities import element_click, scrolldown_to_element_click, switch_to_webview, switch_to_native, \
    swipe_with_action_chains_using_coordinates


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def click_search(self):
        search_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search')
        element_click(self.driver, (AppiumBy.ACCESSIBILITY_ID, 'Search'))

    def verify_search_bar(self):
        actual_title = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search Bar').text
        assert actual_title == "Search Bar", f"Expected title 'Search Bar', but got '{actual_title}'"

    def navigate_back(self):
        back_button = self.driver.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="UICatalog"]')
        element_click(self.driver, (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="UICatalog"]'))

    def verify_uicatalog(self):
        actual_title = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'UICatalog').text
        assert actual_title == "UICatalog", f"Expected title 'UICatalog', but got '{actual_title}'"

    def swipe(self, direction):
        swipe_with_action_chains_using_coordinates(self.driver, direction)

    def scroll_to_webview(self):
        webview_element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Web View")
        scrolldown_to_element_click(self.driver, (AppiumBy.ACCESSIBILITY_ID, "Web View"))

    def switch_to_webview(self):
        switch_to_webview(self.driver)

    def switch_to_native(self):
        switch_to_native(self.driver)
