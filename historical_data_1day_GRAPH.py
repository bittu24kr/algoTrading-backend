from logzero import logger
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta

class StockDataHandler:
    def __init__(self, smart_api_client):
        self.smart_api_client = smart_api_client
    
    @staticmethod
    def calculate_date_range(days_ago: int):
        """
        Calculates the start and end date for fetching OHLC data.
        
        :param days_ago: Number of days ago from the current date for the start date.
        :return: A tuple containing the start date (fdate) and end date (todate) formatted as strings.
        """
        todate = datetime.now().strftime("%Y-%m-%d %H:%M")
        fdate = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")
        return fdate, todate

    def fetch_ohlc_data(self, symboltoken, interval, fdate, todate):
        """
        Fetch historical OHLC data from the Smart API.
        """
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
        """
        if candleData is not None:
            column_name = f'{window}-day MA'
            candleData[column_name] = candleData['Close'].rolling(window=window).mean()
            return candleData
        else:
            logger.error("No data available to calculate moving average.")
            return None

    def detect_crossover(self, candleData, short_window, long_window):
        """
        Detect crossover points between two moving averages.

        Golden Cross: When the short moving average crosses above the long moving average (considered bullish).
        Death Cross: When the short moving average crosses below the long moving average (considered bearish).
        
        """
        short_ma_column = f'{short_window}-day MA'
        long_ma_column = f'{long_window}-day MA'

        if short_ma_column in candleData.columns and long_ma_column in candleData.columns:
            # Find the crossover points
            crossover_points = []
            for i in range(1, len(candleData)):
                if candleData[short_ma_column].iloc[i] > candleData[long_ma_column].iloc[i] and \
                   candleData[short_ma_column].iloc[i-1] <= candleData[long_ma_column].iloc[i-1]:
                    crossover_points.append((candleData.index[i], "Golden Cross"))  # Bullish crossover
                elif candleData[short_ma_column].iloc[i] < candleData[long_ma_column].iloc[i] and \
                     candleData[short_ma_column].iloc[i-1] >= candleData[long_ma_column].iloc[i-1]:
                    crossover_points.append((candleData.index[i], "Death Cross"))  # Bearish crossover

            return crossover_points
        else:
            logger.error(f"Missing required moving averages: {short_ma_column} or {long_ma_column}")
            return []

    def plot_ohlc_data(self, candleData, moving_averages=None):
        """
        Plot OHLC data as a candlestick chart with optional moving averages.
        """
        if candleData is not None:
            # Apply moving averages if provided
            if moving_averages is not None:
                for window in moving_averages:
                    candleData = self.calculate_moving_average(candleData, window)

            # Detect and print crossover points
            if len(moving_averages) == 2:
                crossover_points = self.detect_crossover(candleData, moving_averages[0], moving_averages[1])
                for point in crossover_points:
                    logger.info(f"Crossover detected at {point[0]}: {point[1]}")

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
