This repository has been inspired from the [EDGAR CRAWLER](https://github.com/nlpaueb/edgar-crawler) repository for generating 10-K filings. The repository has been modified to generate filings from 8-K and 10-Q forms as well.

## FILINGS SCRAPER

- Crawl and download financial reports for each publicly-traded company, for specified years, through the `edgar_crawler.py` module.
- Extract and clean specific text sections, such as Risk Factors, MD&A, and others, through the `extract_items.py` module.


## Installation
- Set up a virtual enviroment using `pipenv shell` or `pythom3 -m venv`
- Download all dependencies using `pip install -r requirements.txt`

 
## General Information about the files 
- CIK Numbers are available in `CIK.csv`
- `edgar_crawler.py` to generate all the filings for the given cik numbers and duration
- `extract_items_8k.py` to extract all the 8k forms 
- `extract_items_10k.py` to extract all the 10k forms 
- `extract_items_10q.py` to extract all the 10q forms 
- INDICES contains files for the specified year 

## Procedure

1. Edit the `config.json` file with `"filing_types": []` specify the form type as `8-K or 10-K or 10-Q` depending on the type of form we wish to extract

2. Run `edgar_crawler.py` . This will create a csv named `FILLINGS_METADATA.csv` alongwith a folder named `RAW_FILLINGS`

3. Run the corresponding script file in  `extract_items_{type mentioned in the config.json file}.py`

4. Creates a folder in the datasets directory corresponding to the form type 

## Usage
- Before running any script, you can edit the `config.json` file.
  - Arguments for `edgar_crawler.py`, the module to download financial reports:
      - `--start_year XXXX`: the year range to start from
      - `--end_year YYYY`: the year range to end to
      - `--quarters`: the quarters that you want to download filings from (List).<br> Default value is: `[1, 2, 3, 4]`.
      - `--filing_types`: list of filing types to download.<br> Default value is: `['10-K', '10-Q', '8-K']`.
      - `--cik_tickers`: list or path of file containing CIKs or Tickers. e.g. `[789019, "1018724", "AAPL", "TWTR"]` <br>
        In case of file, provide each CIK or Ticker in a different line.  <br>
      If this argument is not provided, then the toolkit will download annual reports for all the U.S. publicly traded companies.
      - `--user_agent`: the User-agent that will be declared to SEC EDGAR.
      - `--raw_filings_folder`: the name of the folder where downloaded filings will be stored.<br> Default value is `'RAW_FILINGS'`.
      - `--indices_folder`: the name of the folder where EDGAR TSV files will be stored. These are used to locate the annual reports. Default value is `'INDICES'`.
      - `--filings_metadata_file`: CSV filename to save metadata from the reports.
      - `--skip_present_indices`: Whether to skip already downloaded EDGAR indices or download them nonetheless.<br> Default value is `True`.
      - `remove_tables`: Whether to remove tables containing mostly numerical (financial) data. This work is mostly to facilitate NLP research and often numerical tables are not useful




