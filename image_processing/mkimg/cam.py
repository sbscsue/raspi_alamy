import picamera
import time
import argparse
from PIL import Image
import cv2 as cv

#from main import new_img
new_img = '/tmp/sample_img.jpg'

def cap_img(_image):
    camera = picamera.PiCamera(resolution=(640, 480), framerate=30)

    #preview = camera.start_preview()
    #preview.fullscreen = False
    #preview.window = (0, 0, 400, 400)
    camera.start_preview()


    img = Image.open(_image)
    pad = Image.new('RGB', (
        ((img.size[0]+31)//32)*32,
        ((img.size[1]+15)//16)*16,
        ))
    pad.paste(img, (0,0))
    over = camera.add_overlay(pad.tobytes(), size=img.size)
    over.alpha = 128
    over.layer = 3

    while True :
        ret = input()
        if(ret == 'c') :
            print(camera.capture(new_img))
            break;
        #print(ret)
        #print("key : " + str(ret))
        #if ret == ord('c') :
        #    camera.capture('image.jpg')
        #    break;


    #time.sleep(5)
    camera.stop_preview()
    camera.remove_overlay(over)

