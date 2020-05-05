# import the necessary packages
import numpy as np
import cv2

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)

	# find the contours in the edged image and keep the largest one
	(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	c = max(cnts, key = cv2.contourArea)

	# compute the bounding box of the region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object
KNOWN_DISTANCE = 3

# initialize the known object width, which in this case, the piece of
# paper is 0.45 meters wide
KNOWN_WIDTH = 0.45

# initialize the list of images that we'll be using
IMAGE_PATHS = ["Test1.jpeg", "Test2.jpeg", "Test3.jpeg"]

# load the furst image that contains an object from our camera,
#then find the paper marker in the image, and initialize the focal length
image = cv2.imread(IMAGE_PATHS[0])
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
# loop over the images
for imagePath in IMAGE_PATHS:
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	image = cv2.imread(imagePath)
	marker = find_marker(image)
	meters = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
	cv2.putText(image, "%.2f meters" % (meters / 5.5),
		(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 255, 0), 3)
	cv2.imshow("image", image)
	cv2.waitKey(0)
