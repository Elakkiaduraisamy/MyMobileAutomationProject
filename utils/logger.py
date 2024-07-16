import logging
import os


def setup_logger():
    c_logger = logging.getLogger('app_logger')
    c_logger.setLevel(logging.DEBUG)  # Set the logger to the debug level

    # Check if the logger has handlers to avoid duplicate logs
    if not c_logger.handlers:
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create file handler and set level to debug
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        fh = logging.FileHandler(os.path.join(log_dir, 'app.log'))
        fh.setLevel(logging.DEBUG)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        c_logger.addHandler(ch)
        c_logger.addHandler(fh)

    return c_logger


logger = setup_logger()
