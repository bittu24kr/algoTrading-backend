import requests
import pandas as pd

def fetch_stock_list():
    
    # API endpoint
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

    # Make the API request to fetch the stock list
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        stock_data = response.json()  # Parse the JSON response
        
        # Convert the stock data to a pandas DataFrame
        stock_df = pd.DataFrame(stock_data)
        #Filtering the data
        stock_df = stock_df[stock_df['symbol'].str.contains('-EQ')]

         # Selecting  only specific columns to display
        columns_to_display = ['symbol', 'name']  
        stock_df = stock_df[columns_to_display]
        
        # Return the DataFrame
        return stock_df
    else:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")
        return None

#  Immediate execution block
# if __name__ == "__main__":
#     stock_df = fetch_stock_list()
    
#     if stock_df is not None:
#         #print(stock_df.head())
#         print(stock_df.head().to_string(index=False))
