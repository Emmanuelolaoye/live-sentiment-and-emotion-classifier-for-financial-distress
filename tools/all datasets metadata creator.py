import os
import pandas as pd

# Define the root directory of the datasets
root_dir = r"C:\Users\eo19181\Documents\All -  Datasets"

# List to store the information for the CSV
data = []

# Walk through the directory
for dataset in os.listdir(root_dir):
    dataset_path = os.path.join(root_dir, dataset)
    if os.path.isdir(dataset_path):
        for gender in os.listdir(dataset_path):
            gender_path = os.path.join(dataset_path, gender)
            if os.path.isdir(gender_path):
                for emotion in os.listdir(gender_path):
                    emotion_path = os.path.join(gender_path, emotion)
                    if os.path.isdir(emotion_path):
                        for file in os.listdir(emotion_path):
                            if file.endswith('.wav') or file.endswith('.mp4'):
                                file_path = os.path.join(emotion_path, file)
                                label = f"{gender.lower()}_{emotion.lower()}"
                                data.append({
                                    'labels': label,
                                    'source': dataset,
                                    'path': file_path
                                })

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_csv_path = r"C:\Users\eo19181\Documents\All -  Datasets\data_paths.csv"
df.to_csv(output_csv_path, index=False)

print(f"CSV file has been created at {output_csv_path}")
