# Utility functions for the project
import re
import os
import json
import pandas as pd
from word2number import w2n
from tqdm.notebook import tqdm

def read_flatten_metrics(path='./config.json'):
    """
        Get the json filings from FILING_PATH
        Flatten the metrics list for easy matching
    Args:
        path (str, optional): Path to config file. Defaults to './config.json'.

    Returns:
        List<String> : 1D List of all metrics. 
    """
    fp = open(path, 'r')
    deepList = (json.load(fp))["metrics"]
    metricList = dict()
    for main in deepList:
        for key in deepList[main]:
            metricList[key.lower()] = list(map(lambda x: x.lower(), deepList[main][key]))
            metricList[key.lower()].append(key.lower())
    return metricList

def is_subseq(s1, s2):
    """
        Subsequence matching
        Define subsequence matching function for matching the metrics in the metrics list in the sentence.
    Args:
        s1 (str): String to be check as subsequence
        s2 (str): String inside which subsequence needs to be checked

    Returns:
        boolean: checks if s1 subsequence of s2 or not.
    """ 
    s1 = re.split('\. |\n|\s|\-', s1.lower()) # Metric 
    s2 = re.split('\. |\n|\s|\-', s2.lower()) # Context
    p1, p2 = 0, 0
    while p1 < len(s1) and p2 < len(s2):
        if s1[p1] == s2[p2]:
            p1+=1
        p2 += 1
    return p1 == len(s1)    

def run_extractor(INPUT_FILINGS_PATH, OUTPUT_FILINGS_PATH, paragraph_extractor):
    """
        Run the Paragraph Extraction Model on all the filings in the FILING_PATH
    Args:
        INPUT_FILINGS_PATH (uri): Path to Input Filings
        OUTPUT_FILINGS_PATH (uri): Path to Output Filings
        paragraph_extractor (uri): Paragraph EDxtractor Object
    """
    #TODO: Handle Directory if already exists or not exists
    dir, _, files = next(os.walk(INPUT_FILINGS_PATH))
    for file in tqdm(files):
        fp = open(f'{dir}/{file}', 'r')
        filing = json.load(fp)
        res = []
        para = ""
        for item in filing:
            para += str(filing[item])
        res = paragraph_extractor(para, int(filing['filing_date'].split('-')[0]))
        data = {
            'score'    : [r['score'] for r in res],
            'metric'   : [r['metric'] for r in res],
            'date'     : [r['date'] for r in res],
            'value'    : [r['value'] for r in res],
            'year'     : [r['year'] for r in res],
            'sentence' : [r['sentence'] for r in res],
        }
        pd.DataFrame(data).to_csv(f'{OUTPUT_FILINGS_PATH}/{file.strip(".json")}.csv', index = False)


def words_to_numbers(INPUT_FILINGS_PATH, OUTPUT_FILINGS_PATH):
    """
        Convert values containing words to numbers
        Example two hundred thirty -> 230

    Args:
        INPUT_FILINGS_PATH (uri): Path to Input Filings
        OUTPUT_FILINGS_PATH (uri): Path to Filings Output
    """    
    dir, _, files = next(os.walk(OUTPUT_FILINGS_PATH))
    for file in tqdm(files):
        if file.endswith('.gsheet'):
           continue
        df = pd.read_csv(f'{dir}/{file}')
        vals = []
        for i in df.index:
            val = df['value'][i]
            val = re.sub(r',', '', str(val))

            # fractions in words like half and one quater is hardcoded
            if val == 'less than half' or val == 'greater than half' or val == 'just over half':
                num = 0.5
            elif val == 'thousands':
                num = 1000.
            elif val == 'millions':
                num = 1e6
            else:
                # Extract the integer value if it is there in the value
                try:
                    num = float(re.findall(r'[0-9\.]+', val)[0])
                except:
                    # convert word like "two" to number 2
                    num = float(w2n.word_to_num(val))

                # multiply the factors
                if 'billion' in val:
                    num *= 1e9
                elif 'million' in val:
                    num *= 1e6
            vals.append(num)

        df['number'] = vals
        df.to_csv(f'{dir}/{file}', index=False)