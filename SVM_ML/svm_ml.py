#encoding:utf-8_*_
#author：@robin
#create time：2018/9/2 15:29
#file：svm_ml.py
#IDE:PyCharm
import numpy as np
import random
def loadData(filename):
    data = []; label = []
    for line in open(filename).readlines():
        temp = line.strip().split('\t')
        data.append( [ float(temp[0]), float(temp[1]) ] )
        label.append( float(temp[2]) )
    return data, label
def selectChar(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j
def cAlpha( aj, L, H):
    if aj > H:
        aj = H
    elif L > aj:
        aj = L
    return aj

# 简单smo算法
def simpleSmo(datatric, label, C, toler, maxiternum):
    #C常数项  toler容忍程度，表示SVM的间隔
    datatric = np.mat(datatric);label = np.mat(label).transpose()
    # print(label[:4])
    m,n = np.shape(datatric)
    alpha = np.mat(np.zeros((m,1)))#alpha矩阵
    b = 0
    iternum = 0
    # alphaPairsChanged 用来更新的次数
    # 当遍历  连续无更新 maxiternum轮，则认为收敛，迭代结束
    #好好理解这句话：只有在所有数据集上遍历maxiternum次，并且alpha不会发生变化，才会跳出while循环
    #   1、数据集遍历iternum次
    #   2、alpha不能发生变化，如果alpha发生变化，直接重新迭代
    #   3、如果在本次内循环中，alpha没有发生变化，则iternum次数+1
    while iternum < maxiternum:
        #当内循环结束一次后，重新令alphaparie=0
        alphaPair = 0
        #对于数据中的每一个数据向量
        for i in range(m):
            fxi = (np.multiply(alpha,label).T * (datatric*datatric[i,:].T)) + b
            Ei = fxi - float(label[i])
            # and or 语句区分：
            # （1）and:且，都为真才为真
            # （2）or:或，有一个为真就为真

            # 根据不满足KKT条件来选取alpha
            if (((label[i]*Ei < -toler) and (alpha[i] < C)) or ((label[i]*Ei > toler) and (alpha[i] > 0)) ):
                j = selectChar(i,m)
                fxj = np.multiply(alpha,label).T * (datatric*datatric[j,:].T)+b
                Ej = fxj - float(label[j])
                alphaIold = alpha[i].copy()
                alphaJold = alpha[j].copy()
                #是否属于同一类
                if label[i] != label[j]:
                    L = max(0, alpha[j] - alpha[i]);
                    H = min(C, alpha[j] - alpha[i] + C)
                else:
                    L = max(0, alpha[i] + alpha[j] - C);
                    H = min(C, alpha[i] + alpha[j])
                if L == H:
                    print("L==H");
                    continue
                eta = 2 * datatric[i, :] * datatric[j, :].T - datatric[i, :] * datatric[i, :].T - datatric[j, :] * datatric[j, :].T  # eta用来调整alpha的参数,注意后边是减法
                if eta >= 0: print("ets>=0");continue
                alpha[j] -= label[j] * (Ei - Ej) / eta  # 得到alpha【j】
                alpha[j] = cAlpha(alpha[j], L, H)  # 调整值
                if abs(alpha[j] - alphaJold) < 0.0001:
                    print("J not enough");#变化不大
                    continue
                alpha[i] += label[j] * label[i] * (alphaJold - alpha[j])  # 得到alphs[i]的值
                b1 = b - Ei - label[i] * (alpha[i] - alphaIold) * (alpha[i] * alpha[i].T) \
                     - label[j] * (alpha[j] - alphaJold) * (alpha[i] * alpha[j].T)
                b2 = b - Ej - label[i] * (alpha[i] - alphaIold) * (alpha[i] * alpha[j].T) \
                     - label[j] * (alpha[j] - alphaJold) * (alpha[j] * alpha[j].T)
                # 根据不同条件来选择b值
                if (0 < alpha[i]) and (alpha[i] < C):
                    b = b1
                elif (0 < alpha[j]) and (alpha[j] < C):
                    b = b2
                else:
                    b = (b1 + b2) / 2
                # 修改结束
                alphaPair += 1
                print("iternum %d,i:%d,J:%d,alphaPaired:%d" % (iternum, i,j, alphaPair))
        if alphaPair == 0:
            iternum += 1
        else:
            iternum = 0
        print("iter num:%d" %iternum)
    return b, alpha





if __name__== '__main__':
    data, label = loadData('testSet.txt')
    # print( np.shape(np.transpose(label[:5])) )
    print( label[:5] )
    print(data[:5])
    b, alphas = simpleSmo(data, label, 0.6, 0.001, 40)
    print(b)
    print(alphas[alphas>0])#表示对应的点是支持向量
    #输出支持向量的个数
    print(np.shape(alphas[alphas>0]))
    #输出支持向量
    for i in range(100):
        if alphas[i]>0:
            print((data[i],label[i]))



