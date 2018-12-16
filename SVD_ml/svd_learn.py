#encoding:utf-8_*_
#author：@robin
#create time：2018/12/5 21:01
#file：svd_learn.py
#IDE:PyCharm
import numpy as np
from numpy import linalg as lg
#欧氏距离
def eculide(inA,inB):
        return 1/(1+lg.norm(inA-inB))
#皮尔僧距离
def pearson(inA,inB):
        if len(inA) < 3:
                return 1.0
        return 0.5 + 0.5*np.corrcoef(inA,inB,rowvar=0)[0][1]
def cosDis(inA,inB):
        num = float(inA.T * inB)#注意矩阵转置
        mul = lg.norm(inA) * lg.norm(inB)+0.0001#假定计算列向量范数
        return 0.5+ 0.5*(num/mul)
def loadData():
        data =[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]
        return data

# u,sigma,v = np.linalg.svd(data)
# print('sigma',sigma)
# #根据svd分解后的sigma重构原始矩阵
# sigma_2 = np.mat([[sigma[0],0],[0,sigma[1]]])
# recovery_data = u[:,:2] * sigma_2 * v.T[:2,:]
# print('recovery_data',recovery_data)

#测试距离函数
data = np.mat(loadData())
# print(data[:,0]-data[:,0])
# disecu1 = eculide(data[:,0],data[:,0])
# disecu2 = eculide(data[:,0],data[:,4])
# print('distance eculide:',disecu1,' ',disecu2)
# discoDIs1 = cosDis(data[:,0],data[:,0])
# discoDIs2 = cosDis(data[:,0],data[:,4])
# print('distance cosDis:',discoDIs1,' ',discoDIs2)
# disPearson1 = pearson(data[:,0],data[:,0])
# disPearson2 = pearson(data[:,0],data[:,4])
# print('pearson distanse:',disPearson1,' ',disPearson2)