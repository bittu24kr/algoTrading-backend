from ConnectSmartAPI import ConnectSmartAPI
from logzero import logger
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

 #Historic api
def OHLCHistory (smart_api_client, symboltoken, interval, fdate, todate):
    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": symboltoken, #"3045",
        "interval": interval, #"FIVE_MINUTE",
        "fromdate": fdate, #"2024-08-08 09:00", 
        "todate": todate, #"2024-08-08 15:30"
        }
        smart_api_client.smartApi.getCandleData(historicParam)

            # Fetch the candle data
        response = smart_api_client.smartApi.getCandleData(historicParam)
        
        if response.get('status', False):
            candle_data_raw = response.get('data', [])
            
            # Define column names
            columns_name = ["timestamp", "open", "high", "low", "close", "volume"]
            
            # Convert the data to a DataFrame
            candleData = pd.DataFrame(candle_data_raw, columns=columns_name)
            
            print(candleData)
        else:
            logger.error("Failed to fetch historical data: {}".format(response.get('message', 'No message')))

    except Exception as e:
        logger.exception(f"Historic Api failed: {e}")
    
def main():
    smart_api_client = ConnectSmartAPI()

    # Connect to Smart API
    smart_api_client.connect_session()

    # Call the OHLCHistory function
    OHLCHistory (smart_api_client, "3045", "FIVE_MINUTE", "2024-08-08 09:00", "2024-08-08 15:30")

    # Terminate the session after processing
    smart_api_client.terminate_session()

if __name__ == "__main__":
    main()