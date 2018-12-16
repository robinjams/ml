#encoding:utf-8_*_
#author：@robin
#create time：2018/10/29 20:21
#file：abalonel_predict.py
#IDE:PyCharm
import numpy as np
import regression.LocalLineLR as LLR
import regression.starndLR as SLR
def rsserror(label,yhat):
    error = ((label-yhat)**2).sum()
    return error

if __name__=='__main__':
    data, label = LLR.loadData('abalone.txt')
    print(label[0:99])
    #最小二乘法回归
    weight = SLR.standRegression(data[0:99],label[0:99])
    yhat_stand = data[100:199]*weight
    # print(label[100:199])
    error_stand = rsserror(label[100:199],yhat_stand.T.A)
    print('error_stand',error_stand)
    # 新数据来测试回归
    newyHat = LLR.testlwlr(data[100:199], data[0:99], label[0:99], k=10)
    error_new_10 = rsserror(label[100:199], newyHat)
    print('error_new_10', error_new_10)


    #不同k值来预测
    yhat1 = LLR.testlwlr(data[0:99],data,label,k=1.0)
    error1 = rsserror(label[0:99],yhat1)
    print('error1',error1)
    yhat01 = LLR.testlwlr(data[0:99], data, label, k=0.1)
    error01 = rsserror(label[0:99], yhat01)
    print('error01', error01)
    yhat10 = LLR.testlwlr(data[0:99], data, label, k=10)
    error10 = rsserror(label[0:99], yhat10)
    print('error10', error10)



