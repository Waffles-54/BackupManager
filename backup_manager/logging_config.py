# backup_manager/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, 'backup_manager.log')

logger = logging.getLogger("backup_manager")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# File handler with rotation
file_handler = RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# Console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handlers only if they haven't been added yet
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
