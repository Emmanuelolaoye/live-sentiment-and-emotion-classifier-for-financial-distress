import datetime
from datetime import datetime
import os
import json

"""
2024-07-29 07:02:49.523986
Current date and time : 
29-07-2024 - 07:02:49
"""

# # Get the current date and time
# now = datetime.now()
#
# print(now)
#
# print("Current date and time : ")
#
# # Print the current date and time in a specific format
# json_name = now.strftime("%d-%m-%Y - %H:%M:%S")

dictionary = {
    "date": "2024-07-29 07:02:49.523986",
    "text": "Another sample text",
    "fine-tuned finBert": "neutral",
}


class Json:
    def __init__(self, filename=None):
        self.directory = "json_files"
        self.filepath = None
        self.data = []
        # Create a directory for storing JSON files if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if filename:
            self.load_file(os.path.join(self.directory, filename))
        else:
            self.create_file()

    def create_file(self):
        # Generate a filename with the current date-time
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")
        self.filepath = os.path.join(self.directory, filename)
        # Create an empty list to store content
        self.data = []
        # Write an empty list to the new JSON file
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Created new file: {self.filepath}")

    def add_content(self, date, text, sentiments, emotions):
        if self.filepath is None:
            raise ValueError("No file has been created yet.")

        # Add new content to the data list
        new_content = {
            "date": date,
            "text": text,
            "sentiments": sentiments,
            "emotions": emotions
        }

        self.data.append(new_content)
        # Write the updated data to the JSON file
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)
        # print(f"Added new content to {self.filepath}")

    def display_content(self):
        # Display the current content of the JSON file
        print(json.dumps(self.data, indent=4))

    def load_file(self, filepath):
        # Load data from an existing JSON file
        if not os.path.exists(filepath):
            raise ValueError("File does not exist.")
        self.filepath = filepath
        with open(self.filepath, 'r') as file:
            self.data = json.load(file)
        print(f"Loaded data from {self.filepath}")

    def update_content(self, index, date=None, text=None, sentiments=None, emotions=None):
        if self.filepath is None:
            raise ValueError("No file has been loaded yet.")
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range.")

        # Update the content at the specified index
        if date is not None:
            self.data[index]['date'] = date
        if text is not None:
            self.data[index]['text'] = text
        if sentiments is not None:
            self.data[index]['sentiments'] = sentiments
        if emotions is not None:
            self.data[index]['emotions'] = emotions

        # Write the updated data to the JSON file
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Updated content at index {index} in {self.filepath}")

    def delete_content(self, index):
        if self.filepath is None:
            raise ValueError("No file has been loaded yet.")
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range.")

        # Delete the content at the specified index
        self.data.pop(index)

        # Write the updated data to the JSON file
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"Deleted content at index {index} from {self.filepath}")


# Example usage:
# sentiment_json = JsonHandler()  # Creates a new file
# sentiment_json.add_content("2024-07-29", "This is a sample text.", "Positive")
# sentiment_json.display_content()
# sentiment_json.update_content(0, text="Updated sample text.")
# sentiment_json.display_content()
# sentiment_json.delete_content(0)
# sentiment_json.display_content()

# Or loading an existing file:
# sentiment_json = JsonHandler("existing_file.json")  # Loads the specified file
# sentiment_json.add_content("2024-07-29", "This is a sample text.", "Positive")
# sentiment_json.display_content()

# Usage example
if __name__ == "__main__":
    # # Create an instance of the SentimentJSON class
    # sentiment_json = Json()
    # # Create a new JSON file
    # sentiment_json.create_file()
    # # Add content to the JSON file
    # sentiment_json.add_content(
    #     date="2024-07-29 07:02:49.523986",
    #     text="Another sample text",
    #     sentiments={
    #         "nltk": 0.3,
    #         "textBlob": 0.4,
    #         "finbert": 0.2,
    #         "lstm": 0.6
    #     }
    # )

    # Or loading an existing file:
    sentiment_json = Json("2024-07-29-22-36-45.json")  # Loads the specified file
    sentiment_json.add_content("2024-07-29", "This is a sample text.", "Positive")

    # Display the current content of the JSON file
    sentiment_json.display_content()
