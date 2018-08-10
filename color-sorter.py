#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for reading an EV3 color sensor connected to PORT_1 of the BrickPi3
# 
# Hardware: Connect an EV3 or NXT touch sensor to BrickPi3 Port 1.
# 
# Results:  When you run this program, you should see a 0 when the touch sensor is not pressed, and a 1 when the touch sensor is pressed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Define sensors.
COLOR_SENSOR    = BP.PORT_1 # Color sensor on BrickPi sensor
DISTANCE_SENSOR = BP.PORT_2 # Distance sensor on BrickPi sensor
WHEELS_MOTOR    = BP.PORT_A # Wheels motor on BrickPi motor
GATE_MOTOR      = BP.PORT_B # Gate motor on BrickPi motor
BELT_MOTOR      = BP.PORT_C # Belt motor on BrickPi motor

# Configure sensors.
BP.set_sensor_type(COLOR_SENSOR, BP.SENSOR_TYPE.EV3_COLOR_COLOR) # Configure for an EV3 color sensor.
#BP.set_sensor_type(DISTANCE_SENSOR, BP.SENSOR_TYPE.EV3_COLOR_COLOR) # Configure for an EV3 color sensor.

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

def none():
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    BP.set_motor_position(WHEELS_MOTOR, 0) # reset motor position
    print("No Color")
    return

def black():
    print("Black")
    return

def blue():
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    BP.set_motor_position(WHEELS_MOTOR, 0) # reset motor position
    print("Blue")

def green():
    print("Green")

def yellow():
    print("Yellow")
    BP.set_motor_power(BELT_MOTOR, 0)
    BP.set_motor_position(WHEELS_MOTOR, 250) # set motor target position
    #position = BP.get_motor_encoder(WHEELS_MOTOR)
    time.sleep(5)
    BP.set_motor_position(GATE_MOTOR, 90) # set motor target position
    time.sleep(0.5)
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    return

def red():
    print("Red")
    BP.set_motor_power(BELT_MOTOR, 0)
    BP.set_motor_position(WHEELS_MOTOR, 650) # set motor target position
    position = BP.get_motor_encoder(WHEELS_MOTOR)
    time.sleep(5)
    BP.set_motor_position(GATE_MOTOR, 90) # set motor target position
    time.sleep(0.5)
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    return

def white():
    print("White")
    return

def brown():
    print("Brown")
    return

def colorToMotion(argument):
    # print(color[argument]) # print the color
    switcher = {
        0: none,
        1: black,
        2: blue,
        3: green,
        4: yellow,
        5: red,
        6: white,
        7: brown
    }
    func = switcher.get(argument, lambda: "Invalid color") # Get the function from switcher dictionary
    func() # Execute the function
    
try:
    BP.offset_motor_encoder(WHEELS_MOTOR, BP.get_motor_encoder(WHEELS_MOTOR)) # reset encoder for WHEELS_MOTOR
    BP.offset_motor_encoder(GATE_MOTOR, BP.get_motor_encoder(GATE_MOTOR)) # reset encoder for WHEELS_MOTOR
    BP.set_motor_limits(WHEELS_MOTOR, 50, 200) # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    BP.set_motor_limits(GATE_MOTOR, 50, 200) # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    while True:
        # read and display the color sensor value
        try:
            BP.set_motor_power(BELT_MOTOR, 25)
            value = BP.get_sensor(COLOR_SENSOR)
            colorToMotion(value) # move color to it's position
        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.05)  # delay for 0.05 seconds (50ms) to reduce the Raspberry Pi CPU load.

except IOError as error:
            print(error)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

