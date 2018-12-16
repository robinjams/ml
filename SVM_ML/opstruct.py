#encoding:utf-8_*_
#author：@robin
#create time：2018/9/15 11:10
#file：opstruct.py
#IDE:PyCharm
import numpy as np
from SVM_ML import svm_ml

#使用类的目的在于使用结构中的变量
class opstruct:
    def __init__(self,data, label, C, toler ):
        self.data = data
        self.label = label
        self.C = C
        self.b = 0
        self.toler = toler
        self.m = np.shape(data[:,])[0]
        self.alpha = np.mat(np.zeros((self.m, 1)))
        self.eCache = np.mat(np.zeros((self.m, 2)))
def cacuE(os, k):
    fxk = float(np.multiply(os.alpha, os.label).T * (os.data*os.data[k,:].T))+os.b
    Ek = fxk -float(os.label[k])#真实值-预测值
    return Ek
# 启发式选择j
def selectJ(i, os, Ei):
    maxK = -1; maxDelta = 0; Ej = 0
    os.eCache[i] = [i,Ei]
    validlist = np.nonzero(os.eCache[:,0].A)[0]#选择不为0的返回list,  .A表示以数组的形式返回
    # print(validlist)
    if len(validlist)>1:
        for k in validlist:
            if k==i:continue
            Ek = cacuE(os, k)
            delta = abs(Ek - Ei)
            if delta > maxDelta:
                maxDelta = delta;maxK = k;Ej = Ek
        # print('max',maxK,Ej)
        return maxK,Ej
    else:
        j = svm_ml.selectChar(i, os.m)
        Ej = cacuE(os, j)
    return j,Ej
def update(os,k):
    Ek = cacuE(os, k)
    os.eCache[k] = [1,Ek]
#内层循环优化
def innerL(i,os):
    Ei =cacuE(os,i)
    if (((os.label[i]*Ei < -os.toler) and (os.alpha[i]<os.C)) or (((os.label[i]*Ei > os.toler) and (os.alpha[i]>0)))):
        #((1)选择j
        j,Ej = selectJ(i,os,Ei)
        # print(j)
        alphaOldI = os.alpha[i].copy();alphaOldJ = os.alpha[j].copy()
        if (os.label[i] != os.label[j]):
            L = max(0,os.alpha[j] - os.alpha[i])
            H = min(os.C, os.C+os.alpha[j]-os.alpha[i])
        else:
            L = max(0,os.alpha[i]+os.alpha[j]-os.C)
            H = min(os.C,os.alpha[i]+os.alpha[j])
        if L==H:print("L==H");return 0
        #更新alpha[i] alpha[j]
        eta = 2 * os.data[i,:]*os.data[j,:].T - os.data[i,:]*os.data[i,:].T - os.data[j,:]*os.data[j,:].T
        if eta >=0 :print("eta>=0");return 0
        os.alpha[j] -= os.label[j]*(Ei - Ej)/eta#忘记了更新alpha[j] 的时候除以参数eta,导致alpha[j] 更新错误
        os.alpha[j] = svm_ml.cAlpha(os.alpha[j],L,H)
        update(os,j)#更新了alpha[j]对应的值
        if abs(alphaOldJ-os.alpha[j])<0.001:
            print("j not enough")
            return 0
        os.alpha[i]  += os.label[i]*os.label[j]*(alphaOldJ-os.alpha[j])
        update(os,i)
        #更新b
        #点乘的形式得到的是一个值，而叉乘的形式得到的是一个向量
        bi = os.b - Ei - os.label[i]*(os.alpha[i]-alphaOldI)*(os.data[i,:]*os.data[i,:].T)-os.label[j]*(os.alpha[j]-alphaOldJ)*(os.data[i,:]*os.data[j,:].T)
        bj = os.b - Ej - os.label[i]*(os.alpha[i]-alphaOldI)*(os.data[i,:]*os.data[j,:].T)-os.label[j]*(os.alpha[j]-alphaOldJ)*(os.data[j,:]*os.data[j,:].T)
        if (os.alpha[i]>0) and (os.alpha[i]<os.C):os.b = bi
        elif (os,os.alpha[j]>0) and (os.alpha[j]<os.C):os.b= bj
        else:os.b = (bi+bj)/2
        return 1
    else:return 0

#SMO算法
def smo(data,label,C,toler,maxIter):
    os = opstruct(np.mat(data),np.mat(label).transpose(),C,toler)
    iter = 0;entry = True;alphaPaired = 0
    while ((iter < maxIter) and ((alphaPaired > 0) or (entry==True))):
        # print(entry)
        alphaPaired = 0
        #支持向量边
        if entry == True:
            for i in range(os.m):
                alphaPaired += innerL(i, os)
                print("fullSet:data iter%d,i:%d,change paire%d" % (iter, i, alphaPaired))
            iter += 1
        else:
            #边界边更新alpha
            nonBoundsIs = np.nonzero((os.alpha.A > 0) * (os.alpha.A < C) )[0]
            # print(nonBoundsIs)
            for i in nonBoundsIs:
                alphaPaired += innerL(i, os)
                print("nonBoundIS:iter%d,i:%d,change paire%d" % (iter, i, alphaPaired))
            iter += 1
        # print('--------------------------',entry)
        # print('--------------------',alphaPaired)
        if entry==True:entry=False
        elif (alphaPaired==0):entry=True#这个条件表明：entry=False并且非边界没有改变alpha，则重新针对支持向量alpha；如果非边界改变alpha，继续迭代非边界
        print("outLoop iter:%d"%iter)
    return os.b,os.alpha
def getW(data,label,alpha):
    data = np.mat(data);label = np.mat(label).transpose()
    m,n = np.shape(data)
    w = np.zeros((n,1))
    for i in range(m):
        w += np.multiply(alpha[i]*label[i] ,data[i,:].T)
    return w

if __name__=='__main__':
    from SVM_ML import svm_ml
    #得到两个矩阵之间共有非零元素的索引
    print(np.nonzero((np.mat([1,23,0,9,0]).A >0 )*(np.mat([1,2,3,0,0]).A>0 )))
    #测试修改后的platt SMO算法
    data,label = svm_ml.loadData('testSet.txt')
    b,alpha = smo(data,label,0.6,0.001,40)
    w = getW(data,label,alpha)#得到w的值
    # for i in ]range(100):
    #     if alpha[i]>0:
    #         print(data[i],label[i])
    #检测预测是否正确
    print("预测：",np.mat(data[0])*np.mat(w)+b)
    print("真实：",label[0])
