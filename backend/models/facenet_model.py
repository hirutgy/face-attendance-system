import cv2
import numpy as np
import onnxruntime as ort

from backend.config import MODEL_PATH

_session = None
_input_size = None


def _get_session():
    global _session, _input_size
    if _session is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"FaceNet model not found at {MODEL_PATH}. "
                "Run: python DOWNLOAD_FACENET.py or place facenet512.onnx in models_local/."
            )
        _session = ort.InferenceSession(str(MODEL_PATH))
        shape = _session.get_inputs()[0].shape
        # Expected NCHW: [batch, 3, H, W]
        height = shape[2] if len(shape) >= 4 and isinstance(shape[2], int) else 160
        width = shape[3] if len(shape) >= 4 and isinstance(shape[3], int) else 160
        _input_size = (width, height)
    return _session


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.square(x)))


def get_embedding(face):
    face = np.asarray(face, dtype=np.float32)

    session = _get_session()
    width, height = _input_size
    face = cv2.resize(face, (width, height))

    # Normalize to [0, 1]
    face = face / 255.0

    # HWC -> CHW, then add batch dimension
    face = np.transpose(face, (2, 0, 1))
    face = np.expand_dims(face, axis=0)

    inputs = {session.get_inputs()[0].name: face.astype(np.float32)}

    embedding = session.run(None, inputs)[0]
    embedding = np.asarray(embedding, dtype=np.float32).reshape(-1)

    if embedding.size != 512:
        raise ValueError(
            f"Expected 512-dimensional embedding, got {embedding.size}"
        )

    embedding = l2_normalize(embedding)

    return embedding.tolist()