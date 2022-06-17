"""# Question Answering Module

Question answering module inherits utilities from the entity recognition module and is used to answer the questions.
"""

from entity_recognition import EntityRecognitionModule
class QuestionAnsweringModule(EntityRecognitionModule):
    def __init__(self, nerModel, qaModel):
        super(QuestionAnsweringModule, self).__init__(nerModel=nerModel)
        self.qaModel = qaModel

    def __call__(self, qs, ctx):
        # TODO:
        # 1. Call the model for question answering
        # 2. Return the answer on single sentence
        #    with highest score

        qs = qs.strip().lower()
        ctx = ctx.strip().lower()

        res = self.qaModel(question=qs, context=ctx)
        res = self.cleanAnswer(res, ctx)
        return res

    def cleanAnswer(self, res, ctx):
        # Logic for cleaning answer
        return res