import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDINGS_FILE = "data/embeddings_facenet.pkl"

class FaceRecognizer:
    def __init__(self, embeddings_file=EMBEDDINGS_FILE, threshold=0.35):
        data = pickle.load(open(embeddings_file, "rb"))
        self.embeddings = np.array(data["embeddings"])
        self.labels = np.array(data["labels"])
        self.threshold = threshold

    def recognize(self, embedding):
        embedding = np.array(embedding).reshape(1, -1)

        sims = cosine_similarity(embedding, self.embeddings)[0]
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]

        if best_score >= self.threshold:
            return self.labels[best_idx], best_score
        else:
            return "Unknown", best_score
