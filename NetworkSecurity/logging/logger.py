import logging
import os
from datetime import datetime
import sys

# Generate the log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the log directory and ensure it exists
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Full log file path
log_path = os.path.join(log_dir, LOG_FILE)

# Configure logging
logging.basicConfig(
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)


