from ConnectSmartAPI import ConnectSmartAPI
from PlaceOrderEquity import PlaceOrderEquity
from historical_data_1day_GRAPH import StockDataHandler  

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

        # Instantiate the StockDataHandler to manage data fetching and plotting
        stock_data_handler = StockDataHandler(smart_api_client.smartApi)

        # Specify parameters for fetching OHLC data
        symboltoken = "3045"    
        interval = "ONE_DAY"    
        fdate = "2023-08-26 09:00"  # Start date and time for fetching data
        todate = "2024-08-26 15:30" # End date and time for fetching data

        # Fetch the OHLC data using StockDataHandler
        candle_data = stock_data_handler.fetch_ohlc_data(symboltoken, interval, fdate, todate)

        # Plot the fetched OHLC data with moving averages (e.g., 50-day and 200-day)
        stock_data_handler.plot_ohlc_data(candle_data, moving_averages=[50, 200])    
    
    finally:
        # Ensure the session is terminated even if an error occurs
        smart_api_client.terminate_session()

if __name__ == "__main__":
    main()
