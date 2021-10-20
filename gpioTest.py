import RPi.GPIO as GPIO
import time

gpioPin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while 1:
    print(str(GPIO.input(gpioPin)))
    time.sleep(0.5)