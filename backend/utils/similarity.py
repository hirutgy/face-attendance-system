import numpy as np


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-12)
    return matrix / norms


def batch_cosine_similarity(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Return cosine similarity between one query vector and each row in matrix."""
    query = np.asarray(query, dtype=np.float32)
    matrix = np.asarray(matrix, dtype=np.float32)

    query_norm = query / max(np.linalg.norm(query), 1e-12)
    matrix_norm = l2_normalize(matrix)
    return matrix_norm @ query_norm
