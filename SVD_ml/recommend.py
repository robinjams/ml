#encoding:utf-8_*_
#author：@robin
#create time：2018/12/7 20:48
#file：recommend.py
#IDE:PyCharm
import numpy as np
from SVD_ml import svd_learn
from operator import itemgetter
from numpy import linalg as lg

from numpy import *
from numpy import linalg as la
def loadExData2():
    return[
            [2, 0, 0,4,4,0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]
def eststand(dataMat,user,item,sim_fun):
    n = np.shape(dataMat)[1]
    totalSim = 0.0; totalRate = 0.0
    for j in range(n):
        rate = dataMat[user,j]
        if (rate == 0):
            continue
        overLap = np.nonzero(np.logical_and(dataMat[:,item],dataMat[:,j]))[0]
        if len(overLap)==0:
            similarity = 0
        else:
            similarity = sim_fun(dataMat[overLap,item],dataMat[overLap,j])
        totalSim += similarity
        totalRate += similarity * rate
    if totalSim==0:
        return 0.0
    return totalRate/totalSim
#用户对商品的评分
def svdEst(dataMat,user,item,sim_fun):
    n = np.shape(dataMat)[1]
    totalSim = 0.0;totalRate = 0.0
    u,sigma,v = lg.svd(dataMat)
    k = main_feature(sigma)#找到主要特征
    sigma_last = np.mat(np.eye(k)*sigma[:k])
    reduce_item = dataMat.T * u[:,:k] * sigma_last.I#降维后的物品空间
    for i in range(n):
        rate = dataMat[user,i]
        if rate==0 or i==item:#因为已经将数据去稀疏，所以会与eststand 31row 的有点差别
            continue#用户没有对商品评分，所以跳过
        simlarity = sim_fun(reduce_item[item,:].T,reduce_item[i,:].T)
        print('物品%d与物品%d的相似度是:%f'%(item,i,simlarity))
        totalSim += simlarity
        totalRate += simlarity * rate
    if totalSim==0:
        return 0.0
    else:
        return totalRate/totalSim

#调用svdEst函数的推荐函数
# def recommend1(dataMat,user,N = 3,est_fun = eststand,sim_fun =svd_learn.cosDis ):
def recommend1(dataMat,user,N = 3,est_fun = eststand,sim_fun =svd_learn.eculide ):
    no_rate_item = np.nonzero(dataMat[user,:].A==0)[1]
    print(no_rate_item)
    recommed_rate = []
    for item  in no_rate_item:
        rate = est_fun(dataMat,user,item,sim_fun)
        recommed_rate.append((item,rate))
    last =  sorted(recommed_rate,key=itemgetter(1),reverse=True)[:N]
    return last
#找到总量>90%的特征个数
def main_feature(sigma):
    num = np.sum(sigma)
    count = 0;
    index = 1
    for i in sigma:
        count += i
        if count / num > 0.8:
            break
        else:
            index += 1
    return  index



if __name__=='__main__':
    #标准推荐
    # dataMat =np .mat([
    #     [4,4,0,2,2],
    #     [4,0,0,3,3],
    #     [4,0,0,1,1],
    #     [1,1,1,2,0],
    #     [2,2,2,0,0],
    #     [1,1,1,0,0],
    #     [5,5,5,0,0]
    # ])
    # print(dataMat)
    # result1 = recommend1(dataMat,2)
    # print('recommd1',result1)

    #svd降维后推荐
    dataMat = np.mat(loadExData2())
    u, sigma, v = lg.svd(dataMat)
    k = main_feature(sigma)  # 找到主要特征
    print('main feature num', k)
    result2 = recommend1(dataMat,est_fun=svdEst,user=1)
    print('recommend2',result2)


