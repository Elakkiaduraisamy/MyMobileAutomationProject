import json
import os
from utils.logger import logger


def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON configuration file: {config_file}")
    except Exception as e:
        logger.error(f"Unexpected error loading configuration file: {e}")
    return None


def get_platform_config(config, platform_name):
    print("I am inside get_platform_config method :" )
    print(config[platform_name.lower()])
    try:
        return config[platform_name.lower()]
    except KeyError:
        logger.error(f"Platform configuration for '{platform_name}' not found in config file")
    return None
