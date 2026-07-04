import numpy as np

from backend.utils.similarity import batch_cosine_similarity, l2_normalize


def test_l2_normalize():
    matrix = np.array([[3.0, 0.0], [0.0, 4.0]], dtype=np.float32)
    normalized = l2_normalize(matrix)
    norms = np.linalg.norm(normalized, axis=1)
    np.testing.assert_allclose(norms, [1.0, 1.0], rtol=1e-5)


def test_batch_cosine_identical_vectors():
    vector = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    matrix = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float32,
    )
    scores = batch_cosine_similarity(vector, matrix)
    assert scores[0] > 0.99
    assert scores[1] < 0.01


def test_batch_cosine_best_match():
    query = [1.0, 0.0]
    candidates = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]]
    scores = batch_cosine_similarity(query, np.array(candidates, dtype=np.float32))
    assert int(np.argmax(scores)) == 0
