# -*- coding: utf-8 -*-
"""
	Original file is located at
    https://colab.research.google.com/drive/1fn0l33AFmorHOrVDplB8a7FkYVVTgmYl?usp=sharing
"""
import json
import spacy
import spacy.cli
from utils import *
from transformers import pipeline
from paragraph_extraction import ParagraphExtractionModule
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

CONFIG_PATH = "./config.json"
config = open(CONFIG_PATH, 'r')
INPUT_FILINGS_PATH = (json.load(config))["INPUT_FILINGS_PATH"]
config = open(CONFIG_PATH, 'r')
OUTPUT_FILINGS_PATH = (json.load(config))["OUTPUT_FILINGS_PATH"]
print("Reading Filings from "+INPUT_FILINGS_PATH,"\Filings Output to"+OUTPUT_FILINGS_PATH)

#load assests
try:
    spacy_nlp_model = spacy.load('en_core_web_lg')
except:
    print("ERROR LOADING SPACY en_core_web_lg, downloading and installing...")
    spacy.download('en_core_web_lg')
    spacy_nlp_model = spacy.load('en_core_web_lg')

"""Create the question answering pipeline using hugging face transformers"""
question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

"""Create the pargraph extractor and then test it on sample sentence"""
paragraph_extractor = ParagraphExtractionModule(nerModel=spacy_nlp_model, qaModel=question_answerer)

"""Get the json filings from INPUT_FILING_PATH"""
run_extractor(INPUT_FILINGS_PATH, OUTPUT_FILINGS_PATH, paragraph_extractor)

"""
	Convert values containing words to numbers
	Example two hundred thirty -> 230
"""
words_to_numbers(INPUT_FILINGS_PATH, OUTPUT_FILINGS_PATH)