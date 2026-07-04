import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("backend/models/facenet512.onnx")

def l2_normalize(x):
    return x / np.sqrt(np.sum(np.square(x)))

def get_embedding(face):
    face = face.astype('float32')
    face = face / 255.0
    face = np.resize(face, (160, 160, 3))
    face = np.expand_dims(face, axis=0)

    inputs = {session.get_inputs()[0].name: face}
    embedding = session.run(None, inputs)[0][0]
    embedding = l2_normalize(embedding)

    return embedding.tolist()
