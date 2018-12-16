#encoding:utf-8_*_
#author：@robin
#create time：2018/10/31 14:51
#file：ridge_reg.py
#IDE:PyCharm
import numpy as np
from regression import starndLR as st
from matplotlib import pyplot as plt
#解决线性回归问题中x'x无法求逆的问题
#计算权重
def ridgeRes(dataMat,labelMat,lam = 0.2):
    xTx = dataMat.T*dataMat
    denom = xTx+np.eye((np.shape(dataMat)[1]))*lam
    inverse = np.linalg.det(denom)
    print(inverse)
    if(inverse==0.0):
        print('this matric is sigular mat,no invert matric')
    else:
        w = denom.I * (dataMat.T*labelMat)
    return w
#测试岭回归
def ridgeTest(data,label):
    dataMat = np.mat(data);labelMat = np.mat(label).transpose()
    numpoint = 30
    wMat = np.zeros((numpoint,np.shape(dataMat)[1]))
    #标准化
    dataMean = np.mean(dataMat,0)#列平均，即同一特征平均
    labelMean = np.mean(labelMat,0)
    labelMat = labelMat - labelMean
    dataVar = np.var(dataMat,0)
    dataMat = (dataMat - dataMean)/dataVar
    for i in range(numpoint):
        weight = ridgeRes(dataMat,labelMat,np.exp(i-10))
        wMat[i,:] = weight.T
    return wMat
if __name__=='__main__':
    data,label = st.loadData('abalone.txt')
    #测试单个lamda权重
    dataMat = np.mat(data);labelMat = np.mat(label).transpose()
    weight = ridgeRes(dataMat,labelMat)
    print('w:',weight)
    print('character num:',np.shape(weight)[0])
    #多个lamda权重集合
    wMat = ridgeTest(data,label)
    print('wMat',wMat)
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)
    ax.plot(wMat)
    plt.title('diffrent lamda ridge coefficient')
    plt.show()
