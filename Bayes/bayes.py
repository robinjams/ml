#encoding:utf-8_*_
#author：@robin
#create time：2018/8/9 16:32
#file：bayes.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid'],
                 ['i','hate','the','correctness','Trump'],
                 ]
    labels = [0,1,0,1,0,1,1]
    return postingList,labels
def vocaList(data_set):
    voca = set([])
    for list_data in data_set:
        voca = voca | set(list_data)#集合的并
    return list(voca)
#词集模型，每个词出现一次
def word2Vec(vocalist,input_set):
    return_vec = [0]*len(vocalist)#返回是否包含词典中的单词
    for key in input_set:
        if key in vocalist:
            return_vec[vocalist.index(key)] = 1
        else:
            print('该词汇%s不在字典中'%key)
    return return_vec
#文档词袋模型，与词集模型的区别在于，每个单词可以出现多次
def bag_word2Vec(vocalist,input_set):
    returnVec = [0]*len(vocalist)
    for key in input_set:
        if key in vocalist:
            returnVec[vocalist.index(key)] +=1
    return returnVec
#得到概率
def trainNB0(trainmatric,traincatory):
    n_document = len(trainmatric)
    n_vocation = len(trainmatric[0])
    #由于概论是连乘，避免没有出现的单词，初始设置为1
    p0_num = np.ones(n_vocation);p1_num = np.ones(n_vocation)
    p0_demo = 2.0;p1_demo = 2.0
    #先验概率，每个类别文档所占的概率
    classprop = sum(traincatory)/n_document
    for i in range(n_document):
        if traincatory[i]==1:#一类文章中每一个此条出现的数目
            p1_num += trainmatric[i]#一类文章中词条出现的总数目
            p1_demo += sum(trainmatric[i])
        else:
            p0_num += trainmatric[i]
            p0_demo += sum(trainmatric[i])
    #使用log求解避免太多很小的数相乘，造成下溢出，结果四舍五入变为0
    prop1 = np.log(p1_num/p1_demo) #属于第一类文章的概率
    prop0 = np.log(p0_num / p0_demo ) # 属于第一类文章的概率
    return prop0,prop1,classprop

#贝叶斯分类
def classifyNB(classifyVec,prop0,prop1,classprop):
    p1 = sum(classifyVec*prop1)+np.log(classprop)
    p0 = sum(classifyVec*prop0)+np.log(classprop)
    if p1>p0:
        return 1
    else:
        return 0



