#encoding:utf-8_*_
#author：@robin
#create time：2018/9/16 13:54
#file：plot.py
#IDE:PyCharm
import numpy as np
import random
import matplotlib.pyplot as plt
from SVM_ML import opstruct,svm_ml
fr = open("testSetRBF.txt")
xcoord0 = [];ycoord0 = [];
xcoord1 = [];ycoord1 = []
for line in fr.readlines():
    line = line.strip().split('\t')
    # print(line)
    if line[2] == 1:
        xcoord0.append(float(line[0]))
        ycoord0.append(float(line[1]))
    else:
        xcoord1.append(float(line[0]))
        ycoord1.append(float(line[1]))
fr.close()
fig = plt.figure()
ax = fig.add_subplot(111)
data,label = svm_ml.loadData('testSet.txt')
b,alpha = opstruct.smo(data,label,0.6,0.001,40)
support = []
for i in range(100):
    if alpha[i]>0:
        print(alpha[i])
        support.append(data[i])
print(support)
ax.scatter(xcoord0,ycoord0, marker='o', s=90, c = 'b')
ax.scatter(xcoord1,ycoord1, marker='o', s=50, c='red')
# #绘制支持向量
# for su in support:
#     circle = plt.Circle((su[0],su[1]),0.15,color='y')
#     ax.add_patch(circle)#绘制圆形
# #绘制曲线
# w = opstruct.getW(data,label,alpha)
# w0 = w[0][0];w1 = w[1][0]
# print(w0,w1)
# x_data = np.arange(0,6,0.5)
# x = x_data.reshape(len(x_data),1)
# y = (-w0*x-b)/w1
# ax.set_yticks((-6,6,1))
# ax.plot(x,y)

plt.show()
