import pandas as pd
import yfinance as yf
from datetime import datetime

def calculate_top10_portfolio_return(portfolio_csv_name, date1, date2):
    """
    Calculates the total return of the top 10 stocks by dollar value in the portfolio
    from date1 to date2 using Yahoo Finance data.
    
    Args:
    portfolio_csv_name (str): Path to the portfolio CSV file (CUSIP in col 0, dollar in col 1).
    date1 (str): Start date in 'YYYY-MM-DD' format.
    date2 (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
    float: The total portfolio return as a decimal (e.g., 0.05 for 5%).
    """
    # Read portfolio CSV without headers, only first two columns
    df_port = pd.read_csv(portfolio_csv_name, header=None, usecols=[0, 1])
    df_port.columns = ['cusip', 'dollar']  # CUSIP in col 'cusip', Dollar in col 'dollar'
    df_port['dollar'] = pd.to_numeric(df_port['dollar'], errors='coerce')  # Convert dollar to numeric
    
    # Sort by dollar value descending and take top 10
    df_top = df_port.sort_values(by='dollar', ascending=False).head(10).reset_index(drop=True)
    
    # Read CUSIP lookup CSV without headers, only first two columns
    df_cusip = pd.read_csv('CUSIP.csv', header=None, usecols=[0, 1])
    df_cusip.columns = ['cusip', 'ticker']  # CUSIP in col 'cusip', Ticker in col 'ticker'
    
    # Create mapping from CUSIP (str) to ticker
    cusip_to_ticker = {}
    for idx, row in df_cusip.iterrows():
        cusip_key = str(row['cusip']).strip()
        ticker = str(row['ticker']).strip()
        cusip_to_ticker[cusip_key] = ticker
    
    # Get tickers and initial investments for top 10
    tickers = []
    initial_investments = []
    for idx, row in df_top.iterrows():
        cusip = str(row['cusip']).strip()
        if cusip in cusip_to_ticker:
            tickers.append(cusip_to_ticker[cusip])
            initial_investments.append(row['dollar'])
    
    if not tickers:
        return 0.0  # No valid tickers found
    
    # Download adjusted close prices using yfinance
    start_dt = pd.to_datetime(date1)
    end_dt = pd.to_datetime(date2)
    data = yf.download(tickers, start=date1, end=(end_dt + pd.Timedelta(days=1)).strftime('%Y-%m-%d'), auto_adjust=False)
    
    if data.empty:
        return 0.0  # No data available
    
    adj_close = data['Adj Close']
    
    # Get start prices (first available >= start_dt)
    start_data = adj_close.loc[adj_close.index >= start_dt]
    if start_data.empty:
        return 0.0
    start_prices = start_data.iloc[0]
    
    # Get end prices (last available <= end_dt)
    end_data = adj_close.loc[adj_close.index <= end_dt]
    if end_data.empty:
        return 0.0
    end_prices = end_data.iloc[-1]
    
    # Calculate position returns and sum them
    total_return_amount = 0.0
    total_initial = sum(initial_investments)
    for i, ticker in enumerate(tickers):
        if pd.isna(start_prices[ticker]) or pd.isna(end_prices[ticker]):
            continue
        price_ratio = end_prices[ticker] / start_prices[ticker]
        position_return = (price_ratio - 1) * initial_investments[i]
        total_return_amount += position_return
    
    # Portfolio total return
    if total_initial == 0:
        return 0.0
    portfolio_return = total_return_amount / total_initial
    return round(portfolio_return*100,2)

# print(calculate_top10_portfolio_return("Momentum_Wealth_Planning_LLC.csv", "2025-07-01", "2025-9-24"))