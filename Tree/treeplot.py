
#encoding:utf-8_*_
#author：@robin
#create time：2018/8/7 22:56
#file：treeplot.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
from Tree import tree
leaf_node = dict(boxstyle = 'round4',fc ='r')
decide_node = dict(boxstyle = 'sawtooth',fc = 'b')
arrow_arg = dict(arrowstyle = '<-')#指向标注内容
def plot_node(describe,target_node,source_node,nodetype):

    create_plot.ax1.annotate(describe,xy = source_node,xytext = target_node,xycoords = 'axes fraction',\
                             textcoords = 'axes fraction',arrowprops = arrow_arg,va = 'center',ha = 'center',bbox = nodetype )

    return True
def create_plot():
    fig = plt.figure()
    fig.clf()#清除画布
    # cla()   # Clear axis
    # clf()   # Clear figure
    # close() # Close a figure window
    create_plot.ax1 = plt.subplot(111)
    plot_node('parent node',(0.5,0.1),(0.1,0.5),decide_node)
    #xy表示点的坐标
    #xytext表示注释内容的起始位置
    plot_node('leaf node', (0.8, 0.3), (0.3, 0.8), leaf_node)
    plt.show()

#两个节点之间添加文本
def plot_mid_text(target_node,source_node,node_text):
    x = (source_node[0]-target_node[0])/2 + target_node[0]#想象两个节点，计算两个节点的中间节点
    y = (source_node[1]-target_node[1])/2 + target_node[1]
    create_plot.ax1.text(x,y,node_text)
#逻辑绘制plot_tree
def plot_tree(mTree,source_node,node_text):
    num_leaf = tree.numLeaf(mTree)
    tree_depth = tree.get_tree_depth(mTree)
    # print('决策树为：',mTree)
    # print('当前树深度%d节点数%d'%(num_leaf,tree_depth))

    # target_node文本中心点   source_node 指向文本中心的点
    target_node = (plot_tree.x_off+(1+num_leaf)*(1/2)*(1/plot_tree.totalW),plot_tree.y_off)#根节点的source_node，target_node相同
    plot_mid_text(target_node,source_node,node_text)
    parent_node = list(mTree.keys())[0]
    bo = plot_node(parent_node,target_node,source_node,decide_node)#分类特征，箭头起始位置，箭头指向位置，节点类型
    # print('当前子树根节点是否创建:',bo)
    son_node = mTree[parent_node]
    plot_tree.y_off = plot_tree.y_off  - (1/plot_tree.totalD)#从上往下画
    # print('y轴改变：',plot_tree.y_off)
    for key in son_node.keys():
        if type(son_node[key]) == dict :
            plot_tree(son_node[key],target_node,key)
        else:
            plot_tree.x_off = plot_tree.x_off + (1/plot_tree.totalW)
            boo = plot_node(son_node[key],(plot_tree.x_off,plot_tree.y_off),target_node,leaf_node)#注意这行参数，是以原来的节点为绘制指向的初始节点，新节点坐标已经修改
            # print('叶子节点是否创建：',boo)
            plot_mid_text((plot_tree.x_off,plot_tree.y_off),target_node,key)
    # 深度搜索，在绘制结束一个节点的子节点，返回，所以需要将y_off改变成之前的值
    #由于迭代结束一个特征的属性，因此在for结束之后将y轴坐标还原，而不是在循环中还原
    plot_tree.y_off = plot_tree.y_off + (1/plot_tree.totalD)

#实际绘制决策树图
def create_tree(mTree):
    fig = plt.figure(num='决策树',figsize=(11,7))
    fig.clf()
    create_plot.ax1 = plt.subplot(111,frameon = False)#frameon = True显示图像框架
    plot_tree.totalW = tree.numLeaf(mTree)#叶子节点数
    plot_tree.totalD = tree.get_tree_depth(mTree)#树的深度
    plot_tree.x_off = -0.5/float(plot_tree.totalW)#初始节点坐标
    plot_tree.y_off = 1.0
    plot_tree(mTree,(0.5,1.0),'')
    create_plot.ax1.set_xticks([])
    create_plot.ax1.set_yticks([])
    plt.show()
