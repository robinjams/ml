#encoding:utf-8_*_
#author：@robin
#create time：2018/10/29 14:05
#file：LocalLineLR.py
#IDE:PyCharm
import numpy as np

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
#局部加权线性回归函数
def lwlr(testPoint,xArr,yArr,k=1.0):
    # print('k=%f'%k)
    xMat = np.mat(xArr); yMat = np.mat(yArr).T
    m = np.shape(xMat)[0]
    weights = np.mat(np.eye((m)))
    for j in range(m):                      #next 2 lines create weights matrix
        diffMat = testPoint - xMat[j,:]     #
        weights[j,j] = np.exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if np.linalg.det(xTx) == 0.0:
        print ("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    # print(testPoint) m* n
    # print(ws)  n*1
    return testPoint * ws
def testlwlr(testArr,data,label,k):
    m = np.shape(np.mat(testArr))[0]
    ymat = np.zeros((m))
    for i in range(m):
        # print('testArr',testArr)
        ymat[i] = lwlr(testArr[i],data,label,k)
    return ymat
#局部线性加权绘制图像
def plotscatter(data,label,k):
    from  matplotlib import pyplot as plt
    predict_mul = testlwlr(data, data, label, k)
    dataMat = np.mat(data)
    sortInd = dataMat[:, 1].argsort(0)
    # print(sortInd)
    sort = dataMat[sortInd][:, 0, :]  # 因为返回了一个三维数组，所以得转化为二维数组
    # print(sort)
    dataM = np.mat(data);Label = np.mat(label).transpose()
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)
    # print(np.mat(predict_mul[sortInd]).flatten().A[0])#用于测试散点数据
    ax.plot(sort[:,1],predict_mul[sortInd])#绘制预测线段
    # ax.scatter(sort[:,1].flatten().A[0],np.mat(predict_mul[sortInd]).flatten().A[0],c= 'b')#绘制预测散点图
    ax.scatter(dataMat[:,1].flatten().A[0],Label.T.flatten().A[0],c='r')#绘制数据散点图
    plt.title('local line logical regression')
    plt.show()
if __name__=='__main__':
    data,label = loadData('ex0.txt')
    print(data[0])
    # 测试lwlr函数
    print('label one', label[0])
    predict = testlwlr([data[0]], data, label,k=1.0)
    print('one point predict:', predict)
    print('label double', label[0], label[1])
    predict_double = testlwlr(data[0:2], data, label,k=1.0)
    print('double point predict:', predict_double)
    #绘图
    # plotscatter(data,label,k=0.003)#过拟合
    plotscatter(data,label,k=0.01)#拟合效果比较好
    # plotscatter(data,label,k=1.0)#与最小二乘法效果相差不大


