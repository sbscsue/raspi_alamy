import RPi.GPIO as GPIO
import time

pin_buzzer = 20


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_buzzer,GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO.PWM(pin_buzzer,33)

pwm.start(1)
time.sleep(2)
GPIO.cleanup()

