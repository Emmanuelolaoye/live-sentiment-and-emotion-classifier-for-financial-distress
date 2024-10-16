import os
import shutil

# List of female ActorIDs
female_ids = [1002, 1003, 1004, 1006, 1007, 1008, 1009, 1010, 1012, 1013, 1018, 1020, 1021, 1024, 1025, 1028, 1029,
              1030, 1037, 1043, 1046, 1047, 1049, 1052, 1053, 1054, 1055, 1056, 1058, 1060, 1061, 1063, 1072, 1073,
              1074, 1075, 1076, 1078, 1079, 1082, 1084, 1089, 1091]

# Root directory of the dataset
root_dir = r"C:\Users\eo19181\Documents\CREMA\AudioWAV" # Replace with the actual path
# Directory to store sorted files
sorted_dir = r'C:\Users\eo19181\Documents\new'

# Make the sorted directory if it doesn't exist
os.makedirs(sorted_dir, exist_ok=True)


# Function to get gender from ActorID
def get_gender(actor_id):
    if actor_id in female_ids:
        return 'female'
    else:
        return 'male'


# Function to copy files to the sorted directory
def copy_files_by_gender_emotion():
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):  # Assuming the audio files are in .wav format
                parts = file.split('_')
                if len(parts) < 3:
                    continue  # Skip files that don't match the expected pattern

                actor_id = int(parts[0])
                emotion = parts[2]
                gender = get_gender(actor_id)
                new_dir = os.path.join(sorted_dir, gender, emotion)

                # Create the new directory if it doesn't exist
                os.makedirs(new_dir, exist_ok=True)

                # Copy the file to the new directory
                src_path = os.path.join(subdir, file)
                dest_path = os.path.join(new_dir, file)
                shutil.copy2(src_path, dest_path)
                print(f'Copied {src_path} to {dest_path}')


# Run the function to sort the files
copy_files_by_gender_emotion()