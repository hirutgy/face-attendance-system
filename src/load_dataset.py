import deeplake
import numpy as np
from collections import Counter

def load_lfw():
    return deeplake.load('hub://activeloop/lfw')

def count_identities(ds):
    identity_key = "name"
    print(f"Using identity tensor: {identity_key}")

    labels = []
    for i in range(len(ds)):
        value = ds[identity_key][i].numpy()

        if isinstance(value, np.ndarray):
            value = value.item()

        labels.append(str(value))  # convert to string

    return Counter(labels)

def filter_valid_identities(counts, min_images=5):
    return [identity for identity, count in counts.items() if count >= min_images]
