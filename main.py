import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime
import re

# --- Pop-up Configuration ---
popup_timer = 0
popup_text = ""

# --- Load Known Encodings and Connect to Databases ---
print("[INFO] Loading encodings...")
try:
    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    print("[ERROR] 'encodings.pickle' not found. Please run the encode_faces.py script first.")
    exit()

try:
    conn_students = sqlite3.connect('students.db')
    cursor_students = conn_students.cursor()
    conn_attendance = sqlite3.connect('attendance.db')
    cursor_attendance = conn_attendance.cursor()
except sqlite3.Error as e:
    print(f"[ERROR] Database connection failed: {e}")
    exit()

# --- Create Attendance Table ---
cursor_attendance.execute('''
CREATE TABLE IF NOT EXISTS attendance_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no INTEGER NOT NULL,
    name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    date TEXT NOT NULL,
    UNIQUE(roll_no, name, date)
)
''')
conn_attendance.commit()

# --- Initialize Video Stream ---
print("[INFO] Starting video stream...")
vs = cv2.VideoCapture(0)
if not vs.isOpened():
    print("[ERROR] Cannot open camera.")
    exit()

# --- Main Loop ---
while True:
    ret, frame = vs.read()
    if not ret:
        print("[WARNING] Failed to grab frame.")
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb_frame, model='hog')
    encodings = face_recognition.face_encodings(rgb_frame, boxes)
    
    display_texts = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.6)
        name = "Unknown"
        roll_no = None

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            
            if counts:
                name = max(counts, key=counts.get)

            if name != "Unknown":
                try:
                    cursor_students.execute("SELECT roll_no FROM students WHERE name=?", (name,))
                    result = cursor_students.fetchone()

                    if result:
                        roll_no = result[0]
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        
                        cursor_attendance.execute(
                            "INSERT OR IGNORE INTO attendance_log (roll_no, name, timestamp, date) VALUES (?, ?, ?, ?)",
                            (roll_no, name, timestamp, current_date)
                        )
                        
                        # --- TRIGGER POP-UP ---
                        # Check if a new row was actually inserted
                        if cursor_attendance.rowcount > 0:
                            popup_text = "Attendance Marked"
                            popup_timer = 60  # Display for 60 frames
                        
                        conn_attendance.commit()

                except sqlite3.Error as e:
                    print(f"[ERROR] Database error: {e}")
        
        # --- Prepare the text for the face box ---
        if roll_no is not None:
            display_text = f"name: {name} roll no: {roll_no}"
        else:
            display_text = name
        display_texts.append(display_text)

    # --- Display the Results on the Frame ---
    for ((top, right, bottom, left), display_text) in zip(boxes, display_texts):
        color = (0, 255, 0) if "Unknown" not in display_text else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, display_text, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # --- DRAW THE POP-UP ---
    if popup_timer > 0:
        # Define pop-up box properties
        box_x, box_y, box_w, box_h = 10, 10, 300, 50
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 200, 0), -1)
        # Put text inside the box
        cv2.putText(frame, popup_text, (box_x + 20, box_y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        popup_timer -= 1

    # Show the final frame
    cv2.imshow("Attendance System - Press 'q' to quit", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# --- Cleanup ---
print("[INFO] Cleaning up and shutting down...")
vs.release()
cv2.destroyAllWindows()
conn_students.close()
conn_attendance.close()
