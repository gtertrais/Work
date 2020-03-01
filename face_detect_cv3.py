import cv2
import sys
import glob
from PIL import Image
import os


images=glob.glob("images/" + "**/*.jpg", recursive=True)

  # Get user supplied values
cascPath = "haarcascade_frontalface_default.xml"

  # Create the haar cascade
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)

for image in images:
  # Read the image
	read = cv2.imread(image)
	gray = cv2.cvtColor(read, cv2.COLOR_BGR2GRAY)

  # Detect faces in the image
	faces = faceCascade.detectMultiScale(
    	gray,
    	scaleFactor=1.1,
    	minNeighbors=5,
    	minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
	)
	
	print(image)
	print("Found {0} faces!".format(len(faces)))
	if len(faces) != 1:
		print("deleting image")
		os.remove(image)


# Draw a rectangle around the faces

 # cv2.imshow("Faces found", image)
# cv2.waitKey(0)