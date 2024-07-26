# Mobile Automation Testing with Behave and Appium

This project is a sample setup for mobile automation testing using Behave (a BDD framework), Appium (a mobile automation framework), and Python. It includes sample tests, configuration files, and scripts for setting up and tearing down the WebDriver.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Tests](#running-the-tests)
- [Configuration](#configuration)
- [Logging](#logging)
- [Teardown](#teardown)
- [Allure Reports](#allure-reports)

## Prerequisites

- Python 3.6+
- Node.js (for Appium)
- Appium (`npm install -g appium`)
- Allure command-line tool (`brew install allure` on macOS, or follow [Allure Installation](https://docs.qameta.io/allure/#_installing_a_commandline))
- Xcode (for iOS testing)

## Project Structure

```markdown
project_root/
│
├── apps/
│   └── iOS.Simulator.SauceLabs.Mobile.Sample.app.2.7.1.app
│
├── config/
│   └── config.json
│
├── logs/
│   └── appium.log
│
├── pages/
│   └── login_page.py
│
├── tests/
│   ├── features/
│   │   ├── environment.py
│   │   ├── login.feature
│   │   └── steps/
│   │       └── login_steps.py
|   |── test_app.py   
│
├── utils/
│   ├── appium_utilities.py
│   ├── config_loader.py
│   └── logger.py
│   
│
├── webdriver/
│   └── webdriver_setup.py
│
└── requirements.txt
```

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv myvenv
    source myvenv/bin/activate
    ```

3. Install the required Python packages:
    ```sh
    pip3 install -r requirements.txt
    ```

4. Install Appium:
    ```sh
    npm install -g appium
    ```

5. Install Allure command-line tool:
    ```sh
    brew install allure
    ```

6. Ensure the config/config.json file is correctly configured (see Configuration section).

## Running the Tests

To run the tests, use the following command:
```sh
behave -f allure_behave.formatter:AllureFormatter -o reports/ tests/features -D platform=ios

```
This command will execute the test scenarios defined in the login.feature file and generate Allure report data.

## Configuration
The configuration file config/config.json contains settings for the Appium server and the mobile application under test. Ensure it is correctly set up:
```json
{
    "appium_server_url": "http://127.0.0.1:4723",
    "appium_server_address": "127.0.0.1",
    "appium_server_port": "4723",
    "log_level": "debug",
    "log_file_path": "./logs/appium.log",
    "platform_name": "iOS",
    "platform_version": "17.5",
    "device_name": "iPhone 15 Pro",
    "automation_name": "XCUITest",
    "udid": "abc-def-ghij-klmn-opqrstuvwxyz",
    "bundle_id": "com.saucelabs.SwagLabsMobileApp",
    "app_path": "apps/iOS.Simulator.SauceLabs.Mobile.Sample.app.2.7.1.app"
}
```
## Logging
Logs are configured to be stored in the path specified in log_file_path in the configuration file. 

## Teardown
The WebDriverSetup class includes a method to shut down the iOS simulator after tests are completed. This is handled automatically in the environment.py file using Behave hooks.

Example of environment.py:
```python

import sys
import os
from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup
import allure

# Add steps directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'steps')))

def before_all(context):
    logger.info("Initializing test run")
    context.webdriver_setup = WebDriverSetup()
    context.driver = None  # Initialize driver to None

def before_scenario(context, scenario):
    logger.info(f"Setting up WebDriver for scenario: {scenario.name}")
    context.driver = context.webdriver_setup.setup_driver()
    allure.dynamic.feature(scenario.feature.name)
    allure.dynamic.story(scenario.name)

def after_scenario(context, scenario):
    logger.info(f"Tearing down WebDriver for scenario: {scenario.name}")
    if context.driver:
        context.driver.quit()
        context.driver = None

def after_all(context):
    logger.info("Tearing down after all tests")
    if context.webdriver_setup:
        context.webdriver_setup.teardown_driver()


```

## Allure Reports

To generate and view Allure reports:

1. Run the tests with Allure result directory specified:

    ```shell
   behave -f allure_behave.formatter:AllureFormatter -o reports/ tests/features -D platform=ios
    ```
2. Generate the Allure report:
    ```shell
    allure serve reports/
    ```
This will start a local server and open the Allure report in your default web browser.


