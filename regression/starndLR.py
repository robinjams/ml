#encoding:utf-8_*_
#author：@robin
#create time：2018/10/24 16:22
#file：starndLR.py
#IDE:PyCharm
import numpy as np
# from numpy import *
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties #添加c盘中的字体
#绘制散点图
def plotscatter():
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
    xcord = []; ycord = []
    file = open('ex0.txt')
    fig = plt.figure(figsize=(10,8))
    fig.clf()
    ax = fig.add_subplot(111)
    for line in file.readlines():
        liArr = line.strip().split('\t')
        # print(liArr)
        xcord.append(float(liArr[1]))
        ycord.append(float(liArr[2]))
    ax.scatter(xcord,ycord,marker='s')
    plt.title(u'数据散点图',FontProperties=font_set)
    # plt.title('Data Scatter')
    plt.show()
#自适应加载数据
def loadData(filename):
    numFeat = len(open(filename).readline().split('\t'))-1
    data = []; label = []
    for line in open(filename).readlines():
        linArr = []
        cur = line.strip().split('\t')
        for num in range(numFeat):
            linArr.append(float(cur[num]))
        data.append(linArr)
        label.append(float(cur[-1]))
        # print(label)
    return data,label
#标准回归W
def standRegression(dataArr,labelArr):
    dataMat = np.mat(dataArr)
    Label = np.mat(labelArr).T
    xTx = dataMat.T * dataMat
    if(np.linalg.det(xTx)==0.0):#行列式为0，表示不存在逆矩阵
        print('sorry,NO invert mat')
    else:
        w = xTx.I * (dataMat.T*Label)
    return w


if __name__=='__main__':

    #绘制散点图
    # plotscatter()
    #加载数据
    data,label = loadData('ex0.txt')
    # print(data[:3])
    # print(label[:3])
    dataMat = np.mat(data)
    LabelMat = np.mat(label)
    w = standRegression(data,label)
    # print('W:',w)
    # fig = plt.figure(figsize=(10,8))
    # ax = fig.add_subplot(111)
    #
    # #绘制数据散点图
    # # print([x[1] for x in data])#list获取列的方式，但是数组、矩阵可以直接切片data【：，1】
    # ax.scatter(dataMat[:,1].flatten().A[0],LabelMat.A[0])#绘制散点图
    # # ax.scatter(dataMat[:,1].flatten().A[0],LabelMat[:,0].flatten().A[0])#等价转换
    #
    #绘制回归曲线
    xcopy = np.mat(data.copy())
    xcopy.sort(0)#sort在本身上改变，sorted新生成,0表示按照第0维排序
    y = xcopy * w
    # # print('dataMat:',xcopy[:])
    # ax.plot(xcopy[:,1],y,c ='r')
    # plt.show()
    #
    #计算相关系数（西瓜书p415自己备注了含义）
    print('predict:',y)#预测值
    print('Label:',LabelMat)
    relation = np.corrcoef(LabelMat,y.T)
    print('correlation coefficent:',relation)



