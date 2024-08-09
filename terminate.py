# terminate_session.py
from connect import smartApi  # Import the smartApi instance
from logzero import logger
import os

# Terminate the session
terminate = smartApi.terminateSession(os.getenv('CLIENT_ID'))
logger.info(f"Connection Close: {terminate}")