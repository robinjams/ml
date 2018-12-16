#encoding:utf-8_*_
#author：@robin
#create time：2018/9/15 11:10
#file：opstruct.py
#IDE:PyCharm
import numpy as np
from SVM_ML import svm_ml
import os


#使用类的目的在于使用结构中的变量
class opstruct:
    def __init__(self,data, label, C, toler,ktup ):
        self.data = data
        self.label = label
        self.C = C
        self.b = 0
        self.toler = toler
        self.m = np.shape(data[:,])[0]
        self.alpha = np.mat(np.zeros((self.m, 1)))
        self.eCache = np.mat(np.zeros((self.m, 2)))
        self.k = np.mat(np.zeros((self.m,self.m)))
        #因为 求解核函数看k(x,xi),所以才会在迭代的时候选择列来迭代
        for i in range(self.m):
            self.k[:,i] = kernal(data,data[i,:],ktup)
def cacuE(os, k):
    # fxk = float(np.multiply(os.alpha, os.label).T * (os.data*os.data[k,:].T))+os.b
    # print(os.alpha)
    # print(os.label)
    fxk = float(np.multiply(os.alpha, os.label).T * (os.k[:,k])+os.b)
    Ek = fxk -float(os.label[k])#真实值-预测值
    return Ek
# 启发式选择j
def selectJ(i, os, Ei):
    maxK = -1; maxDelta = 0; Ej = 0
    os.eCache[i] = [i,Ei]
    validlist = np.nonzero(os.eCache[:,0].A)[0]#选择不为0的返回list,  .A表示已数组的形式返回
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
        eta = 2 * os.k[i,j] - os.k[i,i] - os.k[j,j]
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
        bi = os.b - Ei - os.label[i]*(os.alpha[i]-alphaOldI)*(os.k[i,i])-os.label[j]*(os.alpha[j]-alphaOldJ)*(os.k[i,j])
        bj = os.b - Ej - os.label[i]*(os.alpha[i]-alphaOldI)*(os.k[i,j])-os.label[j]*(os.alpha[j]-alphaOldJ)*(os.k[j,j])
        if (os.alpha[i]>0) and (os.alpha[i]<os.C):os.b = bi
        elif (os,os.alpha[j]>0) and (os.alpha[j]<os.C):os.b= bj
        else:os.b = (bi+bj)/2
        return 1
    else:return 0

#SMO算法
def smo(data,label,C,toler,maxIter,ktup = ('line',0)):
    os = opstruct(np.mat(data),np.mat(label).transpose(),C,toler,ktup)
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
#得到权重
def getW(data,label,alpha):
    data = np.mat(data);label = np.mat(label).transpose()
    m,n = np.shape(data)
    w = np.zeros((n,1))
    for i in range(m):
        w += np.multiply(alpha[i]*label[i] ,data[i,:].T)
    return w
#构造核函数，只有线性和函数和高斯核函数
def kernal(data,A,ktup):
    #data:数据集
    #A:某一行数据
    #ktup('type','character')核函数类型+参数的元组
    m,n = np.shape(data)
    k = np.zeros((m,1))
    if ktup[0]=='line':
        k = data*A.T
    elif ktup[0]=='rbf':
        for i in range(m):
            delta = data[i]-A
            k[i] = delta*delta.T
        k = np.exp(k/(-1*ktup[1]**2))#ktup[1]径向基核函数的参数，在高斯核函数中，该参数叫做确定到达率，也就是函数值跌落到0的速度参数
    else:
        'sorry ,not support the kernal function'
    return k
def hello():
    print('hello')
#测试高斯径向基
def RBF(k1 = 1.3):
    data, label = svm_ml.loadData("testSetRBF.txt")
    dataMat = np.mat(data);labelMat = np.mat(label).transpose()
    b, alpha = smo(data, label, 0.6, 0.001, 5,('rbf',k1))
    # print(b)
    svInd = np.nonzero(alpha.A>0)[0]
    # print(svInd)
    svs = dataMat[svInd]
    svlabel = labelMat[svInd]
    print("support vetor number:%d" %np.shape(svs)[0])
    m,n = np.shape(dataMat)
    errorCount = 0
    # 只考虑了支持向量
    for i in range(m):
        ker = kernal(svs,dataMat[i,:],("rbf",1.3))

        # *对应数组：对应元素相乘、对应矩阵：矩阵运算
        # mutiply:对应数组：对应元素相乘、对应数组：对应相乘相加的和
        predict = ker.T * np.multiply(alpha[svInd],svlabel)+b
        if np.sign(predict[0][0])!= np.sign(label[i]):
            errorCount += 1
    print("trining error rate:%f"%float(errorCount/m))
    errorCount = 0
    data,label = svm_ml.loadData("testSetRBF2.txt")
    dataMat = np.mat(data);labelMat = np.mat(label)
    m,n = np.shape(dataMat)
    for i in range(m):
        ker = kernal(svs,dataMat[i,:],("rbf",0.5))

        # *对应数组：对应元素相乘、对应矩阵：矩阵运算
        # mutiply:对应数组：对应元素相乘、对应数组：对应相乘相加的和
        predict = ker.T * np.multiply(alpha[svInd],svlabel)+b
        if np.sign(predict[0][0])!= np.sign(label[i]):
            errorCount += 1
    print("testing error rate:%f"%float(errorCount/m))

