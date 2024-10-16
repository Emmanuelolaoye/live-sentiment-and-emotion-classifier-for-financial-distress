from textblob import TextBlob

text = "i hate Derrick Rose, he is terrible for the nba"


# sent = TextBlob(text)


# print(red + str(sent.sentiment) + END)


# def sentiment(text):
#     if TextBlob(text).polarity > 0.50:
#
#         return text, ': - Posivive'
#
#     else:
#         return text, ': - Negative'


class TextblobSentimentAnalyser:

    def get_sentiment(self, input_text):
        sentiment_analysis = TextBlob(input_text).sentiment
        compound_score = sentiment_analysis.polarity
        sentiment = "Positive" if compound_score > 0 else "Negative" if compound_score < 0 else "Neutral"
        return f"{sentiment}¦ {round(compound_score, 3)}"
#
# text_analyser = TextblobSentimentAnalyser(text)
# print(text_analyser.analyze(text))
# <<< Sentiment(polarity=-0.4000000000000001, subjectivity=0.9500000000000001)
