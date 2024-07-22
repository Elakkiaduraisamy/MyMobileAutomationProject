from behave import given, when, then
from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup
from pages.login_page import LoginPage  # Assuming LoginPage is in the correct module


@given('the app is set up')
def step_given_app_is_set_up(context):
    logger.info("Setting up WebDriver")
    platform_name = context.config.userdata.get('platform', 'iOS')  # Default to iOS if not specified
    context.webdriver_init = WebDriverSetup(context)
    context.login_page = LoginPage(context.driver, context.input_platform_name)


@when('the user logs in with standard credentials')
def step_when_user_logs_in_with_standard_credentials(context):
    logger.info("Starting login with standard credentials")
    context.login_page.login_with_standard_user()


@then('the user should be logged in successfully')
def step_then_user_should_be_logged_in_successfully(context):
    # Implement your verification step here, e.g., checking for a successful login
    # This could be checking for a specific element that appears on successful login
    logger.info("Verifying user is logged in")
    context.login_page.is_user_logged_in()


def after_all(context):
    logger.info("Tearing down WebDriver")
    context.webdriver_setup.teardown_driver()
