import sys
import time 


class IoTDev:
    def __init__(self, firstArrTim = sys.maxint, orbitFirstStartTim = sys.maxint,\
                orbitEndTim = sys.maxint, arrTimAfterOrbit = sys.maxint, \
                compltTim = sys.maxint, recertified = False):
        
        self.firstArrTim = firstArrTim
        self.orbitFirstStartTim = orbitFirstStartTim
        self.arrTimAfterOrbit = orbitEndTim
        self.orbitEndTim = orbitEndTim
        self.compltTim = compltTim
        self.recertified = False
        
def insertSortedOrbtList(orbitList, dev):
    for index in range(len(orbitList)):
        if orbitList[index].arrTimAfterOrbit > dev.arrTimAfterOrbit:
            orbitList.insert(index, dev)
            return
    orbitList.append(dev)
            
        
DEBUG = True
def runIoTSim():
    global DEBUG
    
    infiniteDev = IoTDev()
    
    nDevToRecert = 1000
    
    interArrTim = 6
    servTim = 10
    buffLenLimit = 2
    retransTim = 5
    
    mstrClk = 0
    waitBuf = []
    orbtEvtLst = []
    IoTDevLst = []
    nDevRecert = 0
    servCompl = sys.maxint
    
    '''First device'''
    dev = IoTDev(2)
    IoTDevLst.append(dev)
    
    for _ in xrange(1, nDevToRecert):
        dev = IoTDev()
        IoTDevLst.append(dev)
    
    newArr = IoTDevLst[0]
    
    startTime = time.time()
    if DEBUG:
        print '\nMC\tCLA\tCLS\t#Queue\tCLR\n'
    
    devArrived = 0
    currServDev = None
    
    while nDevRecert < nDevToRecert:
        if DEBUG:
            if servCompl == sys.maxint:
                print str(mstrClk) + '\t' + str(newArr.firstArrTim) + '\t' + '-' + '\t' + str(len(waitBuf)) \
                    + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst])
            else:
                print str(mstrClk) + '\t' + str(newArr.firstArrTim) + '\t' + str(servCompl) + '\t' + str(len(waitBuf)) \
                    + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst])
        
        if orbtEvtLst:
            '''Get the minimum since orbtEvtLst is sorted list'''
            minObtEvt = orbtEvtLst[0]
        else:
            minObtEvt = None
        
        
        if minObtEvt != None: 
            servComplLessMinOrb = servCompl < minObtEvt.arrTimAfterOrbit
            newArrLessMinOrb = minObtEvt.arrTimAfterOrbit > newArr.firstArrTim
            minOrbitDeal = minObtEvt.arrTimAfterOrbit <= servCompl and minObtEvt.arrTimAfterOrbit <= newArr.firstArrTim
        else:
            servComplLessMinOrb = True
            newArrLessMinOrb = True
            minOrbitDeal = False
        
        if servCompl < newArr.firstArrTim and servComplLessMinOrb:
                              
                currServDev.compltTim = servCompl
                if currServDev.recertified == True:
                    print 'error 1'
                    sys.exit()
                else:
                    currServDev.recertified = True
                
                mstrClk = servCompl
                servCompl = mstrClk + servTim
                
                nDevRecert += 1
                waitBuf.pop(0)
                
                if waitBuf:
                    currServDev = waitBuf[0]
                
        elif newArr.firstArrTim <= servCompl and newArrLessMinOrb:
            mstrClk = newArr.firstArrTim
            '''If buffer is not full'''
            if len(waitBuf) < buffLenLimit:
                if len(waitBuf) == 0:
                    servCompl = mstrClk + servTim
                    currServDev = newArr
                
                waitBuf.append(newArr)
                
            else:
                if newArr.orbitFirstStartTim == sys.maxint:
                    newArr.orbitFirstStartTim = mstrClk + retransTim
                    newArr.arrTimAfterOrbit = newArr.orbitFirstStartTim
                else:
                    print 'logic error 3'
                    sys.exit()
                
                insertSortedOrbtList(orbtEvtLst, newArr)
                
            '''Create new device'''
                
            devArrived += 1
            if devArrived < nDevToRecert:
                IoTDevLst[devArrived].firstArrTim = mstrClk + interArrTim    
                newArr = IoTDevLst[devArrived]
            
            if devArrived == nDevToRecert:
                newArr = infiniteDev
            
            if devArrived > nDevToRecert:
                print 'logic error 4'
                sys.exit()
           
                
        elif minOrbitDeal:
            mstrClk = minObtEvt.arrTimAfterOrbit
            if len(waitBuf) < buffLenLimit:
                if len(waitBuf) == 0:
                    servCompl = mstrClk + servTim
                    currServDev = minObtEvt
                    
                orbtEvtLst.pop(0)
                waitBuf.append(minObtEvt)
                
            else:
                minObtEvt.arrTimAfterOrbit += retransTim
                orbtEvtLst.pop(0)
                insertSortedOrbtList(orbtEvtLst, minObtEvt)
        else:
            print 'logic error 5'
            sys.exit()
            
    print mstrClk
    print 'Running time ' + str(time.time() - startTime)            
            
runIoTSim()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        