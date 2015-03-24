#coding: utf-8

from time import sleep
from threading import Thread, Lock

import nxt.locator
from nxt.motor import Motor

GRIP_ANGLE = 10
ROTATE_ANGLE = 359
ELEVATION_ANGLE = 100

class NXTThread():
    def __init__(self):
        self.thread = Thread(target = self.Run)
        self.exit = False

    def Start(self):
        self.thread.start()

    def Join(self):
        self.thread.join()

    def Halt(self, wait = True):
        self.exit = False
        if wait and self.thred.is_alive():
            self.Join()

    def Run(self):
        pass

class Sensor(NXTThread):
    def __init__(self, robot, port, scan_time = 0.1):
        NXTThread.__init__(self)

        self.robot = robot
        self.scan_time = scan_time
        self.port = port
        self.value = None

        self.Initialize()
    
    def Run(self):
        while not self.exit:
            sleep(self.scan_time)
            result = self.Scan()
            if result != self.value:
                self.value = result
                self.robot.NewValue(self.name, self.value)
                

    def GetValue(self):
        return self.value
    
    def AddEvent(self, obj):
        self.events.append(obj)

    def Initialize(self):
        pass

    def GetName(self):
        return None

    def Scan(self):
        pass


class ColorSensor(Sensor):
    def Initialize(self):
        pass
        #self.sensor = nxt.Color20(self.robot.GetBrick(), self.port)

    def Scan(self):
        #return self.sensor.get_sample()
        return 1
        
class Component(NXTThread):

    name = ''
    
    def __init__(self, robot):
        NXTThread.__init__(self)

        self.robot  = robot
        self.priority = 0
        self.Initialize()
        

    def IsImportant(sensor, value):
        return False
        
    def Initialize(self):
        pass
            
    def Run(self):
        pass

class Scanner(Component):

    name = "scanner"
    
    def IsImportant(sensor, value):
        return True
        
    def Initialize(self):
        priority = 0
            
    def Run(self):
        self.robot.TurnTo(0)
        self.robot.ElevavateTo(10)
        for n in range(359):
            self.robot.TurnTo(n)

            if self.exit:
                return

class Collector(Component):
    
    name = 'collector'
    
    def IsImportant(sensor, value):
        if sensor == 'color':
            return True
        
    def Initialize(self):
        priority = 50
     
    def Run(self):
        self.robot.Grip()
        self.robot.TurnTo(0)
        self.robot.Release()
    

class Robot:
    def __init__(self, brick):
        self.brick = brick
        #self.motor_grip = Motor(self.brick, nxt.PORT_A)
        #self.motor_rotate = Motor(self.brick, nxt.PORT_B)
        #self.motor_elevate  = Motor(self.brick, nxt.PORT_C)
        self.components = {}
        self.active = Component(self) 
        self.InitializeComponents()
        self.InitializeSensors()

    def GetBrick(self):
        return self.brick

    def InitializeSensors(self):
        self.color_sensor = ColorSensor(self.brick, nxt.PORT_1)
    
    def InitializeComponents(self):
        self.components[Scanner.name] = Scanner(self)
            
    def Connect(self):
        # if something bad happens here, see
        # http://code.google.com/p/nxt-python/wiki/Installation
        #self.brick.connect()

        self.color_sensor.Start()

    def NewValue(sensor, value):
        active_change = False
        for component in self.components:
            if (component.priority >= self.active.priority):
                if component.IsImportant(sensor, value):
                    self.active.Halt()
                    self.active = component
                    active_change = True

        if active_change:
            self.active.Start()


    def Grip(self):
        if not self.grip:
            self.motor_grip.turn(100, GRIP_ANGLE)            
            self.grip = True
        
    def Release(self):
        if self.grip:
            self.motor_grip.turn(100, -GRIP_ANGLE)            
            self.grip = False
        
    def RotateTo(self, n):
        diff = self.rotation - n
        self.motor_rotate.turn(10, diff)
    
    def Rotate(self, add):
        if (add + self.rotation > ROTATION_ANGLE or
            add + self.rotation < 0):
            div, mod = divmod(add + self.rotation, ROTATION_ANGLE)
            self.RotateTo(abs(div))
    
    def ElevateTo(self, n):
        diff = self.rotation - n
        self.motor_elevate.turn(10, diff)

    def Elevate(self, add):
        if add + self.rotation > ELEVATE_ANGLE:
            div, mod = divmod(add + self.rotation, ELEVATE_ANGLE)
            self.ElevateTo(ELEVATE_ANGLE)
        elif add + self.rotation < 0:
            self.ElevateTo(0)
            
    
def main():
    for brick in nxt.locator.find_bricks():
        robo = Robot(brick)        
        break

    #robo.Connect()

#main()
Robot("Test").Connect()
