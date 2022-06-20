BASE_URL = "https://www.sec.gov/Archives/edgar/full-index/"
COMPANY_TICKER_URL = 'https://www.sec.gov/files/company_tickers.json'
ARCHIVES = 'https://www.sec.gov/Archives/'
COMPANY_SEARCH_BASE = 'https://www.sec.gov/cgi-bin/browse-edgar'
HTML_BASE = 'https://www.sec.gov'
TSV_FILE_HEADERS = [
    'CIK', 'Company', 'Type', 'Date', 'complete_text_file_link', 'html_index',
    'Filing Date', 'Period of Report', 'SIC', 'htm_file_link',
    'State of Inc', 'State location', 'Fiscal Year End', 'filename'
]
ERROR_TYPES = (400, 401, 403, 500, 502, 503, 504, 505)

ITEM_LIST_10_K = [
    '1', '1A', '1B', '2', '3', '4', '5', '6', '7', '7A',
    '8', '9', '9A', '9B', '10', '11', '12', '13', '14', '15'
]
ITEM_LIST_10_Q = [
    "1", "2", "3", "4", "1", "1A", "2", "3", "4", "5", "6"
]
ITEM_LIST_8_K = ['1.01', '1.02', '1.03', '2.01', '2.02', '2.03', '2.04', '2.05', '2.06', '3.01', '3.02', '3.03', '4.01', '4.02', '5.01', '5.02', '5.03', '5.05', '5.07', '7.01', '8.01', '9.01']
