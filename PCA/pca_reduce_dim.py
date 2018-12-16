#encoding:utf-8_*_
#author：@robin
#create time：2018/12/1 20:42
#file：pca_reduce_dim.py
#IDE:PyCharm
import numpy as np
from numpy import linalg
def loadData(filename):
    data = []
    with open(filename,'r',encoding='utf-8') as fr:
        for line in fr.readlines():
            data.append(list(map(float,line.strip().split())))
    return np.mat(data)

def pca(data,topFeature = 9999):
    data_mean = np.mean(data,axis=0)
    normal = data-data_mean
    corr = np.cov(normal,rowvar=0)#默认将列作为一个独立的变量，如果设置rowvar=0将行作为独立的变量
    #对于数组求得的特征值、特征向量依旧是数组；矩阵对应于矩阵
    fvalue,fvet = linalg.eig(np.mat(corr))#将这个协方差数组转化为协方差矩阵
    fvalue = np.argsort(fvalue)
    mainFeature = fvalue[:-(topFeature+1):-1]
    mainVet = fvet[:,mainFeature]
    lowData = normal * mainVet#ps:是中心化数据与特征向量相乘，而不是原始数据相乘
    recover_data = (lowData * mainVet.T) + data_mean
    #最终返回 降维数据和重构后的的数据
    return lowData,recover_data
def plot(dataMat,recover_data):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='*',s=20,color = 'yellow')
    ax.scatter(recover_data[:,0].flatten().A[0],recover_data[:,1].flatten().A[0],marker='+',s=20,color = 'r')
    plt.title('PCA reduce')
    plt.show()
#将NAN转化为该列的均值
def deal_data(filename):
    import math
    data = loadData(filename)
    # data =np.mat( [[1,2,2],
    #         [math.nan,math.nan,2],
    #         [math.nan,math.nan,2]
    #         ])
    # print(data)
    num_fea = np.shape(data)[1]
    for i in range(num_fea):
        mean = np.mean(data[np.nonzero(~np.isnan(data[:,i].A))[0],i])#所有元素求均值,~对于布尔值相当于取反
        data[np.nonzero(np.isnan(data[:,i].A))[0],i] = mean
    return data
if __name__=='__main__':
    import math
    filename = 'testSet.txt'
    data = loadData(filename)
    lowData, recover_data = pca(data,1)
    # print('lowdata',lowData[:12])
    # print('recover_data',recover_data[:12])
    #绘制降维后图形
    # plot(data, recover_data)

    #大量数据的情况下讨论PCA
    filename = 'secom.data'
    data = deal_data(filename)
    mean = np.mean(data,axis=0)
    normal = data - mean
    corr = np.cov(np.mat(normal),rowvar=0)
    feat_val,feat_vet = linalg.eig(corr)
    print('feat_val',feat_val[1])
    print('feat_vet',feat_vet[1])
