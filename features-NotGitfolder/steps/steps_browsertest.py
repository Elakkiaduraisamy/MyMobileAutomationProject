from behave import given, when, then

from NotGitFOlder.server_manager import thread_local


@given('I open the browser')
def open_browser(context):
    # Use the driver from the thread local storage
    context.driver = thread_local.driver

@when('I navigate to "{url}"')
def navigate_to(context, url):
    context.driver.get(url)

@then('the title should be "{title}"')
def check_title(context, title):
    assert context.driver.title == title
    context.driver.quit()
