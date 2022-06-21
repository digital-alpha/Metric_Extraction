class EntityRecognitionModule:
    """
        Entity Recognition Module
        Thy Class of entity recognition module which will be used in the named entity recognition task.
        It expects a pretrained 
    """    
    def __init__(self, nerModel):
        self.nerModel = nerModel
        self.create_pipeline()

    def __call__(self, sent):
        # Call the model  for  entity
        # recognition  and return the
        # entities on single sentence

        # TODO:
        # 1. Call the model for entity recognition
        # 2. Return the entities on single sentence

        # Example:
        # sent = "ARR is $1.2 Bil for last year"
        # entities = {"ORG": [("ARR", 0, 2)],
        #             "MONEY": [("$1.2 Billion", 7, 14)],
        #             "DATE": [("last year", 20,28)]}
        # return entities

        doc = self.nerModel(sent)

        data = dict()

        for ent in doc.ents:
            label = ent.label_
            text = ent.text
            start = ent.start_char
            end = ent.end_char

            if label not in data:
                data[label] = []

            data[label].append((text, start, end))
        return data


    def create_pipeline(self):
        """
            If the model doesnt have inbuilt pipeline like spacy,  create one
            Currently we use a model with inbuilt pipeline.
        """        
        pass