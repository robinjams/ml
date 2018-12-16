#encoding:utf-8_*_
#author：@robin
#create time：2018/8/6 11:49
#file：main.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
import json
from Tree import tree
from Tree import treeplot
import os,sys
from  Tree import getfileName
#测试数据的构造
data,labels = tree.create_data()
print('create data\n',data,'\n',labels)
# #测试生成熵
# result = tree.init_entroy(data)
# print('###shang lower means purity higer###\ncalulate shang:%f'%result)

#测试划分数据
# reset_data = tree.splite(data,0,1)
# reset_data1 = tree.splite(data,0,2)
# assert len(reset_data)==3 ,len(reset_data1)==2#增加断言
# print('与预期相同\n',reset_data,reset_data1)

#测试选择最好的属性
# best_feature = tree.choose_best_splite_data(data)
# print('选择出最好的分类属性:%d'%best_feature)

#测试多数表决
# majority = tree.majority([1,1,1,2,3,4,5])
# print('多数表决:',majority)

#测试决策树
tr = tree.create_tree(data,labels)
print('生成决策树：',tr)
txt = getfileName.getfile_name()
#为了避免每一次都需要才对数据重新生成决策树，将生成的决策树序列化到文件中
with open(txt,'w') as fp_write:
    #sort_keys是否排序、indent是否缩进、
    # separators分割的类型该参数的值应该是一个tuple(item_separator, key_separator)既可以清晰标示又可以避免indent造成的多余空白
    #,separators=(',',':')
    js = json.dumps(tr,sort_keys=False,indent=2)
    fp_write.write(js)
# print(list(tr.keys())[0])

#只要需要到决策树的函数，不需要重新生成决策树，只要反序列化就可以
with open(txt,'r') as fp_read:
    serial_tr = json.load(fp_read)
    print('反序列化结果：',serial_tr)


#绘制决策图
# treeplot.create_plot()

#获取叶子结点
# leafCount = tree.numLeaf(tr)
# assert leafCount == 3,'预期结果相同'
# print(leafCount)
# #获取树的深度
# depth = tree.get_tree_depth(mTree=tr)
# assert depth==2,'与预期不符'
# print(depth)

#绘制决策树
# treeplot.create_tree(mTree=serial_tr)#此处用到的是序列化结果，而不是决策树模型生成结果

#测试通过决策树分类
# data,label = tree.create_data()
# #这里直接调用之前的labels不能达到要求，在构造决策树的时候，已经逐步建labels中的特征删除
# testVec = [1,1]#测试向量
# classlabel = tree.classify_tree(mTree=tr,feature_label=label,testVec=testVec)
# print(testVec,'分类结果;',classlabel)



