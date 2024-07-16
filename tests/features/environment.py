import os
import sys

from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup


def before_all(context):
    logger.info("Initializing test run")
    context.webdriver_setup = WebDriverSetup()
    context.driver = None  # Initialize driver to None

def before_scenario(context, scenario):
    logger.info(f"Setting up WebDriver for scenario: {scenario.name}")
    context.driver = context.webdriver_setup.setup_driver()

def after_scenario(context, scenario):
    logger.info(f"Tearing down WebDriver for scenario: {scenario.name}")
    if context.driver:
        context.driver.quit()
        context.driver = None

def after_all(context):
    logger.info("Tearing down after all tests")
    if context.webdriver_setup:
        context.webdriver_setup.teardown_driver()