# 图片转化为一维向量
def imag2Victor(dirname,filename):
    victor = np.zeros((1,1024))
    with open(dirname+filename,'r',encoding='utf-8') as f:
        for i in range(32):
            line = f.readline()
            for j in range(32):
                victor[0,32*i+j] = line[j]
    return victor
# 加载图片
def loadimage(dir):
    trainlabel = []
    dirs = os.listdir(dir)
    m = len(dirs)
    trainMat = np.zeros((m,1024))
    for i in range(m):
        dirname = dirs[i]
        firdivide = dirname.split('.')[0]
        trainresult = firdivide.split('_')[0]
        if trainresult=='9':
            trainlabel.append(1)
        else:
            trainlabel.append(-1)
        trainMat[i,:] = imag2Victor(dir,dirname)
    return trainMat,trainlabel
# svm手写识别
def testDigits(kTup=('rbf',0.5)):
    pwd = os.getcwd()
    # print(pwd)
    # dirs  = os.listdir(pwd+"\\testDigits")
    # print(dirs)
    dataArr, datalabelArr = loadimage(pwd + "\\trainingDigits\\")
    dataMat = np.mat(dataArr)
    # 数据标签转置，否则无法获取对应元素    Svlabel = datalabel[svInd]
    datalabel = np.mat(datalabelArr).transpose()
    print('datalabel:\n',datalabel);
    print('data:',dataArr[1:3],datalabelArr[1:3])
    # 训练模型
    b,alpha = smo(dataArr,datalabelArr,200,0.01,10,kTup)
    svInd = np.nonzero(alpha.A>0)[0]
    print('svind:',svInd)
    Svs = dataMat[svInd]
    Svlabel = datalabel[svInd]
    print('support number :%d'%np.shape(Svs)[0])
    # 训练集
    errorCount = 0
    m,n = np.shape(dataMat)
    for i in range(m):
        ker = kernal(Svs,dataMat[i,:],kTup)
        predict = ker.T * np.multiply(Svlabel,alpha[svInd]) + b
        print(np.sign(predict[0][0]))
        print(float(np.sign((datalabel[i])[0][0])))
        if(np.sign(predict[0][0])!=float(np.sign((datalabel[i])[0][0]))):
            print('not the same')
            errorCount += 1
            print(errorCount)
        else:
            print('the same')
        print('training error rate:%f'%float(errorCount/m))
    lasttrain = float(errorCount/m)

    # 测试集
    datatestArr, datatestLArr = loadimage(pwd + "\\testDigits\\")
    datatestM = np.mat(datatestArr);
    datatestL = np.mat(datatestLArr).transpose()
    m, n = np.shape(datatestM);
    errorCount = 0
    # 支持向量都不需要改变，直接拿训练出的支持向量来进行预测
    for i in range(m):
        ker = kernal(Svs, datatestM[i, :], kTup)
        predict = ker.T * np.multiply(Svlabel, alpha[svInd]) + b
        print(np.sign(predict[0][0]))
        print(float(np.sign((datatestL[i])[0][0])))
        if (np.sign(predict[0][0]) != float(np.sign((datatestL[i])[0][0]))):
            print('not the same')
            errorCount += 1
            print(errorCount)
        else:
            print('the same')
        print('testing error rate:%f' % float(errorCount / m))
    lasttest = float(errorCount / m)
    print('Last training error rate:%f' %lasttrain )
    print('Last testing error rate:%f' % lasttest)

if __name__=='__main__':
    # RBF(k1=1.3)
    # test = [[-0.12229919]]
    # la = [[-1]]
    # print(np.sign(test[0][0]))
    # print(float(np.sign(la[0][0])))
    # if np.sign(test[0][0])==float(np.sign(la[0][0])):
    #     print('lal')
    testDigits()

