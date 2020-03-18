# USAGE
# python align_faces.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

# import the necessary packages
from imutils import paths
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
from PIL import Image
import os
import imutils
import dlib
import cv2
import shutil
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor and the face aligner
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
fa = FaceAligner(predictor, desiredFaceWidth=256)

imagePaths = list(paths.list_images(args["image"]))

cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)

for (i, imagePath) in enumerate(imagePaths):
    file = imagePath.split("/")[2]
    age = imagePath.split("/")[1]
    path = "aligned/" + age + "/" + file

    if os.path.exists(path):
        pass
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)))
        # load the input image, resize it, and convert it to grayscale
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        if len(faces) != 1:
            print("Invalid image, deleting...")
            os.remove(imagePath)

        # show the original input image and detect faces in the grayscale
        # image
        #cv2.imshow("Input", image)
        rects = detector(gray, 2)

        # loop over the face detections
        for rect in rects:
            # extract the ROI of the *original* face, then align the face
            # using facial landmarks
            (x, y, w, h) = rect_to_bb(rect)
            if x > 0 and y > 0 and w > 0 and h > 0:
                faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
                faceAligned = fa.align(image, gray, rect)
                import uuid
                f = str(uuid.uuid4())
                cv2.imwrite("aligned/" + age + "/" + file, faceAligned)
            else:
                if len(faces) != 1:
                    print("Already deleted")
                else:
                    print("Invalid image2, deleting...")
                    os.remove(imagePath)
                break
        # display the output images
        #cv2.imshow("Original", faceOrig)
        #cv2.imshow("Aligned", faceAligned)
        cv2.waitKey(0)
