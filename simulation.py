
'''class iotDevice():
    def __init__(self, devId = 0):
        self.id = devId
        self.retransmit = False
        self.arrTime = 0
        
class simulation():
    def __init__(self, mstrClk = 0, simQ = [], servBusy = False, noOfDev = 1000):
        self.mstrClk = mstrClk
        self.simQ = simQ
        self.servBusy = servBusy
        self.noOfDev = noOfDev
        self.iotDevices = []
        self.devArrTimes = []
        
    def runSimulation(self):
        for i in range(1, self.noOfDev):
            self.iotDevices.append(iotDevice(i))
            self.devArrTimes[i] = self.iotDevices[i].arrTime
            
        self.masterClock = 0'''
import sys

def runSim():
    newArrival = 2
    servCompl = sys.maxint
    orbittingEvtLst = []
    minObtEvt = sys.maxint
    
    QLen = 0
    mstrClk = 0
    interArrTime = 6
    srvcTime = 10
    bufferSize = 2
    retransmissionDelay = 5
    iotDevReCertified = 0
    nIotDev = 1000
    
    while iotDevReCertified < nIotDev:
        #if iotDevReCertified % 50 == 0:
            #print iotDevReCertified
        #print mstrClk, newArrival, servCompl, QLen, orbittingEvtLst
        if orbittingEvtLst:
            minObtEvt = min(orbittingEvtLst)
        else:
            minObtEvt = sys.maxint
            
        if servCompl < newArrival and servCompl < minObtEvt:
            #print 'handle service completion'
            mstrClk = servCompl 
            servCompl = mstrClk +  srvcTime
            iotDevReCertified += 1
            QLen -= 1
            
        elif newArrival <= servCompl and minObtEvt > newArrival:
            #print 'handle new arrival'
            mstrClk = newArrival
            if QLen < bufferSize:
                if QLen == 0:
                    servCompl = mstrClk + srvcTime
                newArrival += interArrTime
                QLen += 1
                
                                   
            else:
                orbittingEvtLst.append(newArrival + retransmissionDelay)
                newArrival += interArrTime
            
        elif minObtEvt <= servCompl and minObtEvt <= newArrival:
            #print 'handle retransmitted arrival'
            mstrClk = minObtEvt
            if QLen < bufferSize:
                if QLen == 0:
                    servCompl = mstrClk + srvcTime
                orbittingEvtLst.remove(min(orbittingEvtLst))
                QLen += 1
                
            else:
                orbittingEvtLst.remove(min(orbittingEvtLst))
                orbittingEvtLst.append(minObtEvt + retransmissionDelay)
                
        else:
            print 'logic error'
            sys.exit()
    
    print 'all devices re-certified'        
        
runSim()  
        
        
        
        
        
        
        
        
        
        
        
        