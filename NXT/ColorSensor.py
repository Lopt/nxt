# coding: utf-8

from Sensor import Sensor
import nxt

class ColorSensor(Sensor):
    name = 'color'
    def Initialize(self):
        #self.sensor = nxt.Light(self.robot.GetBrick(), self.port)
        #self.sensor.set_illuminated(0)
        self.sensor = nxt.Color20(self.robot.GetBrick(), self.port)

    def Scan(self):
        return self.sensor.get_sample()
        
