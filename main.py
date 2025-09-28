from fileReader import process_13f_file
from portfolioReturn import calculate_top10_portfolio_return
from fileFetch import process_next_url
from cikToFile import get_sec_filing_url
from tickerLookup import tickerLookup
from filterByTicker import filter_csv_by_tickers

# for i in range(1):
#     process_next_url()
#     res = calculate_top10_portfolio_return(process_13f_file("filing.txt"), "2025-07-01", "2025-9-25")

#     # if res >= 10:
#     #     print(res)
#     print(res)

for i in range(1):
    get_sec_filing_url()
    process_next_url()
    res = calculate_top10_portfolio_return(filter_csv_by_tickers(process_13f_file("filing.txt")), "2025-07-01", "2025-9-26")
    print(res)
    #tickerLookup("Kera_Capital_Partners_Inc.csv")