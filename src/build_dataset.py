import os
import cv2
import numpy as np

def build_dataset(ds, valid_ids, save_dir="data/lfw"):
    os.makedirs(save_dir, exist_ok=True)

    identity_key = "name"
    print(f"Using identity tensor: {identity_key}")

    for i in range(len(ds)):
        value = ds[identity_key][i].numpy()

        # Convert numpy array → python scalar
        if isinstance(value, np.ndarray):
            value = value.item()

        # Convert everything to string
        label = str(value)

        if label in valid_ids:
            img = ds.images[i].numpy()
            person_dir = os.path.join(save_dir, label)
            os.makedirs(person_dir, exist_ok=True)
            cv2.imwrite(os.path.join(person_dir, f"{i}.jpg"), img)
