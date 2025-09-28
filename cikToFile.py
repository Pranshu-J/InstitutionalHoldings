import requests
import json

def get_sec_filing_url():
    """
    Reads the first CIK from ciks.txt, fetches the SEC filing URL, writes it to urls.txt,
    removes the used CIK from ciks.txt, and returns the URL.
    
    :return: The constructed filing URL for the first hit, or None if no hits or no CIKs.
    """
    try:
        with open("ciks.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("ciks.txt not found.")
        return None
    
    if not lines:
        print("No more CIKs in ciks.txt.")
        return None
    
    cikNumber = lines[0].strip()
    
    search_url = f"https://efts.sec.gov/LATEST/search-index?q=13f-hr%20information%20table&dateRange=custom&category=custom&entityName={cikNumber}&startdt=2025-07-01&enddt=2025-09-30&forms=13F-HR"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    hits = data.get('hits', {}).get('hits', [])
    if not hits:
        # Still remove the CIK even if no hits
        with open("ciks.txt", "w") as f:
            f.writelines(lines[1:])
        print(f"No filing found for CIK {cikNumber}.")
        return None
    hit = hits[0]
    _id = hit['_id']
    accession = _id.split(':')[0]  # e.g., "0001172661-25-003626"
    ciks = hit['_source'].get('ciks', [])
    if not ciks:
        # Still remove the CIK even if no ciks in hit
        with open("ciks.txt", "w") as f:
            f.writelines(lines[1:])
        return None
    cik = ciks[0].lstrip('0')  # e.g., "1948780"
    dehyphenated = accession.replace('-', '')  # e.g., "000117266125003626"
    filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{dehyphenated}/{accession}.txt"

    with open("urls.txt", "w") as f:
        f.write(filing_url + "\n")

    # Remove the first line and shift the rest up
    with open("ciks.txt", "w") as f:
        f.writelines(lines[1:])
    
    print(f"Processed CIK {cikNumber}, URL written to urls.txt.")
    return filing_url