import pickle
import numpy as np
from sklearn.model_selection import train_test_split

data = pickle.load(open("data/embeddings_facenet.pkl", "rb"))

X = np.array(data["embeddings"])
y = np.array(data["labels"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

pickle.dump({"embeddings": X_train, "labels": y_train}, open("data/train_embeddings.pkl", "wb"))
pickle.dump({"embeddings": X_test, "labels": y_test}, open("data/test_embeddings.pkl", "wb"))

print("Train/Test split complete.")
print("Train size:", len(X_train))
print("Test size:", len(X_test))
