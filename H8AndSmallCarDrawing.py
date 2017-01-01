# coding:utf-8
#实现H8数据和小车数据的同步画图
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
fileName = 'gps.txt'
fileCarName = 'carData12.11.1.txt'
def toRadias(x):
    x = x / 180 * math.pi
    return x


def readCarData(fileCarName):
    global numCar
    fileCar = open(fileCarName, 'a+')
    phoneArray = fileCar.readlines()
    numCar = len(phoneArray)
    # print numCar
    global CarDataMatrix, CardataX, CardataX2
    CarDataMatrix = zeros((numCar, 4))
    CardataX = zeros((numCar, 2))
    CardataX2 = zeros((numCar, 2))
    # phoneArray[0].split(' ')
    for i in range(numCar):
        CarDataMatrix[i, 0] = float(phoneArray[i].split(',')[0])
        CarDataMatrix[i, 1] = float(phoneArray[i].split(',')[1])
        CarDataMatrix[i, 2] = float(phoneArray[i].split(',')[2])
        CarDataMatrix[i, 3] = float(phoneArray[i].split(',')[3])
        if CarDataMatrix[i , 0]==0:
            CarDataMatrix[i , 0]=CarDataMatrix[i-1 , 0]
            CarDataMatrix[i , 1]=CarDataMatrix[i-1 , 1]
        CarDataMatrix[i, 0] = toRadias(CarDataMatrix[i, 0])
        CarDataMatrix[i, 1] = toRadias(CarDataMatrix[i, 1])
def readData(fileName):
    global num
    fileCar = open(fileName, 'a+')
    phoneArray = fileCar.readlines()
    num = len(phoneArray)
    # print num
    global DataMatrix, dataX, dataX2
    DataMatrix = zeros((num-1, 2))
    dataX = zeros((num-1, 2))
    dataX2 = zeros((num-1, 2))
    phoneArray[0].split(' ')
    for i in range(num):
        if i>0:
            DataMatrix[i-1, 0] = float(phoneArray[i].split('\t')[1])
            DataMatrix[i-1, 1] = float(phoneArray[i].split('\t')[0])
            # DataMatrix[i, 0] = int(DataMatrix[i, 0] / 100) + (DataMatrix[i, 0] - int(DataMatrix[i, 0] / 100) * 100) / 60
            # DataMatrix[i, 1] = int(DataMatrix[i, 1] / 100) + (DataMatrix[i, 1] - int(DataMatrix[i, 1] / 100) * 100) / 60
            # print DataMatrix[i - 1, 0]
            # print DataMatrix[i - 1, 1]
            DataMatrix[i-1, 0] = toRadias(DataMatrix[i-1, 0])
            DataMatrix[i-1, 1] = toRadias(DataMatrix[i-1, 1])
def SAC(TargetLat,initPointLat):
    #Sac是y轴上的距离
    alpha = TargetLat - initPointLat
    polynoinal1 = a ** 2 * b ** 2 * (1 + math.tan(TargetLat) ** 2) * math.sin(alpha) ** 2 / (
        a ** 2 * math.tan(TargetLat) ** 2 + b ** 2)
    polynoinal2 = a * b * math.sqrt(
        (1 + math.tan(initPointLat) ** 2) / (a ** 2 * math.tan(initPointLat) ** 2 + b ** 2))
    polynoinal3 = a * b * math.sqrt(
        (1 + math.tan(TargetLat) ** 2) / (a ** 2 * math.tan(TargetLat) ** 2 + b ** 2)) * math.cos(alpha)
    ACDis=math.sqrt(polynoinal1 + (polynoinal2 - polynoinal3) ** 2)
    return ACDis
