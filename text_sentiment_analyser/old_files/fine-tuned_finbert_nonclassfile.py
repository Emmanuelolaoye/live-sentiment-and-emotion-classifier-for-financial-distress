import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Start timing the entire program
program_start_time = time.time()

# Check if GPU is available (optional, since we are focusing on CPU optimization)
device = torch.device("cpu")

# Load the fine-tuned model and tokenizer (this should be done once and reused)
model = AutoModelForSequenceClassification.from_pretrained("../saved_models/fine_tuned_model")
tokenizer = AutoTokenizer.from_pretrained("../saved_models/fine_tuned_model")
model.to(device)  # Ensure the model is on CPU


# Example usage: Tokenize input text and get model predictions
def get_prediction(input_text):
    start_time = time.time()
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)

    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Predictions: {predictions}")
    print(f"Time taken for prediction: {elapsed_time} seconds")


# Example prediction
get_prediction("i love derrick rose")

# End timing the entire program
program_end_time = time.time()
total_program_time = program_end_time - program_start_time

print(f"Total time taken for the program: {total_program_time} seconds")
