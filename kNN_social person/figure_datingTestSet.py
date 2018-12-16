#encoding:utf-8_*_
#author：@robin
#create time：2018/8/3 11:33
#file：figure_datingTestSet.py
#IDE:PyCharm
import kNN
matric,vict = kNN.file2matric('datingTestSet2.txt')
# kNN.showdata(matric,vict)#绘图
#归一化结果
# normal,min,range = kNN.autoNormal(matric)
# print(normal[0:5,:])
# print(min,'\n',range)
#数据分类
# kNN.data_classify_test()
#与用户交互，具体分类某一个人
kNN.classify_person()
#40920	8.326976	0.953952
#35483	12.273169	1.508053