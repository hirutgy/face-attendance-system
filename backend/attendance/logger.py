import json
from datetime import datetime

ATTENDANCE_FILE = "backend/database/attendance.json"

def load_attendance():
    with open(ATTENDANCE_FILE, "r") as f:
        return json.load(f)

def save_attendance(records):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(records, f, indent=4)

def log_attendance(name, confidence):
    records = load_attendance()

    entry = {
        "name": name,
        "confidence": float(confidence),
        "timestamp": datetime.now().isoformat()
    }

    records.append(entry)
    save_attendance(records)

    return entry
