from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(r"F:\FYP\CODE\sleepv1.0\img6.jpg")
image = imutils.resize(image, width=500)

image.shape
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray.shape

# cv2.imshow('gray', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# TODO:
# The first parameter to the detector is our grayscale image (although this method
#  can work with color images as well).
# The second parameter is the number of image pyramid layers to apply when
# upscaling the image prior to applying the detector (this it the equivalent of
# computing cv2.pyrUp N number of times on the image).
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("F:\FYP\CODE\sleepv1.0\shape_predictor_68_face_landmarks.dat")

rects = detector(gray, 1)
rects


def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    # return a tuple of (x, y, w, h)
    return [x, y, w, h]


def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    # return the list of (x, y)-coordinates
    return coords


faces = []
dimensions = []
shape = []
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array

    # convert dlib's rectangle to a OpenCV-style bounding box
    # [i.e., (x, y, w, h)], then draw the face bounding box
    dimensions.append(rect_to_bb(rect))
    faces.append(dimensions[i][2] * dimensions[i][3])

    shape1 = predictor(gray, rect)
    shape1 = face_utils.shape_to_np(shape1)

    shape.append(shape1)


max_ind = np.argmax(faces)
cv2.rectangle(image, (dimensions[max_ind][0], dimensions[max_ind][1]),
              (dimensions[max_ind][0] + dimensions[max_ind][2], dimensions[max_ind][1] + dimensions[max_ind][3]), (0, 255, 0), 2)
cv2.putText(image, "Face #{}".format(i + 1), (dimensions[max_ind][0] - 10, dimensions[max_ind][1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# for (i, shape) in enumerate(shape[np.argmax(faces)]):
#     cv2.circle(image, (shape[np.argmax(faces)][0], y), 1, (0, 0, 255), -1)

for (x, y) in shape[np.argmax(faces)]:
    cv2.circle(image, (x, y), 1, (0, 0, 255), -1)


cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# ------------------------------------------------------------------------
# TODO: rough work
rects
rect
type(shape)

rect.top()
rect.left()
rect.right()
rect.bottom()
shape.shape  # 68 landmarks
gray.shape
gray
shape[:5]

faces = []
dimensions = []
shape = []
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array

    # convert dlib's rectangle to a OpenCV-style bounding box
    # [i.e., (x, y, w, h)], then draw the face bounding box
    dimensions.append(rect_to_bb(rect))
    faces.append(dimensions[i][2] * dimensions[i][3])

    shape1 = predictor(gray, rect)
    shape1 = face_utils.shape_to_np(shape1)

    shape.append(shape1)


max_ind = np.argmax(faces)
cv2.rectangle(image, (dimensions[max_ind][0], dimensions[max_ind][1]),
              (dimensions[max_ind][0] + dimensions[max_ind][2], dimensions[max_ind][1] + dimensions[max_ind][3]), (0, 255, 0), 2)
cv2.putText(image, "Face #{}".format(i + 1), (dimensions[max_ind][0] - 10, dimensions[max_ind][1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# for (i, shape) in enumerate(shape[np.argmax(faces)]):
#     cv2.circle(image, (shape[np.argmax(faces)][0], y), 1, (0, 0, 255), -1)

for (x, y) in shape[np.argmax(faces)]:
    cv2.circle(image, (x, y), 1, (0, 0, 255), -1)


shape[np.argmax(faces)]

type(shape)
shape[1][:5]


faces
dimensions

np.argmax(faces)
max_ind

cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

shape

dimensions[max_ind][0]  # x
dimensions[max_ind][1]  # y
dimensions[max_ind][2]  # w
dimensions[max_ind][3]  # h
