import sqlite3

# Connect to the attendance database
try:
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit()

print("--- Attendance Log ---")

# Fetch all records from the attendance_log table
try:
    cursor.execute("SELECT id, roll_no, name, timestamp FROM attendance_log")
    all_records = cursor.fetchall()

    if not all_records:
        print("No attendance records found.")
    else:
        # Print a header
        print(f"{'ID':<5} | {'Roll No':<10} | {'Name':<20} | {'Timestamp'}")
        print("-" * 60)
        # Print each record
        for record in all_records:
            id, roll_no, name, timestamp = record
            print(f"{id:<5} | {roll_no:<10} | {name:<20} | {timestamp}")

except sqlite3.Error as e:
    print(f"Failed to read records: {e}")

finally:
    # Close the connection
    conn.close()