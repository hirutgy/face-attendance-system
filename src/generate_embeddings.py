import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"   # REQUIRED FIX

from deepface import DeepFace
import numpy as np
import cv2
import pickle

DATASET_DIR = "data/lfw"
EMBEDDINGS_FILE = "data/embeddings_facenet.pkl"

def get_image_paths(dataset_dir):
    image_paths = []
    labels = []

    for person_name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, person_name)

        if not os.path.isdir(person_dir):
            continue

        for img_file in os.listdir(person_dir):
            if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                image_paths.append(os.path.join(person_dir, img_file))
                labels.append(person_name)

    return image_paths, labels

def generate_embedding(image_path):
    try:
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet512",   # FIXED
            enforce_detection=False
        )
        return embedding[0]["embedding"]
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    print("Loading dataset...")
    image_paths, labels = get_image_paths(DATASET_DIR)
    print(f"Found {len(image_paths)} images.")

    embeddings = []
    valid_labels = []

    print("Generating FaceNet512 embeddings...")

    for img_path, label in zip(image_paths, labels):
        emb = generate_embedding(img_path)
        if emb is not None:
            embeddings.append(emb)
            valid_labels.append(label)

    embeddings = np.array(embeddings)

    print(f"Generated {len(embeddings)} embeddings.")

    print("Saving embeddings...")
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump({"embeddings": embeddings, "labels": valid_labels}, f)

    print(f"Embeddings saved to {EMBEDDINGS_FILE}")

if __name__ == "__main__":
    main()
