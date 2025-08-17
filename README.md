# Automated Attendance System using Real-Time Face Recognition
This project is an AI-powered application designed to automate the process of taking attendance using face recognition. It replaces manual roll calls by using a webcam to identify registered students in real-time and automatically logs their attendance into a database.

## Key Features
Real-Time Face Detection: Automatically detects and locates human faces from a live webcam feed.

High-Accuracy Recognition: Identifies known individuals by comparing them against a pre-encoded database of faces.

Automated Attendance Logging: Records the name, roll number, and a precise timestamp for each recognized student into an SQLite database.

Duplicate Prevention: Ensures a student's attendance is marked only once per day.



# 🛠️ Tech Stack
Language: Python

Computer Vision: OpenCV

Face Recognition: face_recognition (built on dlib's deep learning model)

Database: SQLite

Web Framework (Optional): Flask

# 📂 Project Structure
 The project consists of several key files and folders:

New folder/: The directory where you must place your student image sub-folders.

faces.py: Script to encode the faces from the image dataset.

database.py: Script to create the student information database.

recognize_and_attend.py: The main application for live recognition.

view_attendance.py: A utility to view attendance logs in the terminal.

.gitignore: Specifies which files for Git to ignore.

requirements.txt: Lists all the project's Python dependencies.

# ⚙️ How It Works
The system operates in three main stages:

Face Encoding (faces.py): The script processes a collection of photos for each student. It uses a pre-trained deep learning model to learn the unique facial features of every individual and stores this information as a mathematical "encoding" in the encodings.pickle file.

Database Setup (database.py): This script creates an SQLite database (students.db) that links each student's name to their official roll number, acting as the class roster.

Live Recognition (recognize_and_attend.py): The main application activates the webcam, detects faces in the video feed, and compares them against the stored encodings. Upon a successful match, it looks up the student's roll number and saves their attendance with a timestamp into the attendance.db.

# 🚀 Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the Repository
git clone [https://github.com/your-username/Your-Repo-Name.git](https://github.com/your-username/Your-Repo-Name.git)
cd Your-Repo-Name

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to keep project dependencies isolated.

# For Windows
python -m venv myvenv
myvenv\Scripts\activate

# For macOS/Linux
python3 -m venv myvenv
source myvenv/bin/activate

3. Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

#4. Prepare the Image Dataset
Create a folder named New folder in the main project directory.

Inside New folder, create a sub-folder for each student.

IMPORTANT: Name each sub-folder in the format NameRollNo (e.g., Madeeha101, John205).

Place several clear, well-lit photos of each student inside their respective folder.

5. Run the Initial Setup Scripts
You must run these two scripts once to build your face database.

Encode the faces:

python faces.py

This will create the encodings.pickle file.

Set up the student database:

python database.py

This will create the students.db file.

# ▶️ How to Run the Application
Once the setup is complete, you can start the main attendance system.

python recognize_and_attend.py

A window will open showing your webcam feed. When a registered person is recognized, their name and roll number will be displayed, and their attendance will be marked. Press 'q' to quit the application.

# 📊 Viewing Attendance Records
You can view the logged attendance in two ways:

Using the provided script:
Run the view_attendance.py script to see a formatted list in your terminal.

python view_attendance.py

Using a Database Browser:
Use a free tool like DB Browser for SQLite to open the attendance.db file and view the attendance_log table.
