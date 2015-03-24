# coding: utf-8

from Component import Component
import threading
import time

class Scanner(Component):

    name = "scanner"
    priority = 10

    @classmethod
    def IsImportant(self, sensor, value):
        return True
        
    def Initialize(self):
        pass

    def Halt(self):
        Component.Halt(self)
        self.robot.StopMotors()
            
    def Run(self):
            try:
                print "S1"
                self.robot.ElevateTo(0)
                if self.exit: return
                
                print "S1"
                self.robot.RotateTo(0)
                if self.exit: return

                print "S1"
                self.robot.ElevateTo(80)
                if self.exit: return

                print "S3"
                for n in range(100):
                    print "S4"
                    self.robot.RotateTo(n)
                    if self.exit: return
                    
            except Exception, error:
                print 'S Error', error
            self.robot.RotateTo(50)
            self.robot.ElevateTo(-5)
            self.robot.StopMotors()

