import pandas as pd

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and adds technical indicators to the DataFrame using pandas.

    :param df: The input DataFrame with stock data (must have lowercase columns).
    :return: The DataFrame with added technical indicators.
    """
    # Simple Moving Average (SMA)
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()

    # Exponential Moving Average (EMA)
    df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()

    # Relative Strength Index (RSI)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Moving Average Convergence Divergence (MACD)
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    
    # Bollinger Bands
    df['middle_band'] = df['close'].rolling(window=20).mean()
    std_dev = df['close'].rolling(window=20).std()
    df['upper_band'] = df['middle_band'] + (std_dev * 2)
    df['lower_band'] = df['middle_band'] - (std_dev * 2)

    # Drop rows with NaN values created by the indicators
    df.dropna(inplace=True)

    return df

if __name__ == '__main__':
    # Example usage:
    # Create a sample dataframe
    data = {
        'date': pd.to_datetime(pd.date_range(start='2022-01-01', periods=300)),
        'open': pd.np.random.uniform(100, 200, 300),
        'high': pd.np.random.uniform(100, 200, 300),
        'low': pd.np.random.uniform(100, 200, 300),
        'close': pd.np.random.uniform(100, 200, 300),
        'adj close': pd.np.random.uniform(100, 200, 300),
        'volume': pd.np.random.randint(1000, 5000, 300)
    }
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)

    # Add technical indicators
    df_with_indicators = add_technical_indicators(df.copy())

    print("DataFrame with Technical Indicators:")
    print(df_with_indicators.head())
    print(df_with_indicators.tail())
