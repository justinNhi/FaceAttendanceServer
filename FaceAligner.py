import cv2
import numpy as np
import dlib


def shape_to_np(shape):
    coords = np.zeros((shape.num_parts, 2), dtype="int")
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


class FaceAligner:
    def __init__(self, desiredLeftEye=(0.35, 0.35), desiredFaceWidth=150, desiredFaceHeight=None):
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.desiredLeftEye = desiredLeftEye
        self.desiredFaceWidth = desiredFaceWidth
        self.desiredFaceHeight = desiredFaceHeight

        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth

    def align(self, image, rect):
        try:
            shape = self.predictor(image, rect)
            shape = shape_to_np(shape)

            leftEyePts = shape[42:48]
            rightEyePts = shape[36:42]

            leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
            rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

            dY = leftEyeCenter[1] - rightEyeCenter[1]
            dX = leftEyeCenter[0] - rightEyeCenter[0]

            angle = np.degrees(np.arctan2(dY, dX))
            desiredRightEyeX = 1.0 - self.desiredLeftEye[0]
            dist = np.sqrt((dX ** 2) + (dY ** 2))
            desiredDist = (desiredRightEyeX - self.desiredLeftEye[0])
            desiredDist = desiredDist * self.desiredFaceWidth
            scale = desiredDist / dist

            eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2, (leftEyeCenter[1] + rightEyeCenter[1]) // 2)

            M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

            tX = self.desiredFaceWidth * 0.5
            tY = self.desiredFaceHeight * self.desiredLeftEye[1]

            M[0, 2] += (tX - eyesCenter[0])
            M[1, 2] += (tY - eyesCenter[1])

            output = cv2.warpAffine(image, M, (self.desiredFaceWidth, self.desiredFaceHeight), flags=cv2.INTER_CUBIC)

            return output
        except Exception as e:
            print(e)
