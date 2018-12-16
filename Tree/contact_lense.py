#encoding:utf-8_*_
#author：@robin
#create time：2018/8/9 11:00
#file：contact_lense.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
from Tree import tree
from Tree import treeplot
from Tree import getfileName
import json
with open('lenses.txt','r') as fp:
    lense =[line.strip().split('\t') for line in fp.readlines()]
    # print(lense)
lense_labels = ['age','prescript','astigmatic','tearRate']
mTree = tree.create_tree(lense,lense_labels)
#序列化到文件
txt = getfileName.getfile_name()
with open(txt,'w') as fp1:
    js = json.dumps(mTree,indent = 2)
    fp1.write(js)
#从文件中读出后，直接绘图
with open(txt,'r') as fp2:
    mTree = json.load(fp2)
#绘制决策树图
treeplot.create_tree(mTree)

