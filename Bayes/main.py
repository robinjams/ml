#encoding:utf-8_*_
#author：@robin
#create time：2018/8/9 16:46
#file：main.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
from Bayes import bayes,classify_rubish_email
#word2Vec
# data,labels = bayes.loadDataSet()
# vocalist = bayes.vocaList(data)#生成的词典
# print('生成的词典：',vocalist)


#测试具体的一句话，词袋模型将输入文档（词条）对应的为向量
# testinput_set = ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please','my']
# bag_word2Vec = bayes.bag_word2Vec(vocalist,testinput_set)
# print(bag_word2Vec)
# #测试具体的一句话，词集模型将输入文档（词条）对应的为向量
# word2Vec = bayes.word2Vec(vocalist,testinput_set)
# print(word2Vec)

#判断输入文档集合是某一类别的概率

##将文档集合转化为举证的形式表示，每一个【】中包含一个文档向量
# matric = []
# for da in data:
#     matric.append( bayes.word2Vec(vocalist,da))
# prop0,prop1,pab = bayes.trainNB0(matric,labels)
# print('文档属于1类别概率：',pab)
# print('文档中每个单词属于类别1的概率\n',prop1)
# print('文档中每个单词属于类别0的概率\n',prop0)

#测试贝叶斯分类(网站恶意留言)
# testEntry = ['love','please','I']
# testEntry = ['I','dog','Trump']
# classVec = bayes.word2Vec(vocalist,testEntry)
# print(classVec)
# matric = []
# for da in data:
#     matric.append(bayes.word2Vec(vocalist,da))
# prop0,prop1,classprop = bayes.trainNB0(matric,labels)
# result = bayes.classifyNB(classVec,prop0,prop1,classprop)
# if result==1:
#     re = '侮辱词条'
# else:
#     re = '非侮辱词条'
# print(testEntry,'分类结果为：',re)

#邮件分类之转换文字
# import os
# root = os.getcwd()
# file = 1
# with open(root+'\\email\\ham\\%d.txt'%file,'r') as fp:
#     str = fp.read()
#     li_token = classify_rubish_email.textParse(str)
#     print(li_token)

#邮件分类

#返回文档列表和所有词汇列表
# doc_list,full_list = classify_rubish_email.spamTest()
# # print("doc:\n",doc_list)
# # print('full:\n',full_list)
#得到每一个单词表示某一类的概率

#查看返回的概率,注意完整代码已经不支持，只是在编程阶段测试
# p0,p1,prop = classify_rubish_email.spamTest()
# print('p0 spam:\n',len(p0),p0)
# print('p1 ham:\n',len(p1),p1)
# print('-------------------啦啦啦:',prop)

#最终测试分类,进行十次后计算平均错误率
#计算一次错误率
error_rate = classify_rubish_email.spamTest()
print('error rate:',error_rate)

#十次错误率求平均
# error_rate = []
# last = 0.0
# for i in np.arange(10):
#     error_rate.append(classify_rubish_email.spamTest())
# for i in error_rate:
#     last +=  i
# print('mean error rate:',last/len(error_rate))