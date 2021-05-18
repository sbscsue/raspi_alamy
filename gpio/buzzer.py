import RPi.GPIO as GPIO
import time

pin_buzzer = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_buzzer,GPIO.OUT)


while True:
	GPIO.output(pin_buzzer,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin_buzzer,GPIO.LOW)
	time.sleep(0.5)



