import numpy as np
import matplotlib.pyplot as plt
'''
servTime = [11,12,13,14,15,16,17]
meanT = [19.7303604926,23.8851933541,29.702302287,38.3440043201,53.5932023817,73.5856613863,142.897317415]
meanD = [21.9103053073,23.6986845203,31.1722904364 ,37.5545080157, 51.9078722907,69.3022354046,135.946354106] 
meanP = [17977.2404581,17936.6017022,17962.9911096,17958.153464,17897.7526751,18148.1205514 , 18174.3716502]



# red dashes, blue squares and green triangles
meanTPlot, = plt.plot(servTime, meanT, '.r-',label="Mean T")
meanDPlot, = plt.plot(servTime, meanD, 'xb-',label="Mean D")
plt.legend(handles=[meanTPlot,meanDPlot])
plt.show()
'''
'''
servTime = [11,12,13,14,15,16,17]
T95 = [52.1059116019 , 62.6119827865,88.3963837767 ,134.439364027 ,195.977234927, 329.217888857,886.220625195]
D95 = [118.164955876 ,104.505759852,190.494372456  ,258.713424854 , 268.57783629 ,398.758819506 ,939.873160014 ] 

meanTPlot, = plt.plot(servTime, T95, '.r-',label="95 percentile T")
meanDPlot, = plt.plot(servTime, D95, 'xb-',label="95 percentile D")
plt.legend(handles=[meanTPlot,meanDPlot])
plt.show()
'''
'''
servTime = [11,12,13,14,15,16,17]
meanD = [21.9103053073,23.6986845203,31.1722904364 ,37.5545080157, 51.9078722907,69.3022354046,135.946354106] 
D95 = [118.164955876 ,104.505759852,190.494372456  ,258.713424854 , 268.57783629 ,398.758819506 ,939.873160014 ] 

meanTPlot, = plt.plot(servTime, D95, '.r-',label="95 percentile D")
meanDPlot, = plt.plot(servTime, meanD, 'xb-',label="Mean D")
plt.legend(handles=[meanTPlot,meanDPlot])
plt.show()
'''
'''
servTime = [11,12,13,14,15,16,17]

meanP=[ 17977.2404581,17936.6017022,17962.9911096,17958.153464, 17897.7526751 ,18148.1205514,18174.3716502]


meanTPlot, = plt.plot(servTime, meanP, '.r-',label="Mean P")
plt.legend(handles=[meanTPlot])
plt.show()
'''
'''

bufSize = [1,3,5,7,10,15,20]

MeanD = [159.815937598,80.790442541,69.3022354046, 67.7111239812,64.3433755657,24.4720093435,9.88020949561]


meanTPlot, = plt.plot(bufSize, MeanD, '.r-',label="Mean D")
plt.legend(handles=[meanTPlot])
plt.show()
'''

bufSize = [1,3,5,7,10,15,20]

MeanT = [158.520178976,77.9412998131,73.5856613863,77.3941478109,80.4736007077,73.3649076438, 74.8646251302 ]

meanTPlot, = plt.plot(bufSize, MeanT, '.r-',label="Mean T")
plt.legend(handles=[meanTPlot])
plt.show()
