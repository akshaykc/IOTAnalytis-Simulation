import sys
import time
import math
import random

#import numpy as np, scipy.stats as st



DEBUG0 = False
DEBUG1 = False
DEBUG2 = False
compTime = False

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

def standard_deviation(lst, lstMean):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    
    differences = [x - lstMean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd / num_items
    return math.sqrt(variance)

def getCfInt(aList):
    num_items = len(aList)
    mean = sum(aList) / num_items
    sd = standard_deviation(aList, mean)
    temp = (1.96*(sd))/ math.sqrt(num_items)
    interval=[]
    interval.append(mean - temp)
    interval.append(mean + temp)
    return interval

'''def getConfidenceInterval(aList):
    result = st.t.interval(0.95, len(aList)-1, loc=np.mean(aList), scale=st.sem(aList))
    return result
'''
def get95thPercentile(paramList):
    if paramList:
        paramList = sorted(paramList)
        return paramList[int(math.ceil(0.95*len(paramList)) - 1)]
    return 0
        
def getMean(paramList):
    if paramList:
        sumTemp = 0
        for elem in paramList:
            sumTemp += elem
        return float(sumTemp)/float(len(paramList))
    return 0
        
def insertSortedOrbtList(orbitList, dev):
    for index in range(len(orbitList)):
        if orbitList[index].arrTimAfterOrbit > dev.arrTimAfterOrbit:
            orbitList.insert(index, dev)
            return
    orbitList.append(dev)

'''def nextArrPoisson(avgArrRate):
    randomVal = random.random()
    return -math.log(1 - randomVal) / avgArrRate'''

def runIoTSim():
    global DEBUG1
    global DEBUG2
    
    infiniteDev = IoTDev()
    
    nDevToRecert = 1000
    
    T = []
    D = []
    P = []
    
    nT95Perc = []
    nD95Perc = []
    
    nTMeans = []
    nDMeans = []
    
    #nConfIntT = []
    #nConfIntD = []
    
    finalT95Perc, finalD95Perc, finalP95Perc = None, None, None
    finalTMean, finalDMean, finalPMean = None, None, None
    
    
    if len(sys.argv) > 1:
        interArrTim = float(sys.argv[1])
        servTim = float(sys.argv[2])
        retransTim = float(sys.argv[3])
        buffLenLimit = int(sys.argv[4])
        nIterations = int(sys.argv[5])
    else:
        '''interArrTim = 6.0
        servTim = 10.0
        retransTim = 5.0
        buffLenLimit = 2
        nIterations = 10'''
        
        interArrTim = 17.98
        servTim =   13.0
        retransTim = 10.0
        buffLenLimit = 5
        nIterations = 50
    
    
    for x in range(nIterations):
        random.seed(500)
        mstrClk = 0
        waitBuf = []
        orbtEvtLst = []
        IoTDevLst = []
        nDevRecert = 0
        servCompl = sys.maxint
        
        random.seed(x*7)
        
        '''First device'''
        dev = IoTDev(2.0)
        IoTDevLst.append(dev)
        
        for _ in xrange(1, nDevToRecert):
            dev = IoTDev()
            IoTDevLst.append(dev)
        
        newArr = IoTDevLst[0]
        
        
        if DEBUG1:
            print '\nMC\tCLA\tCLS\t#Queue\tCLR\n'
        
        devArrived = 0
        currServDev = None
        
        if DEBUG1:
            for dev in IoTDevLst:
                if dev.recertified:
                    print dev.recertified
                
        startTime = time.time()
        
        if DEBUG1:
            currResultString = ''
            open('output.txt','w+').close()
        while nDevRecert < nDevToRecert:
            if DEBUG0:
                if servCompl == sys.maxint:
                    currResultString = str(mstrClk) + '\t' + str(IoTDevLst[devArrived].firstArrTim) + '\t' + '-' + '\t' + str(len(waitBuf)) \
                        + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst]) +'\n'
                else:
                    currResultString = str(mstrClk) + '\t' + str(IoTDevLst[devArrived].firstArrTim) + '\t' + str(servCompl) + '\t' + str(len(waitBuf)) \
                     + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst])+'\n'
                with open('output.txt','a+') as outputFile:
                    outputFile.write(currResultString)
            
            if DEBUG1:
                if servCompl == sys.maxint:
                    print str(mstrClk) + '\t' + str(newArr.firstArrTim) + '\t' + '-' + '\t' + str(len(waitBuf)) \
                        + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst])
                else:
                    print str(mstrClk) + '\t' + str(newArr.firstArrTim) + '\t' + str(servCompl) + '\t' + str(len(waitBuf)) \
                        + '\t' + str([elem.arrTimAfterOrbit for elem in orbtEvtLst])
            
                
            '''if DEBUG1:
                if mstrClk > clkToStopSim:
                        sys.exit()    '''
                
                
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
                        newArr.arrTimAfterOrbit = mstrClk + random.expovariate(1/retransTim)
                    else:
                        print 'logic error 3'
                        sys.exit()
                    
                    insertSortedOrbtList(orbtEvtLst, newArr)
                    
                '''Create new device'''
                    
                devArrived += 1
                if devArrived < nDevToRecert:
                    #IoTDevLst[devArrived].firstArrTim = mstrClk + interArrTim
                    IoTDevLst[devArrived].firstArrTim = mstrClk +  random.expovariate(1/interArrTim)
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
                    minObtEvt.arrTimAfterOrbit += random.expovariate(1/retransTim)
                    orbtEvtLst.pop(0)
                    insertSortedOrbtList(orbtEvtLst, minObtEvt)
            else:
                print 'logic error 5'
                sys.exit()
        
        if DEBUG2:
            print 'Master clock at the end ' + str(mstrClk)
        
        computationTime = time.time() - startTime
        if DEBUG2:
            print 'Sim done, Total Running time = ' + str(computationTime)            
        
        
        '''Computer performance parameters'''
        TcurrIter = []
        DcurrIter = []
        if compTime:
            PcurrIter = computationTime
        else:
            PcurrIter = mstrClk
        
        for index in range(len(IoTDevLst)):
            if IoTDevLst[index].firstArrTim != sys.maxint and IoTDevLst[index].compltTim != sys.maxint:
                TcurrIter.append(IoTDevLst[index].compltTim - IoTDevLst[index].firstArrTim)
                if IoTDevLst[index].orbitFirstStartTim != sys.maxint and IoTDevLst[index].orbitEndTim != sys.maxint:
                    DcurrIter.append(IoTDevLst[index].orbitEndTim - IoTDevLst[index].orbitFirstStartTim)
        
        T.append(TcurrIter)
        D.append(DcurrIter)
        P.append(PcurrIter)
        
        if DEBUG2:
            print len(TcurrIter), len(DcurrIter), computationTime
        
        if DEBUG1:
            for dev in IoTDevLst:
                if not dev.recertified:
                    print dev.recertified
    
    '''Get statistics for each iteration and store'''
    for elem in T:
        nT95Perc.append(get95thPercentile(elem))
        nTMeans.append(getMean(elem))
        
    for elem in D:
        nD95Perc.append(get95thPercentile(elem))
        nDMeans.append(getMean(elem))
        
    '''Get statistics for N iterations'''
    finalT95Perc = get95thPercentile(nT95Perc)
    finalD95Perc = get95thPercentile(nD95Perc)
    finalP95Perc = get95thPercentile(P)
    
    finalTMean = getMean(nTMeans)
    finalDMean = getMean(nDMeans)
    finalPMean = getMean(P)
    
    ConfIntDMean = getCfInt(nDMeans)
    ConfIntTMean = getCfInt(nTMeans)
    ConfIntP = getCfInt(P)
    
    ConfIntD95P = getCfInt(nD95Perc)
    ConfIntT95P = getCfInt(nT95Perc)
    
    
    
    print '95T = ',finalT95Perc, '\t\t\t\t\t\t','95D = ', finalD95Perc, '\t\t\t\t\t\t','95P = ', finalP95Perc
    print '95TConInt = ',ConfIntT95P, '\t\t','95DConInt = ', ConfIntD95P, '\t\t','PConInt = ', ConfIntP
    
    print "\n"
    print 'MeanT = ',finalTMean,'\t\t\t\t\t\t','MeanD = ', finalDMean ,'\t\t\t\t\t\t','MeanP = ', finalPMean
    print 'MeanTConInt = ',ConfIntTMean, '\t\t','MeanDConInt = ', ConfIntDMean

    
    
runIoTSim()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        