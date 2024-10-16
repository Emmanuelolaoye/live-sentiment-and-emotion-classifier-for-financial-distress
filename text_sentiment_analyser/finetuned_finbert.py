# import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

token = '' # access token deleted and rotated


class FineTunedFinBertSentimentAnalyser:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            r"M:\22-24_CE901-CE911-CF981-SU_olaoye_emmanuel_o\text_sentiment_analyser\saved_models\fine_tuned_model")
        self.tokenizer = AutoTokenizer.from_pretrained(
            r"M:\22-24_CE901-CE911-CF981-SU_olaoye_emmanuel_o\text_sentiment_analyser\saved_models\fine_tuned_model")  # , token=token
        self.model.to(self.device)

    def get_prediction(self, input_text):
        # start_time = time.time()
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)

        # end_time = time.time()
        # elapsed_time = end_time - start_time

        # print(f"Predictions: {predictions}")
        # print(f"Time taken for prediction: {elapsed_time} seconds")
        return predictions, logits

    def get_sentiment(self, input_text):
        # print("got into finbert sentiment")
        predictions, logits = self.get_prediction(input_text)
        # print(f"prediction {predictions}")

        # Assuming the model outputs 0, 1, 2 for Negative, Positive, Neutral respectively
        sentiment_map = {
            0: "Positive",
            1: "Negative",
            2: "Neutral"
        }

        # Get the predicted class index from the tensor
        predicted_class = predictions.item()

        # Retrieve the corresponding sentiment from the sentiment map
        sentiment = sentiment_map.get(predicted_class, "Unknown")

        softmax = torch.nn.functional.softmax(logits, dim=-1)  # calculated compound score using softmax
        compound_score = softmax.max().item()

        return f"{sentiment} - {round(compound_score, 3)}"

# Example usage:
# finbert_analyser = FinBertSentimentAnalyser()
# sentiment = finbert_analyser.get_sentiment("i love derrick rose")
# print(f"Sentiment: {sentiment}")
