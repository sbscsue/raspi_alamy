import picamera
import time
import argparse
from PIL import Image
import cv2 as cv
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/raspi_alamy')
from main import key

new_img = '/tmp/sample_img.jpg'
pin_button=''

def GPIO_SET():
    global pin_button
    pin_button=25
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_button, GPIO.IN)

def ret_button():
    return GPIO.input(pin_button)

def cap_img(_image):
    GPIO_SET()
    camera = picamera.PiCamera(resolution=(640, 480), framerate=30)
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
        global key
        if(key=='c'):
            print(camera.capture(new_img))
            break;

    camera.stop_preview()
    camera.remove_overlay(over)

