#encoding:utf-8_*_
#author：@robin
#create time：2018/8/4 17:05
#file：KNN_writer.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
import os
import operator
#分类
def classify(A,dateSet,labels,k):
    dateSize = dateSet.shape[0]
    relation  = np.tile(A,(dateSize,1))-dateSet
    squar = relation**2
    result = (squar.sum(axis=1))**0.5
    sort_re= result.argsort()
    Count = {}
    #只需要统计结果
    for i in range(k):
        vote = labels[sort_re[i]]
        Count[vote] = Count.get(vote,0)+1
    #将统计结果排序,items函数，将一个字典以列表的形式返回，因为字典是无序的，所以返回的列表也是无序的。
    final = sorted(Count.items(),key=operator.itemgetter(1),reverse=True)
    return final[0][0]#获取具体的某个分类
def imag2Victor(filename):
    victor = np.zeros((1,1024))
    with open(filename,'r',encoding='utf-8') as f:
        for i in range(32):
            line = f.readline()
            for j in range(32):
                victor[0,32*i+j] = line[j]
    return victor
def hand_writer():
    hwLabel = []

    #训练数据的标签，其实就是与测试数据计算距离的原始数据
    trainfile = os.listdir('trainingDigits')
    # print(trainfile[:10])
    m = len(trainfile)
    train_matric = np.zeros((m,1024))
    cwd = os.getcwd()#获得当前目录
    for i in range(m):
        num_original =(trainfile[i].split('.'))[0]
        num_final = num_original.split('_')[0]
        hwLabel.append(num_final)
        # print(cwd+'\\trainingDigits\\'   + trainfile[i])
        train_matric[i,:] = imag2Victor(cwd+'\\trainingDigits\\'+ trainfile[i])
    #测试数据，用做分类的数据
    testfile = os.listdir('testDigits')
    # print(trainfile[:10])
    m_test = len(testfile)
    errorCount = 0
    for i in range(m_test):
        num_original_test = (testfile[i].split('.'))[0]
        num_final_test = int(num_original_test.split('_')[0])
        test_victor = imag2Victor(cwd+'\\testDigits\\'+ testfile[i])
        classify_result = classify(test_victor,train_matric,hwLabel,3)
        print('classifier get\'s result is: %d,And real character is %d\n' \
                  % (int(classify_result),num_final_test))
        if (int(classify_result) != num_final_test):
            errorCount += 1
    print('\n error\'s count is:%d'%errorCount)
    print('\nclassifier error ratio is:%f' % (errorCount / float(m_test)))  # 错误率表示错误数除以总数
