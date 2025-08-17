# setup_database.py (Modified for 'NameRollNo' format)
import sqlite3
import os
import re # Import the regular expressions module

# --- Define the path to your dataset ---
dataset_path = "C:\\Users\\madee\\OneDrive\\Desktop\\minor\\New folder"


# --- Create Student Details Database ---
conn_students = sqlite3.connect('students.db')
cursor_students = conn_students.cursor()

cursor_students.execute('''
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# --- Dynamically add students from folder names ---
students_to_add = []
print("Reading student data from folders...")

for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)
    
    if os.path.isdir(folder_path):
        # Use regex to find a pattern of letters followed by numbers
        match = re.match(r'([a-zA-Z]+)(\d+)', folder_name)
        
        if match:
            # The first group is the name, the second is the roll number
            name = match.group(1)
            roll_no = int(match.group(2))
            students_to_add.append((roll_no, name))
            print(f"Found: Name={name}, Roll No={roll_no}")
        else:
            print(f"Skipping folder '{folder_name}' - does not match 'NameRollNo' format.")

if students_to_add:
    cursor_students.executemany('INSERT OR IGNORE INTO students (roll_no, name) VALUES (?, ?)', students_to_add)
    print("\nDatabase populated with custom student data.")

conn_students.commit()
conn_students.close()
# ... (rest of the script for attendance_log.db remains the same)