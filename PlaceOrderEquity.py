from logzero import logger
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def PlaceOrderEquity(smartApi, symbol, token, qty, ordertype, exch_seg, time, type, variety, price):
    """Places an order using the Smart API."""
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": "BUY",
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": type,
            "duration": time,
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
        }
        
        # Place the order and return the full response
        response = smartApi.placeOrderFullResponse(orderparams)
        logger.info(f"PlaceOrder : {response}")
    except Exception as e:
        logger.exception(f"Order placement failed: {e}")
