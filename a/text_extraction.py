"""# Text Extraction Module

Text extraction module inherits utilities from the entity recognition module and is used to extract the metrics from the document.
"""
import re
from question_answering import QuestionAnsweringModule
from entity_recognition import EntityRecognitionModule
from sentence_transformers import SentenceTransformer, util

class TextExtractionModule(QuestionAnsweringModule):
    def __init__(self, nerModel, qaModel):
        super(TextExtractionModule, self).__init__(qaModel=qaModel, nerModel=nerModel)

    def __call__(self, sent, filing_year):
        sim_model = SentenceTransformer('bert-base-nli-mean-tokens')
        # TODO:
        # 1. Call the model for entity recognition
        # 2. Create question and context
        # 3. Call the model for question answering
        # 4. Return the entities on single sentence
        #    with highest score

        sent = sent.strip().lower()
        entities = EntityRecognitionModule.__call__(self, sent)
        if 'MONEY' not in entities:
            entities['MONEY'] = []
        if 'DATE' not in entities:
            entities['DATE'] = []

        if 'CARDINAL' in entities:
            entities['MONEY'].extend(entities['CARDINAL'])
        if 'QUANTITY' in entities:
            entities['MONEY'].extend(entities['QUANTITY'])


        # Create context for the extractive question answering
        ctx = self.create_context(sent)

        # Grid search on ['ORG', 'DATE', 'MONEY']
        results = []
        all_metrics = [] # List of all the metris that can be extracted from current sentence

        def get_year(date):
            '''
            Get the year from the date

            1. Check if the year is in the date
            
            1.1. If yes, return the year
            
            1.2. If no, match the date with the 
                 following set of possibilities 
                 and shift from the filing year
                 use the  senetence  similarity
                 model to find the  best  match 
            
            1.2.1. If the date is in the past,
                   return the filing year-1
            
            1.2.2. If the date is in the future,
                   return the filing year+1
            
            1.2.3. If the date is in the present,
                   return the filing year
            '''
            
            dates = re.split('\. |\n|\s|\-', date.lower())

            for d in dates:
                if len(d) == 4:
                    try:
                        year = int(d)
                    except:
                        continue
                    return year
            
            year_match = [
                ('previous year', -1), 
                ('present year', 0),
                ('future year', 1)
            ]

            gsim, year = -1, filing_year
            for ysent, shift in year_match:
                enc1 = sim_model.encode(ysent)
                enc2 = sim_model.encode(date)
                sim = util.cos_sim(enc1, enc2)[0][0]

                if gsim < sim:
                    gsim = sim
                    year = filing_year + shift

            return year

        for unit in metricList:
            for alt in metricList[unit]:
                if not is_subseq(alt, sent):
                    continue
                all_metrics.append((alt, unit))

        # Start matching with longest string
        all_metrics.sort(key=lambda x: len(x[0]), reverse=True)

        for alt, unit in all_metrics:
            for date in entities['DATE']:
                year = get_year(date[0])
                for money in entities['MONEY']:

                    qs1 = 'What is value of {} on {} ?'.format(alt, date[0])
                    qs2 = 'What has value {} on {} ?'.format(money[0], date[0])
                    qs3 = 'When is value of {} {} ?'.format(alt, money[0])

                    res1 = QuestionAnsweringModule.__call__(self, qs1, ctx)
                    res2 = QuestionAnsweringModule.__call__(self, qs2, ctx)
                    res3 = QuestionAnsweringModule.__call__(self, qs3, ctx)

                    score = max(res1['score'],
                                res2['score'], 
                                res3['score']
                                )

                    if score >= 0.1:
                        # Do not consider the results with score less than 0.1
                        results.append({
                            'sentence': sent,
                            'metric'  : unit, #res2['answer'],
                            'date'    : date[0], #res3['answer'],
                            'value'   : res1['answer'],
                            'year'    : year,
                            'score'   : score
                        })

        # As a part of the text cleaning we remove the pairs
        # that have two or more out of the  three  parts  of 
        # the pair same

        def match(r1, r2):
            num_matches = 0
            num_matches += int(r1['metric'] == r2['metric'])
            num_matches += int(r1['value'] == r2['value'])
            num_matches += int(r1['date'] == r2['date'])
            return num_matches > 1

        # Sort the results based on the score
        results.sort(key=lambda x: x['score'], reverse=True)
        final = []

        # clean the numeric metrics and those that contain money
        numeric_metrics = ['total number of customers', 'new customers', 'number of new accounts', 'dau', 'wau', 'mau', 'employee count']

        for result in results:

            # Clean the value to only include Number in value
            metric = result['metric']
            entities = EntityRecognitionModule.__call__(self, result['value'])
            
            if 'MONEY' not in entities or metric in numeric_metrics:
                entities['MONEY'] = []

            if metric in numeric_metrics and 'CARDINAL' in entities:
                entities['MONEY'].extend(entities['CARDINAL'])
            if metric in numeric_metrics and 'QUANTITY' in entities:
                entities['MONEY'].extend(entities['QUANTITY'])
            
            if len(entities['MONEY']) > 0:
                result['value'] = entities['MONEY'][0][0]
            else:
                continue

            # Stack based implementation for cleaning the repeated metrics
            if len(final) == 0:
                final.append(result)
            else:
                found = False
                for res in final:
                    if match(res, result):
                        found = True
                        break
                if not found:
                    final.append(result)

        return final

    def create_context(self, sent):
        # Logic for creating custom context
        return sent