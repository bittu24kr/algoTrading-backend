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

        # Instantiate the StockDataHandler
        stock_data_handler = StockDataHandler(smart_api_client.smartApi)

        # Specify the symbol and date range
        symboltoken = "3045"
        interval = "ONE_DAY"

        # Calculate date range for the last 1500 days
        fdate, todate = stock_data_handler.calculate_date_range(1500)

        # Fetch the OHLC data
        candle_data = stock_data_handler.fetch_ohlc_data(symboltoken, interval, fdate, todate)

        # Plot the fetched OHLC data with moving averages and detect crossovers
        stock_data_handler.plot_ohlc_data(candle_data, moving_averages=[50, 200])

    finally:
        # Terminate the session after completion
        smart_api_client.terminate_session()


if __name__ == "__main__":
    main()
