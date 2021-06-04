import numpy as np
import cv2
import matplotlib.pyplot as plt

def canny_img(_image):
    #img = cv2.imread('/home/pi/Documents/ex_project/ex/image_processing/etc/co2.jpg')
    img = cv2.imread(_image)
    img2 = cv2.Canny(img, 50, 100)

    cv2.imshow('original', img)
    cv2.imshow('Canny img', img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    canny_img()
