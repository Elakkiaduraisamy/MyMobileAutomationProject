import os
from NotGitFOlder.server_manager import AppiumServerManager


def before_all(context):
    # Start the Appium server
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config_server.json')
    context.server_manager = AppiumServerManager(config_file=config_path)
    context.server_manager.start()

def after_all(context):
    # Stop the Appium server if it was started
    if hasattr(context, 'server_manager'):
        context.server_manager.stop()
