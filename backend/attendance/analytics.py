import json
from collections import defaultdict
from datetime import datetime

ATTENDANCE_FILE = "backend/database/attendance.json"

def load_attendance():
    with open(ATTENDANCE_FILE, "r") as f:
        return json.load(f)

def compute_analytics():
    records = load_attendance()

    total_entries = len(records)

    # attendance count per person
    per_person = defaultdict(int)
    for r in records:
        per_person[r["name"]] += 1

    # attendance per day
    per_day = defaultdict(int)
    for r in records:
        day = r["timestamp"].split("T")[0]
        per_day[day] += 1

    # latest check-ins (sorted by timestamp)
    latest = sorted(records, key=lambda x: x["timestamp"], reverse=True)[:10]

    # average confidence
    avg_conf = sum(r["confidence"] for r in records) / total_entries if total_entries else 0

    return {
        "total_entries": total_entries,
        "per_person": dict(per_person),
        "per_day": dict(per_day),
        "latest_checkins": latest,
        "average_confidence": avg_conf
    }
