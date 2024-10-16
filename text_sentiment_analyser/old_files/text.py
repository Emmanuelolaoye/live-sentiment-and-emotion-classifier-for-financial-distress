
import ast

from text_sentiment_analyser import Nltk_Vader
from text_sentiment_analyser import Text_Blob

text = "i hate Derrick Rose, he is terrible for the nba"


class Text:


    def __init__(self, text):
        self.text = text
        self.sentiment = 0
        self.sentiment_score = 0
        self.polarity = 0
        self.subjectivity = 0
        self.polarity_score = 0
        self.subjectivity_score = 0
        self.polarity_sentiment = 0
        self.subjectivity_sentiment = 0
        self.polarity_sentiment_score = 0
        self.subjectivity_sentiment_score = 0

    def get_text(self):
        return self.text


    def spilt_text(self): pass


    def get_text_blob_sentiment(self): pass

    def get_nltk_sentiment(self, to_dictionary):
        nltk_analyser = Nltk_Vader.NltkSentimentAnalyser(self.text)

        if to_dictionary:
            return self.dict_to_string(nltk_analyser.get_sentiment())

        # print(nltk_analyser.get_sentiment())
        return nltk_analyser.get_sentiment()


    def dict_to_string(self, dictionary):
        return str(dictionary)

    def get_sentiment(self): pass

    def get_sentiment_score(self): pass

    def get_polarity(self): pass

    def get_subjectivity(self): pass

    def get_polarity_score(self): pass

    def get_subjectivity_score(self): pass

    def get_polarity_sentiment(self): pass

    def get_subjectivity_sentiment(self): pass

    def get_polarity_sentiment_score(self): pass

    def get_subjectivity_sentiment_score(self): pass


# nltk = Text(text)
# example = nltk.get_text()
# print(example)
# nltk_sentiment = nltk.get_nltk_sentiment()
# print(nltk_sentiment)