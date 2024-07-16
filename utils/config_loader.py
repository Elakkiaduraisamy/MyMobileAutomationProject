import json
import os
import logging

logger = logging.getLogger('app_logger')


def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON configuration file: {config_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
