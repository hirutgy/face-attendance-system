import numpy as np
import onnxruntime as ort

from backend.config import MODEL_PATH

_session = None


def _get_session():
    global _session
    if _session is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"FaceNet model not found at {MODEL_PATH}. "
                "Run: python DOWNLOAD_FACENET.py or place facenet512.onnx in models_local/."
            )
        _session = ort.InferenceSession(str(MODEL_PATH))
    return _session


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.square(x)))


def get_embedding(face):
    face = np.asarray(face, dtype=np.float32)
    face = face / 255.0
    face = np.resize(face, (160, 160, 3))
    face = np.expand_dims(face, axis=0)

    session = _get_session()
    inputs = {session.get_inputs()[0].name: face}
    embedding = session.run(None, inputs)[0][0]
    embedding = l2_normalize(embedding)

    return embedding.tolist()
