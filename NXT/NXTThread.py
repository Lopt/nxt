#coding: utf-8

from threading import Thread, Lock

class NXTThread():
    def __init__(self):
        self.thread = Thread(target = self.Run)
        self.exit = False

    def Start(self):
        self.thread.start()

    def Join(self):
        self.thread.join()

    def Halt(self, wait = True):
        self.exit = True
        if wait and self.thread.is_alive():
            self.Join()

    def HasStopped(self):
        return self.thread.is_alive()    
        
    def Run(self):
        pass
