import RPi.GPIO as GPIO
import datetime as dt
import time

def GPIO_SET():
    pin_buzzer = 24
    pin_switch = 25

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(pin_buzzer,GPIO.OUT)
    GPIO.setup(pin_switch,GPIO.IN)


GPIO_SET()

alarm = dt.time(4,45,0,0)

while True:
	real=dt.datetime.now().time()
	real = dt.time(real.hour,real.minute,real.second,0)
	print(real)
	if(real==alarm):
		while True:
            GPIO.output(pin_buzzer,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin_buzzer,GPIO.LOW)
            time.sleep(0.5)
            if GPIO.input(pin_switch)==1:
                break
	time.sleep(1)
