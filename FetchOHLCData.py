from logzero import logger
import pandas as pd

def FetchOHLCData(smartApi, symboltoken, interval, fdate, todate):
    """Fetch historical OHLC data from Smart API."""
    try:
        # Define the request parameters
        historicParam = {
            "exchange": "NSE",
            "symboltoken": symboltoken,
            "interval": interval,
            "fromdate": fdate,
            "todate": todate
        }

        # Fetch the historical data
        response = smartApi.getCandleData(historicParam)
        
        if response.get('status', False):
            candle_data_raw = response.get('data', [])
            
            # Define column names
            columns_name = ["timestamp", "open", "high", "low", "close", "volume"]
            
            # Convert the data to a DataFrame
            candleData = pd.DataFrame(candle_data_raw, columns=columns_name)
            logger.info(f"Fetched historical data: \n{candleData}")
            
            return candleData
        else:
            logger.error(f"Failed to fetch historical data: {response.get('message', 'No message')}")
            return None

    except Exception as e:
        logger.exception(f"Failed to fetch OHLC data: {e}")
        return None
