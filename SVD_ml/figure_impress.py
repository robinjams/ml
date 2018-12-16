#encoding:utf-8_*_
#author：@robin
#create time：2018/12/16 14:55
#file：figure_impress.py
#IDE:PyCharm
import numpy as np
from numpy import linalg as lg
import SVD_ml.recommend as recom
def print_fig(inMat,thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(inMat[i,k])>thresh:
                print(1,end='')
            else:
                print(0,end='')
        print('\n')
def impress(filename,thresh=0.8):
    myMat = []
    with open(filename,'r') as fr:
        for line in fr.readlines():
            num = []
            for i in range(32):
                num.append(int(line[i]))
            myMat.append(num)
    myMat = np.mat(myMat)
    print('original:')
    print_fig(myMat)
    u,sigma,v = lg.svd(myMat)
    k = recom.main_feature(sigma)
    sigmacon  = np.mat(np.zeros((k,k)))
    #转化对角矩阵
    for i in range(k):
        sigmacon[i,i] = sigma[i]
    recoveryMat = u[:,:k] * sigmacon * v[:k,:]
    return recoveryMat

if __name__=='__main__':
    filename = '0_5.txt';
    recoveryMat = impress(filename)
    print('recoveryMat')
    print_fig(recoveryMat)

