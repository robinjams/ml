#encoding:utf-8_*_
#author：@robin
#create time：2018/12/1 18:18
#file：new_mining.py
#IDE:PyCharm
import numpy as np
from Aprior_FPgrowth import FP_growth as fp
def loadData():
    with open('kosarak.dat','r') as fr:
        list = [line.split() for line in fr.readlines()]
    return list
if __name__=='__main__':
    data = loadData()
    print(data[:3])
    cai = fp.get_data(data)
    myFpTree,headerTable = fp.createTree(cai,100000)
    freItem = []
    #找到点击量大于100000的新闻
    freItem = fp.mineTree(myFpTree, headerTable, 100000, prefix=[], freItem=[])
    print('last freItem', freItem)