import RPi.GPIO as GPIO
import time

pin_switch = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_switch,GPIO.IN)


while True:
	if GPIO.input(pin_switch)==0:
		print("0")
		time.sleep(1)
	else:
		print("1")
		time.sleep(1)
