import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from PIL import Image
import requests
from io import BytesIO


def borderImage(scale, image):
	top, bottom, left, right = [scale]*4
	return  cv2.copyMakeBorder(image, top, bottom, left, right, borderType = cv2.BORDER_REPLICATE)

#read in the files
url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
if url == "":
	url = input("Enter URL: ")
response = requests.get(url)
imag = Image.open(BytesIO(response.content))
img = np.float32(imag)
try:
	gray = cv2.cvtColor(np.array(imag), cv2.COLOR_RGB2GRAY)
except:
	gray = np.array(imag)

print("▶▶▶▶▶▶▶▶▶▶▶▶Image Preprocessing")

blur = input("▶▶▶▶▶Would you like to blur the image? Yes/No:")
if blur == "Yes" or blur == "yes" or blur == "y" or blur == "Y":
	#gray = cv2.blur(img,(5,5))
	gray = cv2.bilateralFilter(gray,9,200,200)

#edge detection using canny algorithm
canny = input("▶▶▶▶▶Would you like to apply the Canny Edge Detector to find circles from the image? Yes/No:")
if canny == "Yes" or canny == "yes" or canny == "y" or canny == "Y":
	#img = cv2.Canny(img, 20, 300)
	gray = cv2.Canny(gray, 20, 120)

#add borders to images
borders = input("▶▶▶▶▶Would you like to add borders to the image? This is useful for finding circles when your image is very crowded Yes/No:")
if borders == "Yes" or borders == "yes" or borders == "y" or borders == "Y":
	gray = borderImage(10, gray)
	#img = borderImage(10, img)

#find hough circles
#circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.3, 100)
#print(circles)

#find contours
contour = input("▶▶▶▶▶Would you like to find and draw the contours onto the image? Yes/No:")
if contour == "Yes" or contour == "yes" or contour == "y" or contour == "Y":
	contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#print(contours)
	cv2.drawContours(gray, contours, -1, (255, 255, 255), 3)
	cv2.imshow("Contours", gray)
	cv2.waitKey(0)
	cv2.destroyAllWindows

#find hough circles
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.28, 100)

#draw on the circles if there are any
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(img, (x, y), r, (255,255,0), 4)
		cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0,255,0), -1)
 
	# show the output image
	cv2.imshow("Hough Circles", img)
	#cv2.imshow("output", np.hstack([img, gray]))
	cv2.waitKey(0)
else:
	print("No circles were found!")
	cv2.imshow("No circles", img)
	cv2.waitKey(0)
