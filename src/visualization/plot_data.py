import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_stock_price(df: pd.DataFrame, ticker: str):
    """
    Plots the historical adjusted close price of a stock.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Adj Close'))
    fig.update_layout(title=f'{ticker} Historical Adjusted Close Price',
                      xaxis_title='Date',
                      yaxis_title='Price')
    # fig.show()

def plot_technical_indicators(df: pd.DataFrame, ticker: str):
    """
    Plots technical indicators.
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=('Moving Averages', 'RSI'))

    # Plot moving averages
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Adj Close', legendgroup='1'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50', legendgroup='1'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='SMA 200', legendgroup='1'), row=1, col=1)

    # Plot RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', legendgroup='2'), row=2, col=1)
    fig.add_shape(type='line', x0=df.index.min(), y0=70, x1=df.index.max(), y1=70,
                  line=dict(color='Red', width=2, dash='dash'), row=2, col=1)
    fig.add_shape(type='line', x0=df.index.min(), y0=30, x1=df.index.max(), y1=30,
                  line=dict(color='Green', width=2, dash='dash'), row=2, col=1)

    fig.update_layout(title_text=f'{ticker} Technical Indicators', legend_tracegroupgap=180)
    # fig.show()

def plot_predictions(y_test: pd.Series, y_pred: pd.Series):
    """
    Plots the actual vs. predicted prices.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_test.index, y=y_test, mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(x=y_test.index, y=y_pred, mode='lines', name='Predicted'))
    fig.update_layout(title='Model Predictions vs. Actual Prices',
                      xaxis_title='Date',
                      yaxis_title='Price')
    # fig.show()

if __name__ == '__main__':
    # Example Usage
    # Create a sample dataframe
    data = {
        'Date': pd.to_datetime(pd.date_range(start='2022-01-01', periods=300)),
        'Adj Close': pd.np.random.uniform(100, 200, 300),
        'SMA_50': pd.np.random.uniform(100, 200, 300),
        'SMA_200': pd.np.random.uniform(100, 200, 300),
        'RSI': pd.np.random.uniform(30, 70, 300),
    }
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    
    # Create sample predictions
    y_test_sample = pd.Series(pd.np.random.uniform(150, 180, 50), name='Actual', index=pd.to_datetime(pd.date_range(start='2022-11-01', periods=50)))
    y_pred_sample = pd.Series(pd.np.random.uniform(150, 180, 50), name='Predicted', index=y_test_sample.index)

    # Plotting
    plot_stock_price(df, 'SAMPLE')
    plot_technical_indicators(df, 'SAMPLE')
    plot_predictions(y_test_sample, y_pred_sample)