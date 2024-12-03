from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp
import os
from dotenv import load_dotenv
# import connect

# Load environment variables from the .env file
load_dotenv()

# Create the smartApi instance
smartApi = SmartConnect(os.getenv('API_KEY'))

# connect.setup_session()
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


#place order
def place_order (symbol, token, qty, ordertype, exch_seg, time, type, variety, price):
    try:
        orderparams = {
            "variety": variety, #"NORMAL",
            "tradingsymbol": symbol, #"SBIN-EQ",
            "symboltoken": token, #"3045",
            "transactiontype": "BUY",
            "exchange": "CDS",
            "ordertype": ordertype,#"LIMIT",
            "producttype": type, #"INTRADAY",
            "duration": time,#"DAY",
            "price": price, #"19500",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty #"10"
            }
        # Method 1: Place an order and return the order ID
        # orderid = smartApi.placeOrder(orderparams)
        # logger.info(f"PlaceOrder : {orderid}")
        # Method 2: Place an order and return the full response
        response = smartApi.placeOrderFullResponse(orderparams)
        logger.info(f"PlaceOrder : {response}")
    except Exception as e:
        logger.exception(f"Order placement failed: {e}")

place_order ("USDJPY25JUN141CE", "12001", 100 , "LIMIT", "NSE", "DAY",  "INTRADAY", "NORMAL", 8)

"""
{
"ordertype" : ("MARKET", "LIMIT", "STOPLOSS_LIMIT", "STOPLOSS_MARKET"),
"time" : ("DAY", "IOC"),
"type" : ("DELIVERY", "MARGIN", "INTRADAY", "BO"),
"variety" : ("NORMAL", "STOPLOSS", "AMO", "ROBO")
}
"""