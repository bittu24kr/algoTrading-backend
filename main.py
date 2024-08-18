from ConnectSmartAPI import ConnectSmartAPI
from PlaceOrderEquity import PlaceOrderEquity

def main():
    smart_api_client = ConnectSmartAPI()

    try:
        # Connect to Smart API
        smart_api_client.connect_session()
        
        # Example order parameters
        symbol = "SBIN-EQ"
        token = "3045"
        qty = 10
        ordertype = "LIMIT"
        exch_seg = "NSE"
        time = "DAY"
        type = "INTRADAY"
        variety = "NORMAL"
        price = 19500
        
        # Place the order
        PlaceOrderEquity(smart_api_client.smartApi, symbol, token, qty, ordertype, exch_seg, time, type, variety, price)
    
    finally:
        # Ensure the session is terminated even if an error occurs
        smart_api_client.terminate_session()

if __name__ == "__main__":
    main()
