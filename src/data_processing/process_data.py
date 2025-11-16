import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the stock data.

    :param df: The input DataFrame with stock data.
    :return: The preprocessed DataFrame.
    """
    # Convert column names to lowercase
    df.columns = [col.lower() for col in df.columns]
    
    # Ensure the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    # Sort by date
    df.sort_index(inplace=True)

    # Handle missing values - forward fill
    df.fillna(method='ffill', inplace=True)
    
    # Drop any remaining NaN values
    df.dropna(inplace=True)

    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change()

    # Drop the first row which will have a NaN daily_return
    df.dropna(inplace=True)

    return df

if __name__ == '__main__':
    # Example usage:
    # Create a sample dataframe
    data = {
        'Date': ['2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'Open': [150, 152, 153, 155],
        'High': [153, 154, 156, 157],
        'Low': [149, 151, 152, 154],
        'Close': [152, 153, 155, 156],
        'Adj Close': [151.5, 152.5, 154.5, 155.5],
        'Volume': [1000, 1100, 1200, 1300]
    }
    df = pd.DataFrame(data)
    
    # Preprocess the data
    preprocessed_df = preprocess_data(df.copy())
    
    print("Original DataFrame:")
    print(df)
    print("\nPreprocessed DataFrame:")
    print(preprocessed_df)