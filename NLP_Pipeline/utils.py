# Utility functions for the project
import re
import os
import json

"""### Flatten the metrics list for easy matching"""
def read_flatten_metrics(path='./metrics.json'):
    fp = open(path, 'r')
    deepList = json.load(fp)
    metricList = dict()

    for main in deepList:
        for key in deepList[main]:
            metricList[key.lower()] = list(map(lambda x: x.lower(), deepList[main][key]))
            metricList[key.lower()].append(key.lower())
    return metricList

""" Subsequence matching
    Define subsequence matching function for matching the metrics in the metrics list in the sentence.
"""
def is_subseq(s1, s2):
    s1 = re.split('\. |\n|\s|\-', s1.lower()) # Metric 
    s2 = re.split('\. |\n|\s|\-', s2.lower()) # Context
    p1, p2 = 0, 0
    while p1 < len(s1) and p2 < len(s2):
        if s1[p1] == s2[p2]:
            p1+=1
        p2 += 1
    return p1 == len(s1)    