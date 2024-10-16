from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NltkSentimentAnalyser:

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def get_sentiment(self, input_text):
        scores = self.vader.polarity_scores(input_text)
        compound_score = scores['compound']
        sentiment = "Positive" if compound_score >= 0.05 else "Negative" if compound_score <= -0.05 else "Neutral"
        return f"{sentiment}¦ {round(compound_score, 3)}"
