from PIL import ImageGrab
import numpy as np
import cv2
from PIL import Image as im
import time

def captureScreen(bbox=(300,300,690+300,530+300)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

img_arr=captureScreen()
imgfile = im.fromarray(img_arr)
imgfile=imgfile.save('dummy'+'.jpg')


# show_img = cv2.imread('uploads/129129_faces.jpg')
# cv2.imshow('show_img', show_img)
# time.sleep(3)