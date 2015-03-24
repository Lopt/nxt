# coding: utf-8

from Component import Component
from time import sleep

class Collector(Component):
    
    name = 'collector'
    priority = 50

    @classmethod
    def IsImportant(self, sensor, value):
        if sensor == 'color' and value != 1:
            return True
        return False
        
    def Initialize(self):
        pass
    
    def Run(self):
        print "Sammler läuft"
        try:
            print 'C1'
            try:
                self.robot.Grip()
            except Exception, error:
                print 'C1', error
            
            sleep(1)
            print 'C2'
            self.robot.ElevateTo(0)
            sleep(1)
            
            print 'C3'
            if self.robot.GetSensor('color').Scan() == 5:
                self.robot.RotateTo(100)
            else:
                self.robot.RotateTo(0)
                
            sleep(1)
        except Exception, error:
            print 'C', error
        
        finally:
            print 'C4'
            self.robot.Release()
            sleep(1)

        print 'C5'
        sleep(2)
        self.robot.ElevateTo(-5)
        self.robot.RotateTo(50)
        self.robot.StopMotors()
