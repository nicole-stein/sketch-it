import cv2

img = cv2.imread("selfie2.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imshow("Original Image", gray_img)
cv2.waitKey(0)