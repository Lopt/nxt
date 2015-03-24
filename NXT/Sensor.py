# coding: utf-8

from NXTThread import NXTThread
from time import sleep

class Sensor(NXTThread):
    name = None
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
                self.robot.Interrupt(self.name, self.value)
                

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
