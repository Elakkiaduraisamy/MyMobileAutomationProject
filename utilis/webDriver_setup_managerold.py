
from utilis.appium_utilities import *
''' 
   options.set_capability('browserName', 'Safari')
'''

def main():
    appium_service = start_appium_server()
    appium_server_url = 'http://127.0.0.1:4723'

    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'apps', 'MyRNDemoApp.app'))
    # app_path1 = "../apps/MyRNDemoApp.app/MyRNDemoApp"
    options = launch_appium_options(app_path)
 # appium_server_url2 = 'http://localhost:4723/wd/hub'  # Ensure the correct endpoint

    driver = webdriver.Remote(appium_server_url, options.to_capabilities())
    print("App installed successfully")

    # Verify the app is installed
    is_installed = is_app_installed(driver,'com.example.apple1-samplecode.UICatalog')
    print(f"Is app installed: {is_installed}")

    #click on a element using id
    clickelement_name_locator = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Search')
    element_click(driver,clickelement_name_locator)
    actual_title = driver.find_element(MobileBy.ACCESSIBILITY_ID,'Search Bar')
    assert actual_title == "Search Bar"

    #navigate back to main page
    element_click(driver,driver.find_element(AppiumBy.XPATH, 'UIKITCatalog'))
    actual_title = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Search Bar')
    assert actual_title == "UIKITCatalog"

   # swipe the screen in different direction
    swipe_with_action_chains_using_coordinates(driver, 'up')
    swipe_with_touch_action_using_coordinates(driver, 'down')

   # scroll to find the webview element
    webview_element_locator = driver.find_element(MobileBy.ACCESSIBILITY_ID, "Web View")
    scrolldown_to_element_click(driver, webview_element_locator)

    #switch to webview and back to native app
    switch_to_webview(driver)

    # Function to switch context to native app
    switch_to_native(driver)

    #App in the background
    driver.background_app(-1)

    # perform the left and right swipe on the phone
    swipe_with_touch_action_using_coordinates(driver, 'right')
    swipe_with_touch_action_using_coordinates(driver, 'left')

     # Close the session
    driver.quit()

    #End the server session
    appium_service.stop


"""
    # Open a browser and navigate to a webpage
   // driver.get('https://www.google.com')

    #Perform any interactions or validations here for web applications
    print("Title of the page is:", driver.title)
"""


if __name__ == '__main__':
    main()
