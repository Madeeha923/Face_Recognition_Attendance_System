# encode_faces.py (Modified for 'NameRollNo' format)
import face_recognition
import cv2
import os
import pickle
import re # Import the regular expressions module

dataset_path = "New folder/"
known_encodings = []
known_names = []

# Loop through all items in the dataset path
for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)
    
    # --- FIX: ADD THIS CHECK ---
    # This line ensures we only process folders, and skip any loose files
    if not os.path.isdir(folder_path):
        continue # Skips to the next item in the loop

    # Use the same regex logic to extract the name
    match = re.match(r'([a-zA-Z]+)(\d+)', folder_name)
    if not match:
        print(f"Skipping folder '{folder_name}' as it's not in the 'NameRollNo' format.")
        continue
    
    name = match.group(1) # Extract the name

    # Now, loop through the images inside the valid folder
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        
        # Read the image
        image = cv2.imread(image_path)
        
        # Check if image was loaded successfully
        if image is None:
            print(f"Warning: Could not read image {image_path}. Skipping.")
            continue
            
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        boxes = face_recognition.face_locations(rgb_image, model='hog')
        encodings = face_recognition.face_encodings(rgb_image, boxes)
        
        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name) # Save the correct name

print("Processing complete.")

# Check if any faces were found before creating the file
if known_encodings:
    with open("encodings.pickle", "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)
    print("Encodings created successfully.")
else:
    print("No faces were found in the dataset. 'encodings.pickle' was not created.")

