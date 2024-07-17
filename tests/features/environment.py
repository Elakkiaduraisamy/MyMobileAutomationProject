import os
import sys
from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup

# Add steps directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'steps')))

def before_all(context):
    logger.info("Initializing test run")
    context.webdriver_setup = WebDriverSetup()
    context.driver = None  # Initialize driver to None


def before_scenario(context, scenario):
    logger.info(f"Setting up WebDriver for scenario: {scenario.name}")
    context.driver = context.webdriver_setup.setup_driver()
    context.allure_report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../reports'))
    if not os.path.exists(context.allure_report_dir):
        os.makedirs(context.allure_report_dir)


def after_scenario(context, scenario):
    logger.info(f"Tearing down WebDriver for scenario: {scenario.name}")
    if context.driver:
        context.driver.quit()
        context.driver = None


def after_all(context):
    logger.info("Tearing down after all tests")
    if context.webdriver_setup:
        context.webdriver_setup.teardown_driver()
