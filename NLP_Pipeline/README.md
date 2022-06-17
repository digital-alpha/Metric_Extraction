# Metric Extraction NLP Pipeline

Requirement of NLP Methods for SEC EDGAR Scraping.

Challenges worth considering before stating an NLP approach for the P.S.

- **Unstructured Text**-The task of extracting data from unstructured text is quite vague, since most of the companies report a wide variety of metrics which have formats uniquely specific for that particular company. 

- **Indistinguishable Metrics**- Moreover, without definitely outlining the relevant metrics for our use case most of the NLP models will treat words like “customer” in “customer revenue” as normal entities as a part of the sentence and not specifically distinguish the need for the useful metrics. 

- **Non-Standard Tables**- The main challenges in this field was that parsing unstructured text to extract relevant details is still a vast area of research and the success in this domain is limited, so it is essential in our case to modify the current available state of the art models to perform better for our use case.

Inadequacy in Existing Models-In the case of the tables, some tables contain descriptive information in the form of text and some contain values, these metrics are difficult to be handled directly with any deterministic algorithm. 

# Named Entity Recognition

- Unique entities like money, dates and metrics can be extracted from the sentences using Named Entity Recognition.
- In our case, NER was used to parse important metrics, dates and money from chunk of text taken.
- **Drawback** Once entities are extracted, the task is to accurately map the metric with correct date and value associated with it.
- [Source](https://insight.factset.com/financial-use-cases-for-named-entity-recognition-ner)

# Dependeny Parser 
- The task of mapping dates and values to the correct metric was established using a dependency parser.
- We used SpaCy's dependency parser and the CoreNLP (Stanford) dependency parser to test this hypothesis.
- This method was successful for simple sentences and those containing at most one cross dependency. E.g. Annual recurring revenue was $1.2 Billion in 2019, and $3.5 Billion was the value of Net Profit in 2020.
- However, this method fails significantly with more than one cross dependency (tracing the value dependent on the metric we are crossing on or more other metrics). E.g. _The value of Annual Recurring Revenue, Net Profit and Gross Profit for 2018 were $1.2 Billion, $2.4 Billion and $3.6 Billion respectively._
- **Challenge:** Money and dates were identified accurately, but metrics like _"customer revenue"_ were not identified by NER. This led to a requirement of a custom list of metrics
- [Source](https://www.analyticsvidhya.com/blog/2021/12/dependency-parsing-in-natural-language-processing-with-examples/)

# Question Answering Methods

- The flaws left after dependency parsing were of cross relationships, which Question and Answering approach recognizes, we were not able to achieve this by NER.
-  **Test:** API of GPT-3 DaVinci model was successful in extracting the metrics from the text to a great extent due to large number of trainable parameters.
-  **An Important Obstical** is to map the linguistic dates to actual dates. Eg: Mapping "_last fiscal year_" to its corresponding date.
-  To handle ambiguous sentences and cross dependencies, we explored the language modelling Question Answering approach.
-  The performance of the model was poor for ambiguous and complicated sentences. 
-  The execution time was significantly greater than the NER approach.
-  Extractive Question Answering provides the output in form of start position and end position. - -  Consequently, there are high chances that a portion of garbage text is also parsed along with the value.
-  Another challenge is to convert the text value to comparable integer number. Value might be written in text form, have some special characters, or can just be a percentage growth.

# Hybrid Approach : Optimized QA Metric Extraction using NER

To make our predictions more robust, we ask three questions and make a tuple of related metrics, data and value with the highest confidence in the answer. Say we have a metric Net Profit, date/year 2019 and value $1 Million, then the following three types of questions asked

> When was $1 Million the value of Net Profit?
> What was the value of Net Profit in 2019?
> Which metric has the value of $1 Million in 2019?

The answers provided by the question-answerer were again passed through the named entity recognizer to fetch out the value from the response and discard any unwanted text if present. If there is no value present in the answer, we discard the tuple

- A Binary Search Tree implementation was used to remove duplicate entries. The question answerer model works quite well in general for ambiguous sentences as well. 
- For results with low confidence scores we make use of the dependency tree created to improve the performance for simple but ambiguous 
- It was found that this pipeline performed significantly better than using a dependency parser and using financial models like TAT-QA fine-tuned on financial question answering dataset improved performance compared to Roberta. The pipeline was extended to handle the entire corpus by splitting it into single sentences.
