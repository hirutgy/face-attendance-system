import cv2
import pickle
import numpy as np
import json
from datetime import datetime
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

# Load full training embeddings
train = pickle.load(open("data/train_embeddings.pkl", "rb"))
X_train = np.array(train["embeddings"])
y_train = np.array(train["labels"])   # labels are STRINGS

# Load ID → Name mapping
with open("data/id_to_name.json", "r") as f:
    id_to_name = json.load(f)

# Attendance file
ATTENDANCE_FILE = "attendance.csv"

def mark_attendance(person_id, person_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ATTENDANCE_FILE, "a") as f:
        f.write(f"{person_id},{person_name},{now}\n")
    print(f"Attendance logged for {person_name} at {now}")

# Step 1: Student enters ID (STRING)
target_id = input("Enter your ID: ").strip()

# Filter embeddings for this ID (STRING comparison)
id_embeddings = X_train[y_train == target_id]

if len(id_embeddings) == 0:
    print("ID not found in dataset.")
    exit()

# Lookup name
person_name = id_to_name.get(target_id, "Unknown")

print(f"Loaded {len(id_embeddings)} stored images for {person_name} (ID {target_id})")

# Step 2: Start webcam
cap = cv2.VideoCapture(0)
print("Show your face to the camera...")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Detect face + get embedding + bounding box
        result = DeepFace.represent(
            frame,
            model_name="Facenet512",
            detector_backend="retinaface",
            enforce_detection=False
        )

        emb = np.array(result[0]["embedding"])
        region = result[0]["facial_area"]  # bounding box

        x, y, w, h = region["x"], region["y"], region["w"], region["h"]

        # Compare only with this ID's embeddings
        sims = cosine_similarity(emb.reshape(1, -1), id_embeddings)[0]
        best_score = np.max(sims)

        if best_score > 0.70:
            text = f"{person_name} ({best_score:.2f})"
            color = (0, 255, 0)  # green
            mark_attendance(target_id, person_name)
        else:
            text = "Face does NOT match ID"
            color = (0, 0, 255)  # red

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Draw label above box
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    except Exception:
        cv2.putText(frame, "No face detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("ID Verification Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
