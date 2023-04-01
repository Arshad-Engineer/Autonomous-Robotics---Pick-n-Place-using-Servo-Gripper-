import math
motor_rot_per_wheelrot = int(input("Enter gear ratio (enter only denominator, e.g. If 1:120, enter 120): "))
encoder_ticks_per_motor_rev = int(input("Enter encoder ticks per motor revolution: "))
gear_ratio = 1/motor_rot_per_wheelrot
distance_to_travel = float(input("Enter distance to travel (mm): "))
wheel_diameter = int(input("Enter wheel diameter (mm): "))
# wheel rotations for 1 m
wheel_rot_required = (distance_to_travel) / (math.pi * wheel_diameter)
print("Wheel rotations required for given travel distance: ", round(wheel_rot_required,2))
mot_rot_required = wheel_rot_required * motor_rot_per_wheelrot
print("Motor rotations required for given travel distance: ", round(mot_rot_required,2))
encoder_ticks_required = mot_rot_required * encoder_ticks_per_motor_rev
print("Encoder ticks for each motor for given travel distance: ", round(encoder_ticks_required,2))
encoder_ticks_required_RPi = encoder_ticks_required * 2 # For 2 encoders
print("Encoder ticks registered by RPi for given travel distance: ", round(encoder_ticks_required_RPi,2))