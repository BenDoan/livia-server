import time
import json

#not thread safe

class loggeraccept():
    def __init__(self,name):
        self.usetime=False
        self.endtime=0.0
        self.numleft=0
        self.read(name)
    def addlogger(self):
        if self.isgood() :
            if self.numleft != -1 :
                self.numleft -= 1
            return True
        return False

    def isgood(self):
        return self.istimegood() and self.isnumgood()
    def istimegood(self):
        if self.usetime==False or time.time()<=self.endtime :
            return True
        return False
    def isnumgood(self):
        if self.numleft == -1 or self.numleft > 0 :
            return True
        return False
    def read(self,name):
        try :
            fp=open(name)
            dat=json.load(fp)
            self.usetime=dat["usetime"]
            self.endtime=dat["endtime"]
            self.numleft=dat["numleft"]
        except :
            self.write(name)
    def write(self,name):
        json.dump({"usetime":self.usetime,"endtime":self.endtime,"numleft":self.numleft},open(name,"w"))
