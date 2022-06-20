# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1fn0l33AFmorHOrVDplB8a7FkYVVTgmYl?usp=sharing

# Install dependencies
* Three main dependencies
  * sentence transformers
  * transformers (for hugging face models)
  * sentnecepiece (for testing slow tokenizers)
"""

FILINGS_PATH = "../sec-scrapper/datasets/10_K"
OUTPUT_PATH = "../reports_output"

"""# Pre trained load models
* Two main models required in the application
  * sentence similarity model
  * roberta based fine tuned question answering model
"""
import os
import re
import json
import spacy
import spacy.cli
from utils import *
import pandas as pd
from pprint import pprint
from word2number import w2n
from sklearn import metrics
from tqdm.notebook import tqdm
from transformers import pipeline
#from text_extraction import TextExtractionModule
from paragraph_extraction import ParagraphExtractionModule

#from sentence_transformers import SentenceTransformer, util
#sim_model = SentenceTransformer('bert-base-nli-mean-tokens')
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")


#load assests
try:
    nlp = spacy.load('en_core_web_lg')
except:
    print("ERROR LOADING SPACY en_core_web_lg")
    spacy.download('en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')

# Utility Functions
# metricList = read_flatten_metrics()

# class TextExtractionModule(QuestionAnsweringModule):
#     def __init__(self, nerModel, qaModel):
#         super(TextExtractionModule, self).__init__(qaModel=qaModel, nerModel=nerModel)

#     def __call__(self, sent, filing_year):
#         # TODO:
#         # 1. Call the model for entity recognition
#         # 2. Create question and context
#         # 3. Call the model for question answering
#         # 4. Return the entities on single sentence
#         #    with highest score

#         sent = sent.strip().lower()
#         entities = EntityRecognitionModule.__call__(self, sent)
#         if 'MONEY' not in entities:
#             entities['MONEY'] = []
#         if 'DATE' not in entities:
#             entities['DATE'] = []

#         if 'CARDINAL' in entities:
#             entities['MONEY'].extend(entities['CARDINAL'])
#         if 'QUANTITY' in entities:
#             entities['MONEY'].extend(entities['QUANTITY'])


#         # Create context for the extractive question answering
#         ctx = self.create_context(sent)

#         # Grid search on ['ORG', 'DATE', 'MONEY']
#         results = []
#         all_metrics = [] # List of all the metris that can be extracted from current sentence

#         def get_year(date):
#             '''
#             Get the year from the date

#             1. Check if the year is in the date
            
#             1.1. If yes, return the year
            
#             1.2. If no, match the date with the 
#                  following set of possibilities 
#                  and shift from the filing year
#                  use the  senetence  similarity
#                  model to find the  best  match 
            
#             1.2.1. If the date is in the past,
#                    return the filing year-1
            
#             1.2.2. If the date is in the future,
#                    return the filing year+1
            
#             1.2.3. If the date is in the present,
#                    return the filing year
#             '''
            
#             dates = re.split('\. |\n|\s|\-', date.lower())

#             for d in dates:
#                 if len(d) == 4:
#                     try:
#                         year = int(d)
#                     except:
#                         continue
#                     return year
            
#             year_match = [
#                 ('previous year', -1), 
#                 ('present year', 0),
#                 ('future year', 1)
#             ]

#             gsim, year = -1, filing_year
#             for ysent, shift in year_match:
#                 enc1 = sim_model.encode(ysent)
#                 enc2 = sim_model.encode(date)
#                 sim = util.cos_sim(enc1, enc2)[0][0]

#                 if gsim < sim:
#                     gsim = sim
#                     year = filing_year + shift

#             return year

#         for unit in metricList:
#             for alt in metricList[unit]:
#                 if not is_subseq(alt, sent):
#                     continue
#                 all_metrics.append((alt, unit))

#         # Start matching with longest string
#         all_metrics.sort(key=lambda x: len(x[0]), reverse=True)

#         for alt, unit in all_metrics:
#             for date in entities['DATE']:
#                 year = get_year(date[0])
#                 for money in entities['MONEY']:

#                     qs1 = 'What is value of {} on {} ?'.format(alt, date[0])
#                     qs2 = 'What has value {} on {} ?'.format(money[0], date[0])
#                     qs3 = 'When is value of {} {} ?'.format(alt, money[0])

#                     res1 = QuestionAnsweringModule.__call__(self, qs1, ctx)
#                     res2 = QuestionAnsweringModule.__call__(self, qs2, ctx)
#                     res3 = QuestionAnsweringModule.__call__(self, qs3, ctx)

#                     score = max(res1['score'],
#                                 res2['score'], 
#                                 res3['score']
#                                 )

#                     if score >= 0.1:
#                         # Do not consider the results with score less than 0.1
#                         results.append({
#                             'sentence': sent,
#                             'metric'  : unit, #res2['answer'],
#                             'date'    : date[0], #res3['answer'],
#                             'value'   : res1['answer'],
#                             'year'    : year,
#                             'score'   : score
#                         })

#         # As a part of the text cleaning we remove the pairs
#         # that have two or more out of the  three  parts  of 
#         # the pair same

#         def match(r1, r2):
#             num_matches = 0
#             num_matches += int(r1['metric'] == r2['metric'])
#             num_matches += int(r1['value'] == r2['value'])
#             num_matches += int(r1['date'] == r2['date'])
#             return num_matches > 1

#         # Sort the results based on the score
#         results.sort(key=lambda x: x['score'], reverse=True)
#         final = []

#         # clean the numeric metrics and those that contain money
#         numeric_metrics = ['total number of customers', 'new customers', 'number of new accounts', 'dau', 'wau', 'mau', 'employee count']

#         for result in results:

#             # Clean the value to only include Number in value
#             metric = result['metric']
#             entities = EntityRecognitionModule.__call__(self, result['value'])
            
#             if 'MONEY' not in entities or metric in numeric_metrics:
#                 entities['MONEY'] = []

#             if metric in numeric_metrics and 'CARDINAL' in entities:
#                 entities['MONEY'].extend(entities['CARDINAL'])
#             if metric in numeric_metrics and 'QUANTITY' in entities:
#                 entities['MONEY'].extend(entities['QUANTITY'])
            
#             if len(entities['MONEY']) > 0:
#                 result['value'] = entities['MONEY'][0][0]
#             else:
#                 continue

#             # Stack based implementation for cleaning the repeated metrics
#             if len(final) == 0:
#                 final.append(result)
#             else:
#                 found = False
#                 for res in final:
#                     if match(res, result):
#                         found = True
#                         break
#                 if not found:
#                     final.append(result)

#         return final

#     def create_context(self, sent):
#         # Logic for creating custom context
#         return sent

# """# Paragraph Extraction Module

