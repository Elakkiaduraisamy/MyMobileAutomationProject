def before_all(context):
    # Any setup before all tests run can go here
    context.driver = None  # Ensure context has a driver attribute
    context.webdriver_setup = None


def after_all(context):
    # Teardown after all tests run
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
    if hasattr(context, 'webdriver_setup') and context.webdriver_setup:
        context.webdriver_setup.teardown_driver()
