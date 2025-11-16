import argparse
import pandas as pd
import logging
from src.data_ingestion.download_data import download_stock_data
from src.data_processing.process_data import preprocess_data
from src.technical_analysis.indicators import add_technical_indicators
from src.modeling.train_model import train_model
from src.visualization.plot_data import plot_stock_price, plot_technical_indicators, plot_predictions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(args):
    """
    Main function to run the stock analysis pipeline.
    """
    # 1. Download data
    logging.info(f"Downloading data for ticker: {args.ticker}")
    download_stock_data([args.ticker], args.start_date, args.end_date)
    
    # 2. Load data
    data_path = f"data/{args.ticker}.csv"
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logging.error(f"Data file not found for ticker: {args.ticker}")
        return

    # 3. Preprocess data
    logging.info("Preprocessing data...")
    df = preprocess_data(df)

    # 4. Add technical indicators
    logging.info("Adding technical indicators...")
    df = add_technical_indicators(df)

    # 5. Train model
    logging.info("Training model...")
    model, X_test, y_test, y_pred = train_model(df)

    # 6. Visualize results
    logging.info("Visualizing results...")
    plot_stock_price(df, args.ticker)
    plot_technical_indicators(df, args.ticker)
    
    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    plot_predictions(predictions_df['Actual'], predictions_df['Predicted'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stock Market Analysis Pipeline')
    parser.add_argument('--ticker', type=str, default='AAPL', help='Stock ticker to analyze.')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date for historical data.')
    parser.add_argument('--end_date', type=str, default=None, help='End date for historical data.')
    
    args = parser.parse_args()
    main(args)
