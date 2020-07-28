import Pyro4
import random
import sys
import Pyro4.util
from collections import deque

#from rm3 import replica_manager
@Pyro4.expose
class front_end(object):
    updateId=0
    clientCounter=[0,0,0]
    vectorTS=[0,0,0]
    listRM=["PYRONAME:rm1","PYRONAME:rm2","PYRONAME:rm3"]
    def __init__(self,daemon):
        self.daemon=daemon
        self.counter=0
        self.rm=None
    def sendRating(self,rating,name,rm):
        return rm.updateRating(rating,name)
    def queryRating(self,name,rm):
        return rm.getRating(name)
    def callMe(self):
        return ("Connected")
    def returnRM(self):
        return self.rm
    def getStatus(self,rm):
        print(rm.getStatus())
        return rm.getStatus()        
    def connectRM(self):
        trying=0
        notConnected=True
        maxConnection=0
        print(self.clientCounter)
        while notConnected:
            try:
                listNum=[0,1,2]
                trying=random.choice(listNum)
                maxConnection+=1
                t=Pyro4.Proxy(self.listRM[trying])
                counter=trying
                print("server number:"+str(trying))
                trying+=1
                t._pyroBind()
                if self.clientCounter[counter]>1:
                    print("Server is overloaded")
                    t.serverLoaded()
                    t._pyroRelease()
                    t._pyroBind()
                else:
                    self.clientCounter[counter]+=1
                    self.rm=t
                    notConnected=False
            except Exception:
                if maxConnection>7:
                    self.rm=None
                    notConnected=False
                    return Exception
                print("Finding next RMI...")
                continue
        return self.rm
    def sendUpdate(self,rating,name,rm):
        self.updateId+=1
        prevId=self.vectorTS
        ts=rm.getUpdateInfo(([rating,name],prevId,self.updateId))
        self.vectorTS=ts
        print(self.vectorTS)
        return self.vectorTS
    def disconnect(self,rm):
       for i in range(0,3):
           if rm.rmName()==self.listRM[i]:
               self.clientCounter[i]-=1
    def mergeList(self,ts):
        for i in range(0,3):
            if self.vectorTS[i]<=ts[i]:
                self.vectorTS[i]=ts[i]
    @Pyro4.oneway 
    def shutdown(self):
        print("shutting down...")
        self.daemon.shutdown()
if __name__=='__main__':
    Pyro4.config.COMMTIMEOUT = 3
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()                 
    uri = daemon.register(front_end(daemon))  
    ns.register("fe", uri)
    sys.excepthook=Pyro4.util.excepthook
    daemon.requestLoop()


