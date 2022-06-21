import re
from utils import *
from text_extraction import TextExtractionModule

class ParagraphExtractionModule(TextExtractionModule):
    """
        Paragraph Extraction Module
        Paragraph extraction module inherits utilities from the text extraction module and is used to extract the paragraphs from the document.

    Args:
        TextExtractionModule (TextExtractionModule): TextExtractionModule Class Inherited.
    """    
    def __init__(self, nerModel, qaModel):
        super(ParagraphExtractionModule, self).__init__(nerModel=nerModel, qaModel=qaModel)

    def __call__(self, para, filing_year):
        sents = re.split(r'\. |\n', para)

        metrics = []
        metricList = read_flatten_metrics()
        for sent in sents:
            found = False
            for unit in metricList:
                for alt in metricList[unit]:
                    if is_subseq(alt, sent):
                      found = True
                      break

                if found:
                    break

            # If the sentence has no relevant metrics then continue
            if not found:
                continue

            res = TextExtractionModule.__call__(self, sent, filing_year)
            metrics.extend(res)

        metrics.sort(key=lambda x: x['score'], reverse=True)
        # final = metrics
        return metrics