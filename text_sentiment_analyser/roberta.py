#%% md

#%%
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
#%%
class RobertaSentimentAnalyser:

    def __init__(self):
        self.device = torch.device("cpu")
        self.model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        self.model.to(self.device)

#%%

    def get_prediction(self, input_text):
        with torch.no_grad():
            inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = self.model(**inputs)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)


        return predictions , logits

    def get_sentiment(self, input_text):
        # print("got into finbert sentiment")
        predictions, logits = self.get_prediction(input_text)
        # print(f"prediction {predictions}")

        # Assuming the model outputs 0, 1, 2 for Negative, Positive, Neutral respectively
        sentiment_map = {
            0: "Negative",
            1: "Neutral",
            2: "Positive",

        }

        # Get the predicted class index from the tensor
        predicted_class = predictions.item()

        # Retrieve the corresponding sentiment from the sentiment map
        sentiment = sentiment_map.get(predicted_class, "Unknown")
        softmax = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()[0]
        polarity_scores = [1, -1, 0]
        polarity = sum(p * s for p, s in zip(polarity_scores, softmax))

        return f"{sentiment}¦ {round(polarity, 3)}"

#%%
# roberta = RobertaSentimentAnalyser()
# #%%
# sentiment = roberta.get_sentiment("we are down in operating profits since last year")
# print(sentiment)
# #%%
