import pandas as pd
import sys

def tickerLookup(csvName):
    input_file = csvName
    df = pd.read_csv(input_file)

    # Assume the first column contains the CUSIP values
    cusip_col = df.columns[0]

    # Read the lookup file (assumes it has headers: cusip, symbol, description)
    lookup = pd.read_csv('CUSIP.csv')

    # Create a dictionary for fast lookup
    symbols_dict = dict(zip(lookup['cusip'].astype(str), lookup['symbol']))

    # Map CUSIPs to symbols, default to empty string if not found
    symbol_list = [symbols_dict.get(str(cusip), '') for cusip in df[cusip_col]]

    # Insert the new 'Symbol' column at position 2 (third column)
    df.insert(2, 'Symbol', symbol_list)

    # Save back to the original file, overwriting it
    df.to_csv(input_file, index=False)

    #print(f"Updated {input_file} with Symbol column.")