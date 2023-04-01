# import the necessary packages
import os
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera

#Motor Driver Fins:
INA = 31
INB = 33
INC = 35
IND = 37

#Initialisation Function to set pins to low:
def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    GPIO.setup(INC, GPIO.OUT)
    GPIO.setup(IND, GPIO.OUT)

#Clean-up Fxn to set pins to low
def gameover():
    GPIO.output(INA, GPIO.LOW)
    GPIO.output(INB, GPIO.LOW)
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.LOW)

#Forward movement fxn:
def forward(tf):
    init()

    #Left Wheels: (wheels rotating forward)
    GPIO.output(INA, GPIO.HIGH)
    GPIO.output(INB, GPIO.LOW)

    #Right Wheels: (wheels rotating forward)
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.HIGH)

    time.sleep(tf) #wait x seconds

    gameover() #set all pins to low
    GPIO.cleanup() #pin state cleanup

#Backward movement fxn:
def reverse(tf):
    init()

    #Left Wheels: (wheels rotating backward)
    GPIO.output(INA, GPIO.LOW)
    GPIO.output(INB, GPIO.HIGH)

    #Right Wheels: (wheels rotating backward)
    GPIO.output(INC, GPIO.HIGH)
    GPIO.output(IND, GPIO.LOW)

    time.sleep(tf) #wait x seconds

    gameover() #set all pins to low
    GPIO.cleanup() #pin state cleanup
   
#Left movement fxn:
def pivotleft(tf):
    init()

    #Left Wheels: (wheels rotating backward)
    GPIO.output(INA, GPIO.HIGH)
    GPIO.output(INB, GPIO.LOW)

    #Right Wheels: (wheels rotating forward)
    GPIO.output(INC, GPIO.HIGH)
    GPIO.output(IND, GPIO.LOW)

    time.sleep(tf) #wait x seconds

    gameover() #set all pins to low
    GPIO.cleanup() #pin state cleanup

#Right movement fxn:
def pivotright(tf):
    init()

    #Left Wheels: (wheels rotating forward)
    GPIO.output(INA, GPIO.LOW)
    GPIO.output(INB, GPIO.HIGH)

    #Right Wheels: (wheels rotating backward)
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.HIGH)

    time.sleep(tf) #wait x seconds

    gameover() #set all pins to low
    GPIO.cleanup() #pin state cleanup

# def acce_dece(x):
def key_input(event):
    init()
    print("Key: ", event)
    tf = 1
    
    if key_press.lower() == 'w':
        forward(tf)
        text = "moving forward"
        
    elif key_press.lower() == 'z':
        reverse(tf)
        text = "moving back"
        
    elif key_press.lower() == 'a':
        pivotleft(tf)
        text = "taking left"
        
    elif key_press.lower() == 's':
        pivotright(tf)
        text = "taking right"
        
    elif key_press.lower() == 'e':
        GripperPickOp()
        text = "picking-up"
        
    elif key_press.lower() == 'r':
        GripperRelOp()
        text = "releasing"
    
    elif key_press.lower() == 'x':
        duty = ServoControl("full_closed")
        text = "closing FULL"
        
    else:
        print("Invalid key pressed!!")
        text = "Invalid key pressed"
    
    return text

# Function to calculate instantaneous distance
def distance():
    # Distance Measurement - Define pin allocations
    GPIO.setmode(GPIO.BOARD)
    trig = 16
    echo = 18
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    
    # Distance Measure - Initialize - Ensure output has no value
    GPIO.output(trig, False)
    time.sleep(0.01)
    
    # Generate trigger pulse
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # Generate echo time signal
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start

    # Convert time to distance
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    GPIO.cleanup()
    return distance

