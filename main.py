import RPi.GPIO as GPIO
import datetime as dt
import time as timer
import argparse
import threading as th

from image_processing.proc1.compare_img.compare_img import proc_img
from image_processing.proc2.pose_detect.pose_estimation import pose_main
from image_processing.proc3.object_com.object_compare import object_main



def img_processing(number):
    number = int(number)
    cnt = 0
    print("start")
    if(number==1):
        proc_img()
    if(number==2):
        print("hello")
        pose_main("../pose_images")

    if(number==3):
        object_main()
    
  

def GPIO_SET():
    global pin_buzzer
    global pin_switch
    pin_buzzer = 24
    pin_switch = 25

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin_buzzer,GPIO.OUT)
    GPIO.setup(pin_switch,GPIO.IN)
    
def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number',required = True)
    parser.add_argument('--active',required = True)
    parser.add_argument('--time',required = True)
    args = parser.parse_args()
    return args
# @method
#   1 : image_label
#   2 : pose_detect
#   3 : object_compare


GPIO_SET()
args = Parser()



active = args.active
if(active=='on'):
    active = True
else:
    active = False
    quit()


time = args.time.split(":")
time = list(map(int,time))
alarm = dt.time(time[0],time[1],0,0)  


number = args.number

while active:
    real=dt.datetime.now().time()
    real = dt.time(real.hour,real.minute,real.second,0)
    print(real)
    if(real==alarm):
        thread = th.Thread(target=img_processing,args=(number))
        thread.start()
        
        while True:
            print("equal")
            GPIO.output(pin_buzzer,GPIO.HIGH)
            timer.sleep(0.5)
            GPIO.output(pin_buzzer,GPIO.LOW)
            timer.sleep(0.5)
            if(thread.is_alive()==False):
                GPIO.output(pin_buzzer,GPIO.LOW)
                print("alarm off")
                break
            
            
    timer.sleep(1)
