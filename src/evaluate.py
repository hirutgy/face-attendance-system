import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load train and test embeddings
train = pickle.load(open("data/train_embeddings.pkl", "rb"))
test = pickle.load(open("data/test_embeddings.pkl", "rb"))

X_train = np.array(train["embeddings"])
y_train = np.array(train["labels"])

X_test = np.array(test["embeddings"])
y_test = np.array(test["labels"])

# Predict using cosine similarity
preds = []
for emb in X_test:
    sims = cosine_similarity(emb.reshape(1, -1), X_train)[0]
    best_idx = np.argmax(sims)
    preds.append(y_train[best_idx])

# Metrics
accuracy = accuracy_score(y_test, preds)
precision = precision_score(y_test, preds, average="macro", zero_division=0)
recall = recall_score(y_test, preds, average="macro", zero_division=0)
f1 = f1_score(y_test, preds, average="macro", zero_division=0)

cm = confusion_matrix(y_test, preds)
report = classification_report(y_test, preds, zero_division=0)

# Print to terminal
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("\nConfusion Matrix:\n", cm)
print("\nClassification Report:\n", report)

# Save everything to a file
with open("evaluation_report.txt", "w") as f:
    f.write("=== Face Recognition Evaluation Report ===\n\n")
    f.write(f"Accuracy: {accuracy}\n")
    f.write(f"Precision (macro): {precision}\n")
    f.write(f"Recall (macro): {recall}\n")
    f.write(f"F1 Score (macro): {f1}\n\n")
    
    f.write("Confusion Matrix:\n")
    f.write(str(cm))
    f.write("\n\nClassification Report:\n")
    f.write(report)

print("\nSaved full evaluation to evaluation_report.txt")
