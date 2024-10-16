from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

text = "i hate Derrick Rose, he is terrible for the nba"

# vader = SentimentIntensityAnalyzer()
# sentiment = vader.polarity_scores(text)
# print(sentiment)
# for i in sentiment.keys():
#     print(i)

class NltkSentimentAnalyser:

    def __init__(self, text):
        self.text = text

    def get_sentiment(self):
        vader = SentimentIntensityAnalyzer()
        return vader.polarity_scores(self.text)


# nltk_analyser = NltkSentimentAnalyser(text)
# print(nltk_analyser.get_sentiment())