# Paragraph extraction module inherits utilities from the text extraction module and is used to extract the paragraphs from the document.
# """
# class ParagraphExtractionModule(TextExtractionModule):
#     def __init__(self, nerModel, qaModel):
#         super(ParagraphExtractionModule, self).__init__(nerModel=nerModel, qaModel=qaModel)

#     def __call__(self, para, filing_year):

#         # Logic to handle paragraph
#         sents = re.split(r'\. |\n', para)

#         metrics = []
#         global metricList
#         for sent in sents:
#             found = False
#             for unit in metricList:
#                 for alt in metricList[unit]:
#                     if is_subseq(alt, sent):
#                       found = True
#                       break

#                 if found:
#                     break

#             # If the sentence has no relevant metrics then continue
#             if not found:
#                 continue

#             res = TextExtractionModule.__call__(self, sent, filing_year)
#             metrics.extend(res)

#         metrics.sort(key=lambda x: x['score'], reverse=True)
#         # final = metrics
#         return metrics

"""Create the question answering pipeline using hugging face transformers"""

QuestionAnswerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

"""Create the named entity recognition model using the spacy library"""

# this cell may take upto 5 minutes to load the model



#spacy.cli.download("en_core_web_lg")


"""Create the pargraph extractor and then test it on sample sentence"""

pe = ParagraphExtractionModule(nerModel=nlp, qaModel=QuestionAnswerer)
sent = 'Creative ARR for last year was $3.2 billion and increased upto $8.78 billion this year.'
pe(sent.lower(), 2020)

"""# JSON testing"""

# FILINGS_PATH = 'path/to/filings-10K' # Path to the filings
# OUTPUT_PATH = 'path/to/output'       # Path to the output

# EXAMPLE


#TODO: Handle Directory if already exists or not exists
"""Get the json filings from FILING_PATH"""

dir, _, files = next(os.walk(FILINGS_PATH))

"""Run the Paragraph Extraction Model on all the filings in the FILING_PATH"""
for file in tqdm(files):
    fp = open(f'{dir}/{file}', 'r')
    filing = json.load(fp)

    res = []

    para = ""
    for item in filing:
        para += str(filing[item])

    res = pe(para, int(filing['filing_date'].split('-')[0]))

    data = {
        'score'    : [r['score'] for r in res],
        'metric'   : [r['metric'] for r in res],
        'date'     : [r['date'] for r in res],
        'value'    : [r['value'] for r in res],
        'year'     : [r['year'] for r in res],
        'sentence' : [r['sentence'] for r in res],
    }

    pd.DataFrame(data).to_csv(f'{OUTPUT_PATH}/{file.strip(".json")}.csv', index = False)

"""## Convert values containing words to numbers

Example two hundred thirty -> 230
"""

dir, _, files = next(os.walk(OUTPUT_PATH))
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