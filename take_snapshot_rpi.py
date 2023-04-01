# import the necessary packages
import os

# Record image using Raspistill
name = "green_arrow_rpi.jpg"
os.system('raspistill -w 640 -h 480 -o ' + name)