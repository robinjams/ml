#encoding:utf-8_*_
#author：@robin
#create time：2018/11/1 9:18
#file：lasso.py
#IDE:PyCharm
import numpy as np
import regression.starndLR as stand
from numpy import *
from matplotlib import pyplot as plt
#lasso的功能:解决最小当特征数大于样本数，特征存在冗余的时候
#标准化矩阵
def regular(xMat,yMat):
    yMean = np.mean(yMat,0)
    xMean = np.mean(xMat,0)
    xVar = np.var(xMat,0)
    yMat = yMat-yMean
    xMat = (xMat-xMean)/xVar
    return xMat,yMat
def rsserror(label,yhat):
    error = ((label-yhat)**2).sum()
    return error
#lasso算法中由于具有绝对值函数，因此求导的时候有必要进行处理，（1）贪心算法：先找到一个特征，固定其他系数，优化该特征（前向逐步回归）
#                                                            （2）逐一优化：固定某一维度，选择某一维度进行优化
def forword_step_res(xArr,yArr,eps=0.01,numIter=10):
    xMat = np.mat(xArr);yMat = np.mat(yArr).transpose()
    xMat,yMat = regular(xMat,yMat)
    m,n = np.shape(xMat)
    returnweight = np.zeros((numIter,n))
    weight = np.zeros((n,1))
    wTest = weight.copy();wMax = weight.copy()
    print('w original:', weight.T)
    for i in range(numIter):
        lower = np.inf
        for j in range(n):
            for chang in [-1,1]:
                wTest = weight.copy()
                wTest[j] += eps*chang
                yTest = xMat*wTest
                # print('yMat',yMat.A)
                # print('yTest',yTest.A)
                error = rsserror(yMat.A,yTest.A)
                if(error<lower):
                    lower = error
                    wMax = wTest
        weight = wMax.copy()
        returnweight[i,:] = weight.T
        # print('returnweight',returnweight);exit()
    return returnweight


if __name__=='__main__':
    xArr,yArr = stand.loadData('abalone.txt')
    iter_weight = forword_step_res(xArr,yArr,eps=0.005,numIter=1000)
    # iter_weight = forword_step_res(xArr,yArr)
    print('last weight:\n',iter_weight)
    fig = plt.figure(figsize=(8,5))
    ax1 = fig.add_subplot(111)
    ax1.plot(iter_weight)
    ax1.plot(iter_weight)
    plt.xlabel('iter num')
    plt.ylabel('every feature corfficient')
    plt.title('different iter weight')
    plt.show()
    ws = stand.standRegression(xArr,yArr)
    print('最小二乘法权重：',ws.T)



