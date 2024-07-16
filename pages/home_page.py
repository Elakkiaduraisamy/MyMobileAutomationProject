from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def click_search(self):
        search_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search')
        search_button.click()

    def verify_search_bar(self):
        actual_title = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search Bar').text
        assert actual_title == "Search Bar", f"Expected title 'Search Bar', but got '{actual_title}'"

    def navigate_back(self):
        back_button = self.driver.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="UICatalog"]')
        back_button.click()

    def verify_uicatalog(self):
        actual_title = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'UICatalog').text
        assert actual_title == "UICatalog", f"Expected title 'UICatalog', but got '{actual_title}'"

    def scroll_to_webview(self):
        webview_element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Web View")
        self.driver.execute_script("mobile: scroll", {"direction": "down"})
        webview_element.click()

    def switch_to_webview(self):
        contexts = self.driver.contexts
        for context in contexts:
            if 'WEBVIEW' in context:
                self.driver.switch_to.context(context)
                return
        raise Exception("No WEBVIEW context found")

    def switch_to_native(self):
        self.driver.switch_to.context('NATIVE_APP')

    def swipe(self, direction):
        window_size = self.driver.get_window_size()
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

        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME, 'body'), start_x, start_y)
        actions.click_and_hold()
        actions.move_by_offset(end_x - start_x, end_y - start_y)
        actions.release()
        actions.perform()
