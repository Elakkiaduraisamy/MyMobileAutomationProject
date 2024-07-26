from behave import given, when, then
from utils.logger import logger
from pages.login_page import LoginPage  # Assuming LoginPage is in the correct module
from webdriver.webdriver_setup import WebDriverSetup


@given('the app is set up')
def step_given_app_is_set_up(context):
    logger.info("Setting up WebDriver")
    platform_name = context.config.userdata.get('platform', 'iOS')
    context.webdriver_init = WebDriverSetup(context)
    context.login_page = LoginPage(context.driver, context.input_platform_name)


@when('the user logs in with standard credentials')
def step_when_user_logs_in_with_standard_credentials(context):
    logger.info("Starting login with standard credentials")
    context.login_page.login_with_standard_user()


@then('the user should be logged in successfully')
def step_then_user_should_be_logged_in_successfully(context):
    logger.info("Verifying user is logged in or not ")
    context.login_page.is_user_logged_in()


@given(u'user is logged in')
def step_impl(context):
    context.login_page = LoginPage(context.driver, context.input_platform_name)
    logger.info("user is already in login page")


@when(u'the user clicks log out')
def step_user_clicks_log_out(context):
    logger.info("User tries to logout ")
    context.login_page.user_log_out()


@then(u'user logs out and login page is shown')
def step_user_navigates_login_page(context):
    logger.info("User landed in login page ")
    context.login_page.verify_login_page()


@when(u'the user logs in with wrong user credentials')
def step_impl(context):
    context.login_page.login_with_wrong_user()


@then(u'the user should able to see error message')
def step_impl(context):
    context.login_page.verify_wrong_error_msg()
