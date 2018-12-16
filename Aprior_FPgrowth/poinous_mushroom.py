#encoding:utf-8_*_
#author：@robin
#create time：2018/11/28 19:36
#file：poinous_mushroom.py
#IDE:PyCharm
import numpy as np
import Aprior_FPgrowth.aprior as aprior
data = []
with open('mushroom.dat','r') as fr:
    for line in fr.readlines():
        data.append(list(map(float,line.strip().split())))
print(data[0])
L,supportData = aprior.aprior(data,minsupport=0.4)
# print(L[0])
# for frequence in L[0]:
#     print(frequence,':',supportData[frequence])
#找出与毒蘑菇有关的特征，也就是与2有关
#L1具有一个特征与毒蘑菇相关
for item in set(L[1]):
    if item.intersection(set([2])):
        print('L1',item)
#L4具有一个特征与毒蘑菇相关
for item in set(L[4]):
    if item.intersection(set([2])):
        print('L4',item)