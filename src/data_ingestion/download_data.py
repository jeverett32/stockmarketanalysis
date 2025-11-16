import yfinance as yf
import os
import argparse
import logging
import pandas as pd

# Directory to store the data
DATA_DIR = 'data'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_stock_data(tickers, start_date, end_date):
    """
    Downloads historical stock data for a list of tickers and saves it to CSV files.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if not stock_data.empty:
                # Reset index to make 'Date' a column
                stock_data.reset_index(inplace=True)
                
                # Flatten columns if they are multi-level
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_data.columns = stock_data.columns.droplevel(1)

                file_path = os.path.join(DATA_DIR, f'{ticker}.csv')
                stock_data.to_csv(file_path, index=False) # Don't save the index
                logging.info(f'Successfully downloaded and saved data for {ticker} to {file_path}')
            else:
                logging.warning(f'No data found for {ticker}')
        except Exception as e:
            logging.error(f'Failed to download data for {ticker}: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download historical stock data.')
    parser.add_argument('--tickers', nargs='+', default=['AAPL', 'GOOGL', 'MSFT'],
                        help='List of stock tickers to download.')
    parser.add_argument('--start_date', default='2020-01-01',
                        help='Start date for historical data in YYYY-MM-DD format.')
    parser.add_argument('--end_date', default=None,
                        help='End date for historical data in YYYY-MM-DD format.')
    args = parser.parse_args()

    download_stock_data(args.tickers, args.start_date, args.end_date)
