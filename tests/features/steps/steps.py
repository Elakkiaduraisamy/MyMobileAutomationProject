from behave import given, when, then
from pages.home_page import HomePage
from webdriver.webdriver_setup import WebDriverSetup


@given('the app is installed')
def step_impl(context):
    context.webdriver_setup = WebDriverSetup()
    context.driver = context.webdriver_setup.setup_driver()
    context.home_page = HomePage(context.driver)


@when('I click on the search button')
def step_impl(context):
    context.home_page.click_search()


@then('I should see the search bar')
def step_impl(context):
    context.home_page.verify_search_bar()


@then('I navigate back to the main page')
def step_impl(context):
    context.home_page.navigate_back()


@then('I should see the UI catalog')
def step_impl(context):
    context.home_page.verify_uicatalog()


@when('I swipe up')
def step_impl(context):
    context.home_page.swipe('up')


@when('I swipe down')
def step_impl(context):
    context.home_page.swipe('down')


@when('I scroll to the webview element')
def step_impl(context):
    context.home_page.scroll_to_webview()


@then('I should switch to the webview context')
def step_impl(context):
    context.home_page.switch_to_webview()


@then('I switch back to the native context')
def step_impl(context):
    context.home_page.switch_to_native()


@when('I swipe right')
def step_impl(context):
    context.home_page.swipe('right')


@when('I swipe left')
def step_impl(context):
    context.home_page.swipe('left')
