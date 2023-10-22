import os
import logging
from logging.handlers import RotatingFileHandler

"""Configure logger with specified name"""
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Set up logging
log_format = "[%(asctime)s] [%(levelname)s] - %(message)s"

# Create rotating file handler
file_handler = RotatingFileHandler("./logs/app.log", maxBytes=1000000, backupCount=5)
file_handler.setFormatter(logging.Formatter(log_format))

# Create stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(log_format))


def setup_logger(name):
    # Configure the logger
    inner_logger = logging.getLogger(name)
    inner_logger.setLevel(logging.INFO)  # Set logging level
    inner_logger.addHandler(file_handler)
    inner_logger.addHandler(stream_handler)

    return inner_logger


# Set up your main logger
logger = setup_logger(__name__)

