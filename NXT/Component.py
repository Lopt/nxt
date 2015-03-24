from NXTThread import NXTThread

class Component(NXTThread):

    name = ''
    priority = 0
        
    def __init__(self, robot):
        NXTThread.__init__(self)

        self.robot  = robot
        self.Initialize()
        

    def IsImportant(self, sensor, value):
        return False
        
    def Initialize(self):
        pass
            
    def Run(self):
        pass 
