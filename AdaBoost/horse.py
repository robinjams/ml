#encoding:utf-8_*_
#author：@robin
#create time：2018/10/23 10:47
#file：horse.py
#IDE:PyCharm
import numpy as np
from AdaBoost import adaboost
#加载数据(自适应特征)
def loadData(filename):
    numFeat = len(open(filename).readline().split('\t'))
    dataMat = [];Label = []
    file = open(filename)
    for line in file.readlines():
        lineArr = []
        Arr = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(Arr[i]))
        dataMat.append(lineArr)
        Label.append(float(Arr[-1]))
    return dataMat,Label
#绘制ROC和求得AUC的值
#Roc表现了分类器的性能
def plotROC(predStrength,classLabel):
    from matplotlib import pyplot as plt
    cur = (1.0,1.0)
    ynum = 0.0
    numPositive = np.sum(np.array(classLabel)==1.0)
    print('numPositive:',numPositive)
    print('numNegtive:',len(classLabel)-numPositive)
    ystep = 1/float(numPositive)#真正例率比率
    xstep = 1/float(len(classLabel)-numPositive)#假正例率比率
    index_All = predStrength.argsort()#所有样本结果排序
    # print('index_all:',index_All);exit();
    fig = plt.figure(figsize=(8, 5))
    fig.clf()#清空
    ax = fig.add_subplot(111)
    for index in index_All.tolist()[0]:
        if(classLabel[index]==1.0):
            xdel = 0;ydel = ystep
        else:
            xdel=xstep;ydel=0
            ynum += cur[1]#在之后计算AUC需要用到，只有在假正例率改变之后，才会出现新的矩形面积
        ax.plot([cur[0],cur[0]-xdel],[cur[1],cur[1]-ydel])#绘制roc曲线
        cur = (cur[0]-xdel,cur[1]-ydel)
        # print([cur[0],cur[0]-xdel],[cur[1],cur[1]-ydel])
    ax.plot([0,1],[0,1],c='r')#标注绘制的阈值最大点【0，0】所有都为负例和阈值最小点【1,1】所有都为正例
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('roc figure')
    plt.show()
    auc = float(ynum * xstep)
    print('auc:%f'%auc)

if __name__=='__main__':

    # #训练数据
    # data,Label = loadData('horseColicTraining.txt')
    # # print(data[:3])
    # # print(Label[:3])
    # classArr = adaboost.adaboost(data,Label,20)
    # print('cai classifier:\n',classArr)


    # #测试数据
    # testdata,testLabel = loadData('horseColicTest.txt')
    # predict =  adaboost.adaclassify(testdata,classArr)
    # m,n = np.shape(np.mat(testdata))#获取数据集的条数
    # error = np.ones((m,1))
    # print('predict:',predict)
    # print('Label\n',np.mat(testLabel) )
    # #实现方式一
    # count_error = 0
    # for i in range(m):
    #     if(predict[i]!=(np.mat(testLabel).T)[i]):
    #         count_error +=1
    # print('count error:%d,error rate:%f'%(count_error,float(count_error/m)))
    # # 数组过滤的作用在于找出满足条件的元素
    # # li = ["a", "mpilgrim", "foo", "b", "c", "b", "d", "d"]
    # # print([elem for elem in li if len(elem) > 1])
    # # 比较预测与真实值是否相同
    # #实现方式二
    # print('array filter:',error[predict != (np.mat(testLabel).T)])  # 数组过滤
    # sumerror = error[predict != (np.mat(testLabel).T)].sum()  # 数组过滤
    # errorTotal = float(sumerror / m)
    # print('sumerror:', errorTotal)
    # plot([1,1],[1,1])

    #绘制ROC曲线
    #依旧存在问题，adaboost算法的结果roc曲线并不好，依旧存在问题
    data,label = loadData('horseColicTraining.txt')
    classarr,agg_class = adaboost.adaboost(data,label,5)
    # print('lala',agg_class)
    plotROC(predStrength=agg_class.T,classLabel=label)