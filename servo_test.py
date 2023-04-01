import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)

pwm = GPIO.PWM(36, 50)
pwm.start(5)

pwm.ChangeDutyCycle(3.3)
time.sleep(2)

pwm.ChangeDutyCycle(5.5)
time.sleep(2)

pwm.ChangeDutyCycle(7.5)
time.sleep(2)

pwm.ChangeDutyCycle(3.3)
time.sleep(2)

pwm.stop()
GPIO.cleanup()