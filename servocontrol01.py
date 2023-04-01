# Objective: 
'''
• When executed, script must:
1. Slowly (user-define “slowly”)
cycle gripper from open to closed
and back again
2. Record an image with the RPi
camera at each gripper position
3. Print duty cycle onto each image
4. Stich images together to generate
time-lapse video
'''
# import the necessary packages
import os
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import imutils

# Function to take a snapshot from RPi
def TakeImgRPi(name):
    print("Taking a picture..")
    os.system('raspistill -w 640 -h 480 -o ' + name)
    time.sleep(0.5)
    image = cv2.imread(name)
    #cv2.imshow(name, image)
    #cv2.waitKey(1)
    return image

# Function to calculate instantaneous distance
def distance():
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

    return distance

# Function to calculate average distance (takes 2 seconds)
def AvgDistance(num_of_readings):

    average_dist = np.array([])
    distances = []

    for i in range(num_of_readings):
        inst_val = distance()
        #print("Distance: ", inst_val, "cm")
        distances.append(inst_val)
        time.sleep(0.5)
        
    avg_dist = round(np.average(distances),2)
    print("Average distance to the obstacle: ",avg_dist," cm")
    return avg_dist

# Function to rotate servo to the required position (takes 2 seconds)
def ServoControl(pos):
    if pos == "full_closed":
        duty_cycle = 3.3
        pwm.ChangeDutyCycle(duty_cycle)        
        time.sleep(2)
    elif pos == "partial_open":
        duty_cycle = 5.5
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(2)
    elif pos == "full_open":
        duty_cycle = 7.5
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(2)
    else:
        duty_cycle = 3.3
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(2)
    
    return duty_cycle
        
        
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

# Distance Measurement - Define pin allocations
GPIO.setmode(GPIO.BOARD)
trig = 16
echo = 18
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
# Servo Control - Define pin allocations
GPIO.setup(36, GPIO.OUT)

# Distance Measure - Initialize - Ensure output has no value
GPIO.output(trig, False)
time.sleep(0.01)

# Servo Control - Initialize PWM
pwm = GPIO.PWM(36, 50)
pwm.start(5)

######### Gripper to Full-closed Position ##########
# Move the gripper to Full- Closed position (2 sec)
print("Moving the gripper to Full-Closed position")
duty = ServoControl("full_closed")
# Take a snapshot of Gripper position from RPi Camera
# and save it to a jpg file (0.5 sec)
name_image = "Gripper_Full_Closed_Pos_init.jpg"
image = TakeImgRPi(name_image)
# Calculate the avg. distance of an object (4 samples - 2 seconds)
print("Calculating the distance to the obstacle...")
avg_distance = AvgDistance(4)
# Dispaly the average distance on the captured image and save (1 sec)
text = "Distance: " + str(avg_distance) + " cm"
WriteTextOnImg(name_image,text,"R")
text = "Duty Cycle: " + str(duty) + "%"
WriteTextOnImg(name_image,text,"L")
print("-------")

######### Gripper to Partially-Open Position ##########
# Move the gripper to Partially-Open position
print("Moving the gripper to Partially-Open position")
duty = ServoControl("partial_open")
# Take a snapshot of Gripper position from RPi Camera
# and save it to a jpg file
name_image = "Gripper_Partial_Open_Pos.jpg"
image = TakeImgRPi(name_image)
# Calculate the avg. distance of an object (4 samples - 2 seconds)
print("Calculating the distance to the obstacle...")
avg_distance = AvgDistance(4)
# Dispaly the average distance on the captured image and save
text = "Distance: " + str(avg_distance) + " cm"
WriteTextOnImg(name_image,text,"R")
text = "Duty Cycle: " + str(duty) + "%"
WriteTextOnImg(name_image,text,"L")
print("-------")

######### Gripper to Full-Open Position ##########
# Move the gripper to Full- Open position
print("Moving the gripper to Full- Open position")
duty = ServoControl("full_open")
# Take a snapshot of Gripper position from RPi Camera
# and save it to a jpg file
name_image = "Gripper_Full_Open_Pos.jpg"
image = TakeImgRPi(name_image)
# Calculate the avg. distance of an object (4 samples - 2 seconds)
print("Calculating the distance to the obstacle...")
avg_distance = AvgDistance(4)
# Dispaly the average distance on the captured image and save
text = "Distance: " + str(avg_distance) + " cm"
WriteTextOnImg(name_image,text,"R")
text = "Duty Cycle: " + str(duty) + "%"
WriteTextOnImg(name_image,text,"L")
print("-------")

######### Gripper to Full-closed Position ##########
# Move the gripper to Full- Closed position
print("Moving the gripper to Full- Closed position")
duty = ServoControl("full_closed")
# Take a snapshot of Gripper position from RPi Camera
# and save it to a jpg file
name_image = "Gripper_Full_Closed_Pos_final.jpg"
image = TakeImgRPi(name_image)
# Calculate the avg. distance of an object (4 samples - 2 seconds)
print("Calculating the distance to the obstacle...")
avg_distance = AvgDistance(4)
# Dispaly the average distance on the captured image and save
text = "Distance: " + str(avg_distance) + " cm"
WriteTextOnImg(name_image,text,"R")
text = "Duty Cycle: " + str(duty) + "%"
WriteTextOnImg(name_image,text,"L")
print("-------")
# Stope Servo
pwm.stop()
# Cleanup GPIO pins
GPIO.cleanup()