from text_sentiment_analyser.Nltk_Vader import NltkSentimentAnalyser
from text_sentiment_analyser.Text_Blob import TextblobSentimentAnalyser
from text_sentiment_analyser.finbert import FinBertSentimentAnalyser
from text_sentiment_analyser.finetuned_finbert import FineTunedFinBertSentimentAnalyser
from text_sentiment_analyser.roberta import RobertaSentimentAnalyser


class Text:
    def __init__(self, text):
        self.text = text

    def get_text(self):  #: str:text
        return self.text

    @staticmethod
    def dict_to_string(dictionary):
        return str(dictionary)

    def get_nltk_sentiment(self, to_dictionary=True):  # str: NLTK sentiment
        nltk_analyser = NltkSentimentAnalyser()
        sentiment = nltk_analyser.get_sentiment(self.text)

        return sentiment

    def get_text_blob_sentiment(self):
        text_blob_analyser = TextblobSentimentAnalyser()
        sentiment = text_blob_analyser.get_sentiment(self.text)

        return sentiment

    def get_finbert_sentiment(self):
        finbert_analyser = FinBertSentimentAnalyser()
        sentiment = finbert_analyser.get_sentiment(self.text)

        return sentiment

    def finbert_polarity(self):
        finbert = FinBertSentimentAnalyser()
        polarity = finbert.get_polarity(self.text)

        return polarity

    def get_finetuned_finbert_sentiment(self):
        finbert_analyser = FineTunedFinBertSentimentAnalyser()
        sentiment = finbert_analyser.get_sentiment(self.text)

        return sentiment

    def get_roberta_sentiment(self):
        roberta_analyser = RobertaSentimentAnalyser()
        sentiment = roberta_analyser.get_sentiment(self.text)
        return sentiment


# if __name__ == '__main__':
#     text = Text("i love derrick rose")
#
#
#     print(text.get_roberta_sentiment(), "roberta sentiment")
#     print(text.get_finbert_sentiment(), "finbert sentiment")
#     print(text.get_nltk_sentiment(), "nltk sentiment", )
#     print(text.get_text_blob_sentiment(), "text blob sentiment")


