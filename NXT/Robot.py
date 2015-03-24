# coding: utf-8

import nxt.locator
from nxt.motor import Motor
from ColorSensor import ColorSensor
from Scanner import Scanner
from Collector import Collector
from Component import Component
from threading import Thread
from Queue import Queue

from time import sleep

GRIP_ANGLE = 80
GRIP_POWER = 50

ROTATE_ANGLE = 360 * 84
ROTATE_POWER = 127

ELEVATION_ANGLE = 360 * 24
ELEVATION_POWER = 127

ELEVATION_ANGLE_ROTATION = 360 * 24 / 2
ELEVATION_ANGLE_ROTATION_POWER = 11

class Robot:
    def __init__(self, brick):
        self.brick = brick
        self.queue = Queue()
        
        self.components = {}
        self.sensors = {}
        self.active = Component(self)
        
        self.InitializeHardware()
        self.InitializeComponents()
        self.InitializeSensors()

        self.active.Start()
        self.queue_thread = Thread(target=self.QueueWorker)
        self.queue_thread.start()

    def GetBrick(self):
        return self.brick

    def InitializeHardware(self):
        self.motor_grip = Motor(self.brick, nxt.PORT_C)
        self.rotation = 50
        self.motor_rotate = Motor(self.brick, nxt.PORT_B)
        self.elevation = 0
        self.motor_elevate  = Motor(self.brick, nxt.PORT_A)
        self.grip = False

    def InitializeSensors(self):
        self.sensors[ColorSensor.name] = ColorSensor(self, nxt.PORT_1)
    
    def InitializeComponents(self):
        self.components[Scanner.name] = Scanner
        self.components[Collector.name] = Collector

    def Connect(self):
        # if something bad happens here, see
        # http://code.google.com/p/nxt-python/wiki/Installation
        #self.brick.connect()

        for name in self.sensors:
            self.sensors[name].Start()

    def Interrupt(self, sensor, value):
        self.queue.put((sensor, value))

    def QueueWorker(self):
        while True:
            sensor, value = self.queue.get() 
            active_change = False
            for name in self.components:
                if (self.components[name].priority > self.active.priority):
                    if self.components[name].IsImportant(sensor, value):
                        self.active.Halt()
                        self.active = self.components[name](self)
                        active_change = True

            if active_change:
                self.active.Start()
        

            #if self.active.HasStopped():
            #    self.active = Scanner(self)
            #    self.active.Start()

            self.queue.task_done()

            
    def Grip(self):
        #if not self.grip:
            self.motor_grip.turn(GRIP_POWER, GRIP_ANGLE)            
            self.grip = True
        
    def Release(self):
        #if self.grip:
            self.motor_grip.turn(-GRIP_POWER, GRIP_ANGLE)            
            self.grip = False

    def StopMotors(self):
        self.motor_rotate.idle()
        self.motor_elevate.idle()
    
    def RotateTo(self, n):
        diff = self.rotation - n
        if (diff > 0):
            turnPercent = diff / 100.0 * ROTATE_ANGLE
            Thread(target=self.motor_elevate.turn, args=(-ELEVATION_ANGLE_ROTATION_POWER, diff / 100.0 * ELEVATION_ANGLE_ROTATION)).start()
            self.motor_rotate.turn(ROTATE_POWER, turnPercent)

        elif (diff < 0):
            turnPercent = -diff / 100.0 * ROTATE_ANGLE
            Thread(target=self.motor_elevate.turn, args=(ELEVATION_ANGLE_ROTATION_POWER, -diff / 100.0 * ELEVATION_ANGLE_ROTATION)).start()
            self.motor_rotate.turn(-ROTATE_POWER, turnPercent)
        self.rotation = n
    
    def Rotate(self, add):
        if (add + self.rotation > ROTATE_ANGLE or
            add + self.rotation < 0):
            div, mod = divmod(add + self.rotation, 100)
            self.RotateTo(abs(div))
    
    def ElevateTo(self, n): 
        diff = self.elevation - n
        if (diff > 0):
            self.motor_elevate.turn(ELEVATION_POWER, diff / 100.0 * ELEVATION_ANGLE)
        elif (diff < 0):
            self.motor_elevate.turn(-ELEVATION_POWER, -diff / 100.0 * ELEVATION_ANGLE)            
        self.elevation = n
        self.motor_elevate.idle()

    def Elevate(self, add):
        if add + self.rotation > ELEVATE_ANGLE:
            div, mod = divmod(add + self.elevation, 100)
            self.ElevateTo(ELEVATE_ANGLE)
        elif add + self.elevation < 0:
            self.ElevateTo(0)

    def GetSensor(self, name):
        return self.sensors[name]
    
def main():
    brick = nxt.locator.find_one_brick()
    robo = Robot(brick)
    #for brick in nxt.locator.find_bricks():
    #    robo = Robot(brick)        
    #    break

    robo.Connect()

main()

