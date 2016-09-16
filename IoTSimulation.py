import sys
import time 

DEBUG1 = False
DEBUG2 = True

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

def runIoTSim():
    global DEBUG
    
    infiniteDev = IoTDev()
    
    nDevToRecert = 1000
    
    if len(sys.argv) > 1:
        interArrTim = float(sys.argv[1])
        servTim = float(sys.argv[2])
        retransTim = float(sys.argv[3])
        buffLenLimit = float(sys.argv[4])
    else:
        '''interArrTim = 6
        servTim = 10
        retransTim = 5
        buffLenLimit = 2'''
        interArrTim = 17.98
        servTim = 2
        retransTim = 10
        buffLenLimit = 10
    
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
    if DEBUG1:
        print '\nMC\tCLA\tCLS\t#Queue\tCLR\n'
    
    devArrived = 0
    currServDev = None
    
    
    for dev in IoTDevLst:
        if dev.recertified:
            print dev.recertified
    
    while nDevRecert < nDevToRecert:
        if DEBUG1:
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
                if currServDev:              
                    currServDev.compltTim = servCompl
                    if currServDev.recertified == True:
                        print 'error 1'
                        sys.exit()
                    else:
                        currServDev.recertified = True
                
                
                mstrClk = servCompl
                servCompl = mstrClk + servTim
                
                if currServDev:
                    nDevRecert += 1
                    waitBuf.pop(0)
                
                if waitBuf:
                    currServDev = waitBuf[0]
                else:
                    currServDev = None
                
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
                    newArr.orbitFirstStartTim = mstrClk
                    newArr.arrTimAfterOrbit = mstrClk + retransTim
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
                minObtEvt.orbitEndTim = mstrClk
                
            else:
                minObtEvt.arrTimAfterOrbit += retransTim
                orbtEvtLst.pop(0)
                insertSortedOrbtList(orbtEvtLst, minObtEvt)
        else:
            print 'logic error 5'
            sys.exit()
    
    if DEBUG2:
        print 'MAster clock at the end ' + str(mstrClk)
    
    computationTime = time.time() - startTime
    if DEBUG2:
        print 'Sim done, Total Running time = ' + str(computationTime)            
    
    T = []
    D = []
    
    for index in range(len(IoTDevLst)):
        T.append(IoTDevLst[index].compltTim - IoTDevLst[index].firstArrTim)
        if IoTDevLst[index].orbitFirstStartTim != sys.maxint and IoTDevLst[index].orbitEndTim != sys.maxint:
            D.append(IoTDevLst[index].orbitEndTim - IoTDevLst[index].orbitFirstStartTim)
    
    if DEBUG2:
        print len(T), len(D), computationTime
    
    if DEBUG1:
        for dev in IoTDevLst:
            if not dev.recertified:
                print dev.recertified
    
    
runIoTSim()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        