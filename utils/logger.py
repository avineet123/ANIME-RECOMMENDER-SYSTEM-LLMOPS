import logging
import os
from datetime import datetime


# Directory where log files will be saved
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)  # Create if it doesn't exist

# Log file name with current date
log_file_path = os.path.join(LOGS_DIR, f"log_{datetime.now():%Y-%m-%d}.log")

# Configure the global logging format and level
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with the given name.
    
    Args:
        name (str): The name of the logger (usually __name__).
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # You can change this per logger if needed
    return logger