def myFuncCar(initPointLat,initPointLong):
    #RInitial是原点到地心的距离；dataX2[0,0]是纬度，dataX2[0,1]是经度，都是自己方法计算的结果，dataX是vincenty的计算结果
    PointNum=num
    RInitial=a * b * sqrt((1 + math.tan(initPointLat) ** 2) / (a ** 2 * math.tan(initPointLat) ** 2 + b ** 2))
    for i in range(PointNum - 1):
        dataX2[i, 0] = RInitial * math.cos(initPointLat) * (DataMatrix[i, 1] - initPointLong)
        if DataMatrix[i, 0] >= DataMatrix[0, 0]:
            dataX2[i, 1] = SAC(DataMatrix[i, 0],initPointLat)
        else:
            dataX2[i, 1] = -1 * SAC(DataMatrix[i, 0],initPointLat)
            # print math.sqrt(dataX2[i, 0] ** 2 + dataX2[i, 1] ** 2)
            # print dataX2[i, 0]
            # print dataX2[i, 1]
    for i in range(PointNum - 1):
        dataX2[i, 0] = RInitial * math.cos(DataMatrix[0, 0]) * (DataMatrix[i, 1] - DataMatrix[0, 1])
        if DataMatrix[i, 0] >= DataMatrix[0, 0]:
            dataX2[i, 1] = SAC(DataMatrix[i, 0],initPointLong)
        else:
            dataX2[i, 1] = -1 * SAC(DataMatrix[i, 0],initPointLong)
    return 0
def myFuncSmallCar(initPointLat,initPointLong):
    #RInitial是原点到地心的距离；CardataX2[0,0]是纬度，CardataX2[0,1]是经度，都是自己方法计算的结果，CardataX是vincenty的计算结果
    PointnumCar=numCar
    RInitial=a * b * sqrt((1 + math.tan(initPointLat) ** 2) / (a ** 2 * math.tan(initPointLat) ** 2 + b ** 2))
    for i in range(PointnumCar ):
        CardataX2[i, 0] = RInitial * math.cos(initPointLat) * (CarDataMatrix[i, 1] - initPointLong)
        #
        if CarDataMatrix[i, 0] >= initPointLat:
            CardataX2[i, 1] = SAC(CarDataMatrix[i, 0],initPointLat)
        else:
            CardataX2[i, 1] = -1 * SAC(CarDataMatrix[i, 0],initPointLat)
    return 0
a = 6378245
b = 6356863.01877
readData(fileName)
readCarData(fileCarName)
initPointLat=DataMatrix[0, 0]
initPointLong=DataMatrix[0, 1]
myFuncCar(initPointLat,initPointLat)
myFuncSmallCar(initPointLat,initPointLong)
xmin = 18000
xmax = -1000
ymin = 18000
ymax = -1000
i = 0
for i in xrange(num-1):
    if dataX2[i, 0] > xmax:
        xmax = dataX2[i, 0]
    if dataX2[i, 0] < xmin:
        xmin = dataX2[i, 0]
    if dataX2[i, 1] > ymax:
        ymax = dataX2[i, 1]
    if dataX2[i, 1] < ymin:
        ymin = dataX2[i, 1]
for i in range(numCar):
    if CardataX2[i, 0] > xmax:
        xmax = CardataX2[i, 0]
    if CardataX2[i, 0] < xmin:
        xmin = CardataX2[i, 0]
    if CardataX2[i, 1] > ymax:
        ymax = CardataX2[i, 1]
    if CardataX2[i, 1] < ymin:
        ymin = CardataX2[i, 1]
f2 = plt.figure(2)
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
plt.title('myFunc')
plt.xlabel('x/m')
plt.ylabel("y/m", fontname="Times New Roman Italic")
for i in range(numCar):
    if CarDataMatrix[i,3]==4:
        a2 = plt.scatter(CardataX2[i, 0], CardataX2[i, 1], marker=".", color='r')
    elif CarDataMatrix[i,3]==5:
        a1 = plt.scatter(CardataX2[i, 0], CardataX2[i, 1], marker="*", color='g')
    elif CarDataMatrix[i,3]==2:
        a3 = plt.scatter(CardataX2[i, 0], CardataX2[i, 1], marker="+", color='b')
a4 = plt.scatter(dataX2[:, 0], dataX2[:, 1], marker="+", color='b')
plt.show()