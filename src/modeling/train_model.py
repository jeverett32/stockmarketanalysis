import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

def train_model(df: pd.DataFrame):
    """
    Trains a simple linear regression model to predict the next day's adjusted close price.

    :param df: The input DataFrame with features and target.
    :return: The trained model and the test data for evaluation.
    """
    # Define features (X) and target (y)
    # We will use the technical indicators to predict the next day's 'Adj Close'
    # We need to shift the 'Adj Close' to get the next day's price as the target
    df['target'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    features = ['SMA_50', 'SMA_200', 'EMA_50', 'EMA_200', 'RSI', 'MACD', 'MACD_signal', 'MACD_hist', 'upper_band', 'middle_band', 'lower_band']
    
    # Ensure all feature columns are present
    for feature in features:
        if feature not in df.columns:
            raise ValueError(f"Feature '{feature}' not found in DataFrame.")
            
    X = df[features]
    y = df['target']

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model Mean Squared Error: {mse}")

    return model, X_test, y_test, y_pred

if __name__ == '__main__':
    # Example usage:
    # Create a sample dataframe with technical indicators
    data = {
        'Date': pd.to_datetime(pd.date_range(start='2022-01-01', periods=300)),
        'Adj Close': np.random.uniform(100, 200, 300),
        'SMA_50': np.random.uniform(100, 200, 300),
        'SMA_200': np.random.uniform(100, 200, 300),
        'EMA_50': np.random.uniform(100, 200, 300),
        'EMA_200': np.random.uniform(100, 200, 300),
        'RSI': np.random.uniform(30, 70, 300),
        'MACD': np.random.uniform(-1, 1, 300),
        'MACD_signal': np.random.uniform(-1, 1, 300),
        'MACD_hist': np.random.uniform(-0.5, 0.5, 300),
        'upper_band': np.random.uniform(150, 250, 300),
        'middle_band': np.random.uniform(100, 200, 300),
        'lower_band': np.random.uniform(50, 150, 300),
    }
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    # Train the model
    trained_model, X_test, y_test, y_pred = train_model(df.copy())
    
    print("\nTrained Model:")
    print(trained_model)
    
    print("\nSample Predictions:")
    predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    print(predictions.head())