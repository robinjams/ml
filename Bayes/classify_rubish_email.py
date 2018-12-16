#encoding:utf-8_*_
#author：@robin
#create time：2018/8/9 22:56
#file：classify_rubish_email.py
#IDE:PyCharm
import numpy as np
from  Bayes import bayes
import random

#文本解析
def textParse(str):
    import re
    # litoken = str.split()
    litoken = re.split(r'\W+',str)#\W*FutureWarning: split() requires a non-empty pattern match.会匹配长度为零的字符串，因此修改为\W+
    return [key.lower() for key in litoken if len(key)>2]

#留存交叉验证
def spamTest():
    import os
    root = os.getcwd()
    # print(root)
    classList = [];full_list = [];doc_list = []
    #读取文本
    for i in range(1,26):
        import os
        root = os.getcwd()
        spam = open(root+'\\email\\spam\\%d.txt'%i,'rb')
        ham = open(root+'\\email\\ham\\%d.txt'%i,'rb')
        doc_str = textParse(spam.read().decode('GBK'))
        doc_list.append(doc_str)
        full_list.extend(doc_str)
        classList.append(0)#0表示spam类别
        doc_str = textParse(ham.read().decode('GBK'))
        doc_list.append(doc_str)
        full_list.extend(doc_str)
        classList.append(1)#1表示ham类别
        # print(doc_list,'\n')
        #随机选择测试集与训练集
    vocal_dic = bayes.vocaList(doc_list)
    train_set = np.arange(50)
    test_set = []
    for i in range(20):
        test_index = int(random.uniform(0, len(train_set)))
        test_set.append(test_index)
        train_set = np.delete(train_set,test_index)
    train_mat = [];train_classify = []
    for train_key in train_set:
        # print(train_key)
        train_mat.append(bayes.word2Vec(vocal_dic,doc_list[train_key]))
        train_classify.append(classList[train_key])
    p0,p1,classify_prop = bayes.trainNB0(train_mat,train_classify)
    # print('训练数据参数：',p0,p1,classify_prop)
    #进行测试集验证
    error = 0.0#错误率
    for test_key in test_set:
        test_vec = bayes.word2Vec(vocal_dic,doc_list[test_key])
        result = bayes.classifyNB(test_vec, p0, p1, classify_prop)
        if result != classList[test_key]:
            error +=1.0
            print('classifier error',doc_list[test_key])
    # print(len(test_set))
    error_rate = error / len(test_set)
    return  error_rate




#导入模块后就不再运行这一块了，可以用来一般的测试
if __name__ == '__main__':

    # vocal_dic = bayes.vocaList(doc_list)
    train_set = np.arange(50)
    test_set = []
    for i in range(10):
        test_index = int(random.uniform(0, len(train_set)))
        test_set.append(test_index)
        train_set = np.delete(train_set, test_index)
    print(train_set,test_set)