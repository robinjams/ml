#encoding:utf-8_*_
#author：@robin
#create time：2018/8/6 11:59
#file：tree.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
from  math import log
import operator

#计算数据集中的熵
def init_entroy(data_set):
    # print('enter caculate Entroy')
    m = len(data_set)
    labelCount = { }
    for row_feature in data_set:
        current_feature = row_feature[-1]
        if current_feature not in labelCount.keys():
            labelCount[current_feature] = 0
        else:
            labelCount[current_feature]  +=1
    result_shang = 0.0
    for key in labelCount.keys():
        each = float(labelCount[key]/m)
        # print(key,':',each)
        #避免出现0求对数的情况
        if each==0:
            each +=0.01
        result_shang -= each * log(each,2)

    return result_shang
#构造数据
def create_data():
    data_set = [[1,1,'yes'],
                [1,1,'maybe'],
                [1,1,'maybe'],
                [1,1,'yes'],
                [1,0,'no'],
                [0,1,'no'],
                [0,1,'no'],
                # [0,1,'maybe']
                ]
    labels = ['no surfacing','flippers']#不浮出水面、是否脚蹼
    return data_set,labels
#划分数据集（为了根据属性划分不同的数据集,每一次会删除一列）
def splite(data_set,axis,value):#axis不表示维度，而是表示具体一维数组的这一列数据
    reset_data = []
    for data in data_set:
        if data[axis] == value:
            re_data = data[:axis]
            re_data.extend(data[axis+1:])#连接排除当前维度的数据
            reset_data.append(re_data)#虽然都是追加，但是与extend的追加效果不同
    return reset_data
#选择最好的属性去划分数据集
def choose_best_splite_data(data):
    m = len(data[0])-1#获得的是特征个数，因为有一个表示分类的，所以-1行，排除分类属性
    best_Gain = 0.0 #用来记录最好的信息增益
    best_feature = -1#初始化最好的特征
    base_entroy = init_entroy(data)#熵
    # print(base_Gain)
    for i in range(m):
        original = [simple[i] for simple in data]#获取该属性的分类标签，但是会有冗余
        source = set(original)#消除冗余
        new_entroy = 0.0
        for att in source:
            splite_data = splite(data,i,att)
            pro = len(splite_data)/float(len(data))
            new_entroy += pro * init_entroy(splite_data)#公式后半部分
            #通过决策树ID3来讲，前一部分公式求得的熵，是针对与所有的数据，也就是通过分类来求得
            #                   后一部分公式，是根据具体某一属性，然后在该属性的样本集中求得的熵
        new_gain = base_entroy-new_entroy#计算信息增益
        # print('属性%d的信息增益:%f'%(i,new_gain))
        if new_gain > best_Gain:
            best_Gain = new_gain
            best_feature = i
    return best_feature

#多数表决
def majority(classList):
    classCount = { }
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote]  += 1
    sort_class = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    # print(sort_class)#返回元组list
    return sort_class[0][0]

#决策树
def create_tree(dataset,labels):
    classList = [example[-1] for example in dataset]
    #属于同一类，则返回该类别
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #所有属性都已使用结束，通过多数投票来输出类别
    if len(dataset[0])==1:
        return majority(classList)#投票最后一列（分类的标签）
    best_feature = choose_best_splite_data(dataset)#最好的特征
    # print('特征序号:',best_feature)
    best_feature_label = labels[best_feature]
    # print('特征名：',best_feature_label)
    mTree = {best_feature_label:{}}
    del labels[best_feature]#删除指定位置的值
    simple_feature = [example[best_feature] for example in dataset]
    value = set(simple_feature)#去重之后的每个划分特征的属性
    for val in value:
        sublabel = labels[:]
        ##比如具有A   B   C
        #          1  1   1
        #          2  2   2
        #          3  3   3
        #label=['A','B','C']
        #当A特征已经作为最好的特征的时候，现在需要在字典中添加A特征中的每一个属性，
        # 此时就需要用到迭代，首先需要分别划分找到除了A特征维度中value值是等于1、2、3的值（但是会去掉A特征维度）
        #一直到在函数开始给出的两种终止迭代条件：（1）分类完全相同（2）用完了所有的属性，需要投票机制决定
        mTree[best_feature_label][val] = create_tree(splite(dataset,best_feature,val),  )#迭代获取每一个特征的属性值的分类结果
    return mTree

#通过决策树分类

def classify_tree(mTree,feature_label,testVec):
    parent_node = list(mTree.keys())[0]
    son_node = mTree[parent_node]
    # print(parent_node)
    feature = feature_label.index(parent_node)#找到位置
    for key in son_node.keys():
        if testVec[feature] ==key:
            if type(son_node[key]) == dict:
                classLabel = classify_tree(son_node[key],feature_label,testVec)
            else:
                classLabel = son_node[key]

    return classLabel
#以下代码是为了绘制决策树图
#获取叶子节点的数目
def numLeaf(myTree):
    leafCount = 0
    parent_node = list(myTree.keys())[0]#获取决策树的第一个特征
    son_node = myTree[parent_node]#获取该特征下的属性，当然该属性也可能是字典
    for key in son_node.keys():#迭代特征的属性值
        if type(son_node[key])== dict:
            leafCount += numLeaf(son_node[key])
        else:
            leafCount += 1
    return leafCount
#得到树的深度
def get_tree_depth(mTree):
    maxdepth = 0
    parent_node = list(mTree.keys())[0]
    son_node = mTree[parent_node]
    for key in son_node.keys():
        if type(son_node[key]) == dict:
            thisdeep = 1 + get_tree_depth(son_node[key])
        else:
            thisdeep = 1
        if thisdeep > maxdepth: maxdepth = thisdeep
    return maxdepth


