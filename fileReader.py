import xml.etree.ElementTree as ET
import csv
import re
import os
from tickerLookup import tickerLookup

def process_13f_file(file_path: str) -> str:
    """
    Processes an SEC 13F-HR text file to extract CUSIP and dollar value information
    from the information table and writes it to a CSV file named after the conformed
    company name.

    Args:
        file_path (str): Path to the input .txt file.

    Returns:
        str: Path to the generated CSV file.

    Raises:
        ValueError: If company name or information table XML is not found.
        FileNotFoundError: If the input file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract company conformed name from the header section
    company_match = re.search(r'COMPANY CONFORMED NAME:\s*(.+?)(?=\n|$)', content)
    if not company_match:
        raise ValueError("Company conformed name not found in the file.")
    company_name = company_match.group(1).strip()
    
    # Sanitize company name for filename (replace spaces with _, remove commas and periods)
    sanitized_name = re.sub(r'[^\w\s-]', '', company_name).replace(' ', '_').replace('-', '_')
    print(sanitized_name)
    
    # Find the <DOCUMENT> section for INFORMATION TABLE
    doc_start_pattern = r'<DOCUMENT>\s*<TYPE>INFORMATION TABLE'
    doc_start_match = re.search(doc_start_pattern, content)
    if not doc_start_match:
        raise ValueError("INFORMATION TABLE document section not found in the file.")
    doc_start_idx = doc_start_match.start()
    
    # Find the end of this <DOCUMENT> section (next </DOCUMENT>)
    doc_end_match = re.search(r'</DOCUMENT>', content, re.DOTALL)
    if not doc_end_match or doc_end_match.start() < doc_start_idx:
        # If not found after start, search from start
        doc_end_match = re.search(r'</DOCUMENT>', content[doc_start_idx:], re.DOTALL)
        if not doc_end_match:
            raise ValueError("Closing </DOCUMENT> tag not found for INFORMATION TABLE.")
        doc_end_idx = doc_start_idx + doc_end_match.end()
    else:
        doc_end_idx = doc_end_match.end()
    
    # Extract the document fragment
    doc_fragment = content[doc_start_idx:doc_end_idx]
    
    # Within the document, find <XML> start and </XML> end
    xml_start_match = re.search(r'<XML>\s*(.+?)\s*</XML>', doc_fragment, re.DOTALL)
    if not xml_start_match:
        raise ValueError("XML content not found in the INFORMATION TABLE document.")
    xml_content = xml_start_match.group(1).strip()
    
    # Clean up XML content: remove <?xml ... ?> if present
    xml_content = re.sub(r'^\s*<\?xml[^>]*\?>\s*', '', xml_content, flags=re.DOTALL)
    
    # Parse the XML
    root = ET.fromstring(xml_content)
    
    # Define namespace for the information table (using ns1 prefix as in the example)
    ns = {'ns1': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}
    
    # Extract CUSIP and value for each infoTable
    holdings = []
    for info_table in root.findall('.//ns1:infoTable', ns):
        cusip_elem = info_table.find('ns1:cusip', ns)
        value_elem = info_table.find('ns1:value', ns)
        if cusip_elem is not None and value_elem is not None:
            cusip = cusip_elem.text.strip() if cusip_elem.text else ''
            value = value_elem.text.strip() if value_elem.text else ''
            holdings.append((cusip, value))
    
    if not holdings:
        raise ValueError("No holdings data found in the information table.")
    
    # Create CSV filename
    csv_filename = f"{sanitized_name}.csv"
    
    # Write to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CUSIP', 'Dollar Value'])
        writer.writerows(holdings)
    
    tickerLookup(csv_filename)

    return csv_filename

# process_13f_file("file.txt")