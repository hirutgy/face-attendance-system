import numpy as np
import cv2


def crop_face(img, box):
    x, y, w, h = box
    return img[y:y + h, x:x + w]


def align_face(img, keypoints):
    left_eye = keypoints["left_eye"]
    right_eye = keypoints["right_eye"]

    # Compute angle between eyes
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dy, dx))

    # Center between eyes
    eyes_center = (
        int((left_eye[0] + right_eye[0]) / 2),
        int((left_eye[1] + right_eye[1]) / 2),
    )

    # Rotation matrix
    M = cv2.getRotationMatrix2D(eyes_center, angle, 1.0)

    aligned = cv2.warpAffine(
        img,
        M,
        (img.shape[1], img.shape[0]),
    )

    return aligned