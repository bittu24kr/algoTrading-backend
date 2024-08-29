from logzero import logger
import pandas as pd
import mplfinance as mpf


class StockDataHandler:
   

    def __init__(self, smart_api_client):
        
        self.smart_api_client = smart_api_client

    def fetch_ohlc_data(self, symboltoken, interval, fdate, todate):

        #Fetch historical OHLC data from Smart API.
        try:
            # Define parameters for historical data fetching
            historicParam = {
                "exchange": "NSE",
                "symboltoken": symboltoken,
                "interval": interval,
                "fromdate": fdate,
                "todate": todate
            }

            # Fetch the candle data from the API
            response = self.smart_api_client.getCandleData(historicParam)

            # Check if the response is successful
            if response.get('status', False):
                candle_data_raw = response.get('data', [])
                columns_name = ["timestamp", "open", "high", "low", "close", "volume"]
                candleData = pd.DataFrame(candle_data_raw, columns=columns_name)

                # Convert the 'timestamp' column to datetime
                candleData['timestamp'] = pd.to_datetime(candleData['timestamp'])
                candleData.set_index('timestamp', inplace=True)

                # Rename columns to match mplfinance's expected format
                candleData.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                return candleData
            else:
                logger.error("Failed to fetch historical data: {}".format(response.get('message', 'No message')))
                return None
        except Exception as e:
            logger.exception(f"Historic API data fetching failed: {e}")
            return None

    def calculate_moving_average(self, candleData, window):
        """
        Calculate moving average on the provided OHLC data.

        :param candleData: DataFrame containing OHLC data
        :param window: Number of periods for the moving average (e.g., 50, 200)
        :return: DataFrame with an added column for the moving average
        """
        if candleData is not None:
            column_name = f'{window}-day MA'
            candleData[column_name] = candleData['Close'].rolling(window=window).mean()
            return candleData
        else:
            logger.error("No data available to calculate moving average.")
            return None

    def plot_ohlc_data(self, candleData, moving_averages=None):
        """
        Plot OHLC data as a candlestick chart with optional moving averages.

        :param candleData: DataFrame containing the OHLC data
        :param moving_averages: List of moving average windows (e.g., [50, 200])
        """
        if candleData is not None:
            # Apply moving averages if provided
            if moving_averages is not None:
                for window in moving_averages:
                    candleData = self.calculate_moving_average(candleData, window)

            # Plot the candlestick chart using mplfinance
            mpf.plot(candleData,
                     type='candle',
                     volume=True,
                     style='yahoo',
                     mav=moving_averages,  # Provide the list of moving averages
                     title='Candlestick Chart with Moving Averages',
                     ylabel='Price',
                     ylabel_lower='Volume')
        else:
            logger.error("No data available to plot.")
