from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class ConnectSmartAPI:
    def __init__(self):
        self.smartApi = None

    def connect_session(self):
        self.smartApi = SmartConnect(os.getenv('API_KEY'))

        try:
            totp = pyotp.TOTP(os.getenv('TOKEN')).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        data = self.smartApi.generateSession(os.getenv('CLIENT_ID'), os.getenv('PASSWORD'), totp)
        
        if data['status'] == True:
            logger.info("Connected to Smart API")
        else:
            logger.error("Failed to connect to Smart API")

    def terminate_session(self):
        if self.smartApi:
            response = self.smartApi.terminateSession(os.getenv('CLIENT_ID'))
            if response['status'] == True:
                logger.info("Disconnected to Smart API")
        else:
            logger.warning("No active session to terminate.")
