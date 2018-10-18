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
# Code for WEDO : Adel - Juan - Fernando  SCC Interactive August 2018
# Tornado web server with Ivan SanPedro - PreSales Field September 2018
#
# Hardware: Connect an EV3 or NXT touch sensor to BrickPi3 Port 1.
# 
# Results:  When you run this program, you should see a 0 when the touch sensor is not pressed, and a 1 when the touch sensor is pressed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''
from tornado import web
from tornado import ioloop
from tornado import httpserver

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import tornado
import sys

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Define sensors.
COLOR_SENSOR    = BP.PORT_1 # Color sensor on BrickPi sensor
DISTANCE_SENSOR = BP.PORT_2 # Distance sensor on BrickPi sensor
WHEELS_MOTOR    = BP.PORT_A # Wheels motor on BrickPi motor
GATE_MOTOR      = BP.PORT_B # Gate motor on BrickPi motor
BELT_MOTOR      = BP.PORT_C # Belt motor on BrickPi motor

# Tornado HttpServer Port
HTTP_SERVER_PORT = 3004

# Configure sensors.
BP.set_sensor_type(COLOR_SENSOR, BP.SENSOR_TYPE.EV3_COLOR_COLOR) # Configure for an EV3 color sensor.
#BP.set_sensor_type(DISTANCE_SENSOR, BP.SENSOR_TYPE.EV3_COLOR_COLOR) # Configure for an EV3 color sensor.

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

def openGate():
    BP.set_motor_position(GATE_MOTOR, 90)
def closeGate():
    BP.set_motor_position(GATE_MOTOR, 0)
def resetMotors():
    BP.set_motor_power(BELT_MOTOR, 0)
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    BP.set_motor_position(WHEELS_MOTOR, 0) # reset motor position
def stopBelt():
    BP.set_motor_power(BELT_MOTOR, 0)
def startBelt():
    BP.set_motor_power(BELT_MOTOR, 50)
def expellPiece():
    openGate()
    BP.set_motor_power(BELT_MOTOR, 100)
    time.sleep(0.5)
    BP.set_motor_power(BELT_MOTOR, 0)
    closeGate()
    
def goTo(port,position):
    print("Im in goTo with port:", port) #fernando to remove
    print("And position:", position) #fernando to remove
    BP.set_motor_position(port, position) # set motor target position
    time.sleep(0.5)
    speed = BP.get_motor_status(port)[3]
    print("SPEED:", speed) #fernando to remove
    while speed!=0:
        # The following BP.get_motor_encoder function returns the encoder value
        try:
            speed = BP.get_motor_status(port)[3]
            print("Speed: %6d " % (speed))
        except IOError as error:
            print(error)
            
        time.sleep(0.5)  # delay 
        
def none():
    BP.set_motor_position(GATE_MOTOR, 0) # reset motor position
    BP.set_motor_position(WHEELS_MOTOR, 0) # reset motor position
    print("No Color")
    return

def black():
    BP.set_motor_power(BELT_MOTOR, 75)
    time.sleep(1)
    stopBelt()
    print("Black: Waiting for next color")
    return

def blue():
    stopBelt()
    time.sleep(0.5)
    goTo(WHEELS_MOTOR,100)
    openGate()
    time.sleep(0.5)
    closeGate()
    print("Blue")

def green():
    stopBelt()
    time.sleep(0.5)
    goTo(WHEELS_MOTOR,300)
    openGate()
    time.sleep(0.5)
    closeGate()
    print("Green")

def yellow():
    stopBelt()
    time.sleep(0.5)
    goTo(WHEELS_MOTOR,500)
    expellPiece()
    print("Yellow")
    return

def red():
    stopBelt()
    time.sleep(0.5)
    goTo(WHEELS_MOTOR,700)
    openGate()
    time.sleep(0.5)
    closeGate()
    print("Red")
    return

def white():
    print("White")
    return

def brown():
    print("Brown")
    return

def colorToMotion(argument):
    # print(color[argument]) # print the color
    print("Im in colorToMotion with argument", argument)
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

def initialize():
    BP.offset_motor_encoder(WHEELS_MOTOR, BP.get_motor_encoder(WHEELS_MOTOR)) # reset encoder for WHEELS_MOTOR
    BP.offset_motor_encoder(GATE_MOTOR, BP.get_motor_encoder(GATE_MOTOR)) # reset encoder for WHEELS_MOTOR
    BP.set_motor_limits(WHEELS_MOTOR, 50, 200) # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    BP.set_motor_limits(GATE_MOTOR, 50, 200) # optionally set a power limit (in percent) and a speed limit (in Degrees Per Second)
    sentinel=0
    #while sentinel<5:
    while True:
        # read and display the color sensor value
        try:
            print("sentinel: ", sentinel)
            startBelt()
            value = BP.get_sensor(COLOR_SENSOR)
            colorToMotion(value) # move color to it's position
            if value==1:
                sentinel=sentinel+1
            else:
                sentinel=0
        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.05)  # delay for 0.05 seconds (50ms) to reduce the Raspberry Pi CPU load.

def finalize():
    stopBelt()    

class StartMovement(tornado.web.RequestHandler):
    async def get(self):
        try:
            print("GET start_movement received!")
            self.set_header("Content-Type", "text/json")
            #result = roboarm.create_infinite_movement()
            result = "rest call--> starting!"
            self.write({"movement": result})
            print("[STARTMOVEMENT] Thread infinite movement launched!")
            self.flush()
            self.finish()
            initialize()
            return
        except:
            print("Start_movement error: " + str(sys.exc_info()))


class StopMovement(tornado.web.RequestHandler):
    def get(self):
        try:
            print("GET stop_movement received!")
            self.set_header("Content-Type", "text/json")
           # result = roboarm.shutdown_roboarm()
            result = "rest call--> stopping!"
            self.write({"movement": result})
            self.flush()
            self.finish()
            finalize()
            return
        except:
            print("Stop_movement error: " + str(sys.exc_info()))
            
class MyApplication(tornado.web.Application):
    def __init__(self):
        try:
            # variables init
            handlers = [(r"/move_start/", StartMovement),
                        (r"/move_stop/", StopMovement),
                        #(r"/initialize/", Initialize),
                        #(r"/get_temperature/", GetTemperature),
                        ]
            super(MyApplication, self).__init__(handlers)
            print("Web Server Initialize.")
        except:
            print("StartMovement Error" + str(sys.exc_info()))

try:
    server = tornado.httpserver.HTTPServer(MyApplication())
    server.bind(HTTP_SERVER_PORT)
    server.start(1)  # Forks multiple sub-processes
    ioloop.IOLoop.current().start()

except IOError as error:
            print(error)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

except:
    print("generic error...stopping tornado...")
    ioloop.IOLoop.current().stop()
    if str(sys.exc_info()[0]) != 'SystemExit':
        if sys.exc_info()[1] < 0:
            print("Exit Program: " + str(sys.exc_info()[1]))
            sys.exit(-1)
        else:
            sys.exit(0)
