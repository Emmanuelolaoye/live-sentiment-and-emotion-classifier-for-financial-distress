import os
import shutil

# Root directory of the dataset
root_dir = r'C:\Users\eo19181\Downloads\RAVDESS - Audio_Speech_Actors_01-24'  # Replace with the actual path
# Directory to store sorted files
sorted_dir = r'C:\Users\eo19181\Documents\RAVDESS - Dataset'

# Make the sorted directory if it doesn't exist
os.makedirs(sorted_dir, exist_ok=True)


# Function to get gender from ActorID
def get_gender(actor_id):
    return 'female' if actor_id % 2 == 0 else 'male'


# Emotion mapping based on provided rules
emotion_map = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}


# Function to copy files to the sorted directory
def copy_files_by_gender_emotion():
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):  # Assuming the audio files are in .mp4 format
                parts = file.split('-')
                if len(parts) != 7:
                    continue  # Skip files that don't match the expected pattern

                modality = parts[0]
                vocal_channel = parts[1]
                emotion = parts[2]
                intensity = parts[3]
                statement = parts[4]
                repetition = parts[5]
                actor_id = int(parts[6].split('.')[0])

                gender = get_gender(actor_id)
                emotion_str = emotion_map.get(emotion, 'unknown')
                new_dir = os.path.join(sorted_dir, gender, emotion_str)

                # Create the new directory if it doesn't exist
                os.makedirs(new_dir, exist_ok=True)

                # Copy the file to the new directory
                src_path = os.path.join(subdir, file)
                dest_path = os.path.join(new_dir, file)
                shutil.copy2(src_path, dest_path)
                print(f'Copied {src_path} to {dest_path}')


# Run the function to sort the files
copy_files_by_gender_emotion()