# Function to rotate servo to the required position (takes 2 seconds)
def ServoControl(pos):
    GPIO.setmode(GPIO.BOARD)
    # Servo Control - Define pin allocations
    GPIO.setup(36, GPIO.OUT)

    # Servo Control - Initialize PWM
    pwm = GPIO.PWM(36, 50)
    pwm.start(5)
    if pos == "full_closed":
        duty_cycle = 3.3
        pwm.ChangeDutyCycle(duty_cycle)        
        time.sleep(1)
    elif pos == "partial_open":
        duty_cycle = 5.5
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
    elif pos == "full_open":
        duty_cycle = 7.5
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
    else:
        duty_cycle = 3.3
        pwm.ChangeDutyCycle(duty_cycle)
        print("Maintaining closed position for Gripper. Invalid Key Pressed")
        time.sleep(1)
    # Stope Servo
    pwm.stop()
    GPIO.cleanup()
    return duty_cycle

# Function to Pick Object Up (takes 5 seconds)
def GripperPickOp():
    GPIO.setmode(GPIO.BOARD)
    # Servo Control - Define pin allocations
    GPIO.setup(36, GPIO.OUT)

    # Servo Control - Initialize PWM
    pwm = GPIO.PWM(36, 50)
    pwm.start(5)
    # fully open
    duty_cycle = 7.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    # partially close
    duty_cycle = 5.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    # grab
    duty_cycle = 4.0
    pwm.ChangeDutyCycle(duty_cycle)
    print("Object Picked!")
    time.sleep(1)
    # Stope Servo
    pwm.stop()
    GPIO.cleanup()

# Function to Release Object Down (takes 2 seconds)
def GripperRelOp():
    GPIO.setmode(GPIO.BOARD)
    # Servo Control - Define pin allocations
    GPIO.setup(36, GPIO.OUT)

    # Servo Control - Initialize PWM
    pwm = GPIO.PWM(36, 50)
    pwm.start(5)
    # partially open
    duty_cycle = 5.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    # fully open
    duty_cycle = 7.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    # Stope Servo
    pwm.stop()
    GPIO.cleanup()

# Function to take a snapshot from RPi
def TakeImgRPi(name):
    print("Taking a picture..")
    os.system('raspistill -w 640 -h 480 -o ' + name)
    time.sleep(0.2)
    image = cv2.imread(name)
    #cv2.imshow(name, image)
    #cv2.waitKey(1)
    return image

# Read Image, add text, save, and display for 1 second
def WriteTextOnImg(img, text, pos):
    gImage = cv2.imread(img)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    clr = (0, 255, 0)
    if pos == "L":
        orig = (20, 20)
    else:
        orig = (405, 20)
    cv2.putText(gImage, text, orig, font, 1, clr, 1)
    cv2.imwrite(img, gImage)
    #cv2.imshow(img, image)
    #cv2.waitKey(1) 
###### End of Function definitions #############

#------- Main Function ------------#
print("Ensure the Power Switch is ON ...")
time.sleep(5)
img_num = 1

# Take a snapshot of Gripper position from RPi Camera and save it to a jpg file (0.5 sec)
name_image = "drive01_" + str(img_num) + ".jpg"
image = TakeImgRPi(name_image)
img_num += 1
# Dispaly the average distance on the captured image and save (1 sec)
text = "Initial Image"
WriteTextOnImg(name_image,text,"L")

# init()
while True:
    time.sleep(1)
    # Calculate the distance of an object
    print("Distance to obstacle: ", distance(), " cm")
    
    key_press = input("Select operating mode or 'p' to exit: \n'w' - foward \n'z' - reverse \n's' - pivot left \n'a' - pivot right\n'e' - pick up\n'r' - release\n'x' - full-closed\n")
    
    if key_press == 'p':
        break  

    text = key_input(key_press)
    
    # Take a snapshot of Gripper position from RPi Camera and save it to a jpg file (0.5 sec)
    name_image = "drive01_" + str(img_num) + ".jpg"
    image = TakeImgRPi(name_image)
    # Dispaly the average distance on the captured image and save (1 sec)    
    WriteTextOnImg(name_image,text,"L")
    img_num += 1



