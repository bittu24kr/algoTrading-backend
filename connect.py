from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create the smartApi instance
smartApi = SmartConnect(os.getenv('API_KEY'))

def setup_session():
    """Setup the Smart API session."""
    try:
        totp = pyotp.TOTP(os.getenv('TOKEN')).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    # Generate session
    data = smartApi.generateSession(os.getenv('CLIENT_ID'), os.getenv('PASSWORD'), totp)

    if data['status'] == False:
        logger.error(data)
    else:
        feedToken = smartApi.getfeedToken()
        print(f"Feed Token: {feedToken}")
    
    allholdings=smartApi.allholding()
    logger.info(f"AllHoldings : {allholdings}")
    

if __name__ == "__main__":
    setup_session()
