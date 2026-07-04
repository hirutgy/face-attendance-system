from deepface import DeepFace
from face_recognition import FaceRecognizer

recognizer = FaceRecognizer()

img_path = img_path = img_path = "data/lfw/1012/2140.jpg"


embedding = DeepFace.represent(
    img_path=img_path,
    model_name="Facenet512",
    enforce_detection=False
)[0]["embedding"]

label, score = recognizer.recognize(embedding)

print("Prediction:", label)
print("Similarity:", score)
