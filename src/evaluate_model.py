import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score

train = pickle.load(open("data/train_embeddings.pkl", "rb"))
test = pickle.load(open("data/test_embeddings.pkl", "rb"))

X_train = np.array(train["embeddings"])
y_train = np.array(train["labels"])

X_test = np.array(test["embeddings"])
y_test = np.array(test["labels"])

preds = []

for emb in X_test:
    sims = cosine_similarity(emb.reshape(1, -1), X_train)[0]
    best_idx = np.argmax(sims)
    preds.append(y_train[best_idx])

acc = accuracy_score(y_test, preds)

print("Test Accuracy:", acc)
