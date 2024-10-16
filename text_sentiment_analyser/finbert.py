# # from transformers import AutoTokenizer, AutoModelForSequenceClassification
# #
# # tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# # model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
# #
# #
# text1 = "i love derick rose he is great"
# text2 = "cannot believe that anyone would vote for such an evil man that is impossible"
#
# #
# # model_outputs = model(text)
# #
# # print(model_outputs)
#
#
# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
#
# from transformers import BertTokenizer, BertForSequenceClassification,  AutoTokenizer, 
# AutoModelForSequenceClassification from transformers import pipeline
#
#
#
#
# # finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
# # tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
#
# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
#
# nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
#
# sentences = ["there is a shortage of capital, and we need extra financing",
#              "growth is strong and we have plenty of liquidity",
#              "there are doubts about our finances",
#              "profits are flat"]
# results1 = nlp(text1)
# print(results1)
#
# results2 = nlp(text2)
# print(results2)
import warnings

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#
#
# # Load the dataset
# dataset = load_dataset("ugursa/Yahoo-Finance-News-Sentences")
# var = dataset["train"][100]
# print(var)
#
# # Load the tokenizer
# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
#
# # Tokenize function
# def tokenize_function(examples):
#     return tokenizer(examples["text"], padding="max_length", truncation=True)
#
# # Tokenize the dataset
# tokenized_datasets = dataset.map(tokenize_function, batched=True)
#
# # Select small datasets for training and evaluation
# small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(100))
# small_eval_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(100))
#
# # Load the metric
# metric = evaluate.load("accuracy")
# print(metric)
#
# # Compute metrics function
# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     return metric.compute(predictions=predictions, references=labels)
#
# # Load the model
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
# model.to(device)  # Move model to GPU if available
#
# training_args = TrainingArguments(
#     output_dir="saved_models/test_trainer",
#     evaluation_strategy="epoch",
#     per_device_train_batch_size=8,  # Adjust batch size according to your GPU memory
#     per_device_eval_batch_size=8,
#     num_train_epochs=1,  # Reduce the number of epochs for faster training
#     logging_dir="logs",  # Directory for storing logs
#     logging_steps=10,
# )
#
#
# # Define training arguments
# training_args = TrainingArguments(output_dir="saved_models/test_trainer", evaluation_strategy="epoch")
# print(training_args)
#
# # Initialize the Trainer
# from transformers import Trainer
#
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=small_train_dataset,
#     eval_dataset=small_eval_dataset,
#     compute_metrics=compute_metrics,
# )
#
# # Train the model
# trainer.train()
#
#
# # Save the fine-tuned model and tokenizer
# model.save_pretrained("fine_tuned_model")
# tokenizer.save_pretrained("fine_tuned_model")
#
# # metric = evaluate.load("accuracy")
# # print(metric)


from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments
import numpy as np
import torch
import scipy
from datasets import load_dataset
import evaluate

warnings.filterwarnings("ignore")

class FinBertSentimentAnalyser:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.model.to(self.device)

    def get_prediction(self, input_text):
        with torch.no_grad():
            inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
            outputs = self.model(**inputs)
            logit = outputs.logits
            predictions = torch.argmax(logit, dim=-1)

        return predictions, logit

    def get_sentiment(self, input_text):
        predictions, logit = self.get_prediction(input_text)

        # Assuming the model outputs 0, 1, 2 for Positive, Negative, Neutral respectively
        sentiment_map = {
            0: "Positive",
            1: "Negative",
            2: "Neutral"
        }

        predicted_class = predictions.item()
        sentiment = sentiment_map.get(predicted_class, "Unknown")

        softmax = torch.nn.functional.softmax(logit, dim=-1).cpu().numpy()[0]
        polarity_scores = [1, -1, 0]
        polarity = sum(p * s for p, s in zip(polarity_scores, softmax))

        return f"{sentiment}¦ {round(polarity, 3)}"

    def get_polarity(self, input_text):
        _, logits = self.get_prediction(input_text)
        softmax = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()[0]
        polarity_scores = [1, -1, 0]
        polarity = sum(p * s for p, s in zip(polarity_scores, softmax))

        return polarity

# # Example usage
# if __name__ == "__main__":
#     analyser = FinBertSentimentAnalyser()
#
#     text = "The company's growth is terrible."
#     sentiment = analyser.get_sentiment(text)
#     polarity = analyser.get_polarity(text)
#
#     print(f"Sentiment: {sentiment}")
#     print(f"Polarity: {polarity}")