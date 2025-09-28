import pandas as pd

def filter_csv_by_tickers(csv_filename: str) -> str:
    """
    Filters the CSV file by checking if values in the 'Symbol' column exist exactly
    on their own lines in 'all_tickers.txt'. Rows where the symbol is not found are deleted.
    
    Args:
        csv_filename (str): The name of the CSV file to filter.
    
    Returns:
        str: The name of the filtered CSV file.
    """
    # Read all_tickers.txt into a set for exact match lookup
    with open('all_tickers.txt', 'r') as f:
        tickers = {line.strip() for line in f if line.strip()}
    
    # Read the CSV file
    df = pd.read_csv(csv_filename)
    
    # Filter rows where 'Symbol' is in the tickers set
    df_filtered = df[df['Symbol'].isin(tickers)]
    
    # Overwrite the original CSV with filtered data
    df_filtered.to_csv(csv_filename, index=False)
    
    return csv_filename