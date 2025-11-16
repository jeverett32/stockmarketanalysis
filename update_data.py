import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from data_ingestion.download_data import download_stock_data

def update_all_data():
    """
    Downloads the latest stock data for market indices, popular stocks, and recommendation stocks.
    """
    today = datetime.now()
    # Download data for the last 365 days to ensure enough data for indicators
    start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    # Market Indices
    market_indices_tickers = ['^GSPC', '^IXIC', '^DJI']
    print(f"Updating market indices data for {market_indices_tickers}...")
    download_stock_data(market_indices_tickers, start_date, end_date)

    # Popular Stocks (for Top Movers)
    popular_stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'V', 'PFE', 'DIS', 'INTC', 'BA', 'KO', 'PEP', 'MCD', 'NKE', 'WMT', 'HD', 'COST', 'AXP', 'IBM', 'CSCO', 'ORCL', 'ADBE', 'CRM', 'SAP', 'TM', 'SONY']
    print(f"Updating popular stocks data for {popular_stocks}...")
    download_stock_data(popular_stocks, start_date, end_date)

    # Recommendation Stocks
    recommendation_stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NVDA']
    print(f"Updating recommendation stocks data for {recommendation_stocks}...")
    download_stock_data(recommendation_stocks, start_date, end_date)

    print("All data updated successfully!")

if __name__ == '__main__':
    update_all_data()
