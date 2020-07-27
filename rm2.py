import Pyro4
import os
import Pyro4.util
from collections import deque
import time
from threading import Thread
os.environ["PYRO_LOGFILE"] = "pyro.log"
os.environ["PYRO_LOGLEVEL"] = "DEBUG"
from database import database
import re
import random
import sys
@Pyro4.expose
class replica_manager(object):
    replicaTS=[0,0,0]
    log = deque()
    executedOps=[]
    valueTS=[0,0,0]
    tableTS=[[0,0,0],[0,0,0],[0,0,0]]
    def __init__(self):
        p=database()
        self.dictData=p.dictData        
    def updateRating(self,rating,name):
         regex= r'^{}.*$'.format(name)
         for key, value in self.dictData.items():
            if re.search(regex,key.lower(),re.IGNORECASE):
                value=((value+rating)/2)
                self.dictData[key]=value
                print("yesss")
                return self.dictData
            
         return "no"
    def getRating(self,name):
         regex= r'^{}.*$'.format(name)
         for key, value in self.dictData.items():
            if re.search(regex,key.lower(),re.IGNORECASE):
                return value
         return "no"
    def getUpdateInfo(self,tupleFE):
        try:
            #if the log and executed ops are empty
            if len(self.log)==0 and len(self.executedOps)==0:
                self.replicaTS[1]+=1
                ts=self.replicaTS.copy()
                self.log.append([1,ts,tupleFE])
                self.updateRating(tupleFE[0][0],tupleFE[0][1])
                self.mergeList(ts)
                self.executedOps.append(tupleFE[2])
            #check if it's already in the log or executed table
            elif self.checkExecuted(tupleFE[2])==True and self.checkLog(tupleFE[2])==True:
                self.replicaTS[1]+=1
                ts=self.replicaTS.copy()
                print(self.log)
                self.mergeList(ts)
                self.log.append([1,ts,tupleFE])
                self.tableTS[1]=self.replicaTS
                for i in self.log:
                    if self.checkValueTSWithLog(i[1],self.valueTS)==True and self.checkExecuted(i[2][2])==True:
                        self.updateRating(tupleFE[0][0],tupleFE[0][1])
                        self.valueTS=ts
                        self.executedOps.append(tupleFE[2])
                        self.tableTS[1]=self.replicaTS
            print(self.dictData)
            print(self.logTry)
        except:
            print("Pyro traceback:")
            print("".join(Pyro4.util.getPyroTraceback()))
        print(self.replicaTS)
        print(self.executedOps)
        return self.replicaTS
    def setTableTS(self,replicaTSGossip,rm):
        for i in range(0,3):
            if self.tableTS[rm][i]<=replicaTSGossip[i]:
                self.tableTS[rm][i]=replicaTSGossip[i]
    def gossip(self):
        rm1=Pyro4.Proxy("PYRONAME:rm1")
        rm3=Pyro4.Proxy("PYRONAME:rm3")
        rm1.receiveGossip(self.replicaTS,self.log)
        rm3.receiveGossip(self.replicaTS,self.log)
        print("sending")

    def analyseLog(self,gossipLog):
        for i in gossipLog:
            if self.checkGossipTSWithLog(i[1],self.replicaTS)==True:
                self.log.append(i)
                for y in self.log:
                    if self.log[y]==i:
                        self.log.remove(y)
        
    def receiveGossip(gossipTS,gossipLog):
        print("receive")
        self.analyseLog(gossipLog)
        self.mergeList(gossipTS)
        self.gossipUpdate()
        self.setTableTS(gossipTS,1)

    def gossipUpdate(self):
        for i in self.log:
            if self.checkValueTSWithLog(i[1],self.valueTS)==True and self.checkExecuted(i[2][2])==True:
                self.updateRating(tupleFE[0][0],tupleFE[0][1])
                self.valueTS=ts
                self.executedOps.append(tupleFE[2])
                self.tableTS[1]=self.replicaTS
    def checkGossipTSWithLog(self,ts,valueTS):
        for i in range(0,3):
            if ts[i]<=valueTS[i]:
                print("failed")
                return False
        print("success")
        return True
  
    def getDict(self):
        return self.dictData
    def findRating(self,name):
        for key, value in dictData.items():
            if key==name:
                return value
    def checkValueTSWithLog(self,ts,valueTS):
        for i in range(0,3):
            if valueTS[i]<ts[i]:
                print("failed")
                return False
        print("success")
        return True
    def checkLog(self,idNum):
        for i in self.log:
            if int(i[0])==int(idNum):
                return False
        return True
    def checkExecuted(self,idNum):
        print(self.executedOps)
        for i in self.executedOps:
            if int(i)==int(idNum):
                return False
        return True
    def mergeList(self,ts):
        for i in range(0,3):
            if self.valueTS[i]<=ts[i]:
                self.valueTS[i]=ts[i]
    def serverLoaded():
        print("Server overloaded, cannot more than two clients")
    
if __name__=='__main__':
    starttime=time.time()
    while True:
        t=replica_manager()
        daemon = Pyro4.Daemon()                
        ns = Pyro4.locateNS()                  
        uri = daemon.register(t)   
        ns.register("rm2", uri)
        try:
            t.gossip()
        except:
            print("Something wrong with other server")
        print("Ready.")
        sys.excepthook=Pyro4.util.excepthook
        Thread(target=daemon.requestLoop).start()
        print("tick")
        time.sleep(10 - ((time.time() - starttime) % 10.0))
