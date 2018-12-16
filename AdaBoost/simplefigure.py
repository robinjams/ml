#encoding:utf-8_*_
#author：@robin
#create time：2018/10/21 14:25
#file：simplefigure.py
#IDE:PyCharm
import numpy as np
from matplotlib import pyplot as plt
from AdaBoost import adaboost as boost
fig = plt.figure(figsize=(8,5))
dataMat,label = boost.loadSimple()
data = np.array(dataMat)
m,n = np.shape(dataMat)
x1 = [];y1 = []
x2 = [];y2 = []
for i in range(m):
    if(label[i]==1.0):
        x1.append(data[i,0])
        y1.append(data[i,1])
    else:
        x2.append(data[i, 0])
        y2.append(data[i, 1])
ax = fig.add_subplot(111)
ax.scatter(x1,y1,marker = 's')
ax.scatter(x2,y2,marker = 'o')
plt.title('simple data')
plt.show()