import sys
import RPi.GPIO as GPIO

sys.path.append('/home/pi/raspi_alamy/image_processing/proc1')
from mkimg.cam import cap_img
from cppixel.img_hist import cap_pix
from labeling.label_img import main_labeling

import argparse

label=''
new_img='/tmp/sample_img.jpg'
#std_img = "/home/pi/Documents/raspi_alamy/web/weblamy/public/alarm1/img.jpg"
std_img = "/home/pi/raspi_alamy/image_processing/proc1/etc/co1.jpg"

def proc_img():
    label = main_labeling(std_img)
    label_str = ''
    ret = 0.0
    

    while(ret<0.5) :
        if(label_str.find(label) == -1) :
            cap_img(std_img)
            label_str = main_labeling(new_img)
            print("label_str : " + label_str)

        ret = cap_pix(new_img)
        
    
    print("include : " + str(label_str.find(label)))


if __name__=='__main__':
    proc_img()


