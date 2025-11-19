from flask import Flask, render_template
import pandas as pd
import os
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

# Import functions from our analysis pipeline
from src.data_processing.process_data import preprocess_data
from src.technical_analysis.indicators import add_technical_indicators

app = Flask(__name__)

DATA_DIR = 'data'

# Helper function to load and process data for a given ticker
def get_processed_data(ticker, start_date='2020-01-01', end_date=None):
    file_path = os.path.join(DATA_DIR, f'{ticker}.csv')
    if not os.path.exists(file_path):
        # If data not found locally, download it
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            return None
        stock_data.reset_index(inplace=True)
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.droplevel(1)
        stock_data.to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    df = preprocess_data(df)
    df = add_technical_indicators(df)
    return df

@app.route('/')
def index():
    # Market Trends
    market_indices = {
        '^GSPC': 'S&P 500',
        '^IXIC': 'NASDAQ',
        '^DJI': 'Dow Jones Industrial Average'
    }
    
    market_data = {}
    latest_date = None
    for ticker, name in market_indices.items():
        df = get_processed_data(ticker)
        if df is not None and not df.empty:
            if latest_date is None:
                latest_date = df.index[-1].strftime('%B %d, %Y')
            latest_close = df['close'].iloc[-1]
            previous_close = df['close'].iloc[-2]
            daily_change = (latest_close - previous_close) / previous_close * 100
            
            # Create a simple plot for the index
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name=name))
            fig.update_layout(title=f'{name} Performance', showlegend=False,
                              margin=dict(l=20, r=20, t=40, b=20))
            plot_div = plot(fig, output_type='div', include_plotlyjs=False)

            market_data[ticker] = {
                'name': name,
                'latest_close': f'{latest_close:.2f}',
                'daily_change': f'{daily_change:.2f}%',
                'plot': plot_div
            }
    
    return render_template('index.html', market_data=market_data, latest_date=latest_date)

@app.route('/top_movers')
def top_movers():
    # Top Movers (Gainers and Losers)
    # For simplicity, let's use a predefined list of stocks
    popular_stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'V', 'PFE', 'DIS', 'INTC', 'BA', 'KO', 'PEP', 'MCD', 'NKE', 'WMT', 'HD', 'COST', 'AXP', 'IBM', 'CSCO', 'ORCL', 'ADBE', 'CRM', 'SAP', 'TM', 'SONY']
    
    movers_data = []
    latest_date = None
    for ticker in popular_stocks:
        df = get_processed_data(ticker)
        if df is not None and not df.empty:
            if latest_date is None:
                latest_date = df.index[-1].strftime('%B %d, %Y')
            latest_close = df['close'].iloc[-1]
            previous_close = df['close'].iloc[-2]
            daily_change = (latest_close - previous_close) / previous_close * 100
            movers_data.append({
                'ticker': ticker,
                'latest_close': f'{latest_close:.2f}',
                'daily_change': f'{daily_change:.2f}%',
                'change_value': daily_change # for sorting
            })
    
    # Sort by daily change to get top gainers and losers
    top_gainers = sorted(movers_data, key=lambda x: x['change_value'], reverse=True)[:10]
    top_losers = sorted(movers_data, key=lambda x: x['change_value'])[:10]

    return render_template('top_movers.html', top_gainers=top_gainers, top_losers=top_losers, latest_date=latest_date)

@app.route('/recommendations')
def recommendations():
    # Simple Recommendation System
    # For simplicity, let's use a predefined list of stocks
    recommendation_stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NVDA']
    
    recommendations_list = []
    latest_date = None
    for ticker in recommendation_stocks:
        df = get_processed_data(ticker)
        if df is not None and not df.empty:
            if latest_date is None:
                latest_date = df.index[-1].strftime('%B %d, %Y')
            # Simple Golden Cross / Death Cross strategy
            # Buy signal: SMA_50 crosses above SMA_200
            # Sell signal: SMA_50 crosses below SMA_200
            
            latest_sma_50 = df['SMA_50'].iloc[-1]
            latest_sma_200 = df['SMA_200'].iloc[-1]
            
            previous_sma_50 = df['SMA_50'].iloc[-2]
            previous_sma_200 = df['SMA_200'].iloc[-2]

            signal = "HOLD"
            if latest_sma_50 > latest_sma_200 and previous_sma_50 <= previous_sma_200:
                signal = "BUY (Golden Cross)"
            elif latest_sma_50 < latest_sma_200 and previous_sma_50 >= previous_sma_200:
                signal = "SELL (Death Cross)"
            
            recommendations_list.append({
                'ticker': ticker,
                'signal': signal,
                'latest_close': f"{df['close'].iloc[-1]:.2f}"
            })

    return render_template('recommendations.html', recommendations=recommendations_list, latest_date=latest_date)

if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)