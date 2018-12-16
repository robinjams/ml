#encoding:utf-8_*_
#author：@robin
#create time：2018/10/21 14:21
#file：adaboost.py
#IDE:PyCharm
import numpy as np
def loadSimple():
    dataMat = [[1,2.1],[2,1.1],[1.3,1],[1,1],[2,1]]
    datalabel =  [1.0,1.0,-1.0,-1.0, 1.0]
    return dataMat,datalabel
# 定义单层决策树函数,分类函数
def stumpclassify(dataMat,dimen,thresh,thresh_inq):
    m = np.shape(dataMat)[0]
    # 返回m行1列
    # """将数据第dimen维特征与thresh比较，根据大小以及thresh_ineq来判定样本分到哪个类
    # thresh_ineq用于设置是大于thresh为负样本还是小于thresh为负样本"""
    returnArr = np.ones((m,1))
    for i in range(m):
        if(thresh_inq=='lt'):
            returnArr[dataMat[:,dimen]<=thresh] = -1.0
        else:
            returnArr[dataMat[:,dimen]>thresh] = -1.0
    return returnArr
# 单层决策树
def stumpTree(dataMat,datalabel,D):
    data = np.mat(dataMat);label = np.mat(datalabel).transpose()
    m,n = np.shape(dataMat)
    numstep = 10.0#每一个特征选择10个thresh
    beststump = {}#存储最优的特征
    bestclass = np.mat(np.zeros((m,1)))#存储最优分类
    minerror = np.inf
    for i in range(n):
        rangeMin = data[:,i].min();rangeMax = data[:,i].max()
        step = (rangeMax-rangeMin) / numstep
        for j in range(-1,int(numstep)+1):#从-1开始，表明这10个thresh，有一个从左边开始
            for inq in ['lt','gt']:#小于、大于
                threshval = rangeMin + j * step
                predict = stumpclassify(data,i,threshval,inq)
                error = np.mat(np.ones((m,1)))
                error[predict==label]=0
                weighterror = D.T * error
                # print('character(dim):%d,thresh:%f,type:%s,weighterror:%f'%(i,threshval,inq,weighterror))
                if(weighterror<minerror):
                    minerror = weighterror
                    bestclass = predict
                    beststump['dim'] = i
                    beststump['thresh'] = threshval
                    beststump['inq'] = inq
                    beststump['weighterror'] = weighterror
    return beststump,bestclass,minerror

#adaboost算法
def adaboost(dataMat,label,numIter = 20):
    weakArr = []#弱分类器集合
    m = np.shape(dataMat)[0]
    D = np.mat(np.ones((m,1))/m)#表示每一个数据点的权重
    agg_class_res = np.mat(np.zeros((m,1)))#f(x)在训练集上的结果
    for i in range(numIter):
        print('iter:%d'%i)
        beststump, bestclass, minerror = stumpTree(dataMat, label, D)
        print('D',D.T)
        alpha = float(0.5*np.log((1-minerror)/max(minerror,1e-16)))#避免初始的时候错误率为0
        #记录最优弱分类器
        beststump['alpha'] = alpha
        weakArr.append(beststump)
        print('Bestclass:',bestclass.T)
        #更新样本权重
        expon = np.multiply(-1*alpha*np.mat(label).T,bestclass)
        D = np.multiply(D,np.exp(expon))
        D = D/D.sum()
        # print(alpha)
        # print(bestclass)
        # print(alpha*bestclass)
        agg_class_res += alpha*bestclass
        print('agg_class_res:',agg_class_res)
        agg_error = np.multiply(np.sign(agg_class_res)!=np.mat(label).T,np.ones((m,1)))#不同则为1，相同则为0
        error = agg_error.sum()/m
        print('total error:',error)
        if(error==0.0):
            break
    return weakArr,agg_class_res
#多个弱分类器组成强分类器
def adaclassify(dataArr,classiffier):
    print('-------start enhanced classify--------')
    dataM = np.mat(dataArr)
    m = np.shape(dataM)[0]
    agg_class = np.zeros((m,1))
    for i in range(len(classiffier)):
        class_label = stumpclassify(dataM,classiffier[i]['dim'],classiffier[i]['thresh'],classiffier[i]['inq'])
        agg_class += classiffier[i]['alpha']*class_label
        print('class_label',class_label)
        print('agg_class',agg_class)
    return np.sign(agg_class)

if __name__=='__main__':
    D = np.mat(np.ones((5,1))/5)
    dataMat,label =  loadSimple()

    #测试stumpTree
    # beststump, bestclass, minerror = stumpTree(dataMat,label,D)
    # print('bestclass',bestclass)
    # print('beststump',beststump)
    # print('minerror',minerror)

    #测试adaboost算法
    # weakarr= adaboost(dataMat,label)
    # print(weakarr)

    #测试强分类adaclassify
    weakarr= adaboost(dataMat,label)#返回弱分类器字典
    betterClass = adaclassify(dataMat,weakarr)
    otherpoint = [[1.2,1],[1.3,1]]#测试其他数据点
    otherClass = adaclassify(otherpoint,weakarr)
    print('weakarr:',weakarr)
    print('enhanced classify result:',betterClass)
    print('other classify result:',otherClass)


