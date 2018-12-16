#encoding:utf-8_*_
#author：@robin
#create time：2018/11/16 11:04
#file：plot.py
#IDE:PyCharm
import numpy as np
from graphviz import Digraph
import os
from collections import OrderedDict
import uuid
import regression_Tree.CART_tree as cart
def sort(dict):
    row  = ['splitfeature','val','rtree','ltree']
    sortedDict = OrderedDict()
    for key in row:
        if dict.get(key) is not None:
            sortedDict[key] = dict.get(key)
    # print(sortedDict)
    return sortedDict
# 字典转化为nodes和edges
def get_nodes_edges(tree,root_node=None,nodes=[],edges=[]):
    #make the dictionary sorted
    if type(tree).__name__!='OrderedDict':
        print(tree)
        return [],[]
    if root_node==None:
        keys = tree.keys()
        label = str(tree.get('splitfeature'))+'\n'+str(tree.get('val'))
        root_node = (uuid.uuid4(),label)
    nodes.append(root_node)
    if type(tree['ltree']).__name__=='dict' and type(tree['rtree']).__name__=='dict':
        for sub_tree in [tree['ltree'],tree['rtree']]:
            label = str(tree.get('splitfeature'))+'\n'+str(tree.get('val'))
            sub_node = (uuid.uuid4(),label)
            edge = (root_node,sub_node,'edge')
            nodes.append(sub_node)
            edges.append(edge)
            sub_node, sub_edge = get_nodes_edges(sort(sub_tree), sub_node, nodes, edges)

        return nodes, edges
    elif(type(tree['ltree']).__name__!='dict' and type(tree['rtree']).__name__!='dict'):
        for sub_tree in [tree['ltree'], tree['rtree']]:
            label = sub_tree
            sub_node = (uuid.uuid4(), label)
            edge = (root_node, sub_node, 'edge')
            nodes.append(sub_node)
            edges.append(edge)
        return nodes,edges
    elif ((type(tree['ltree']).__name__=='dict' and type(tree['rtree']).__name__!='dict')):
            label = str(tree['ltree'].get('splitfeature'))+'\n'+str(tree['ltree'].get('val'))
            sub_node = (uuid.uuid4(),label)
            edge = (root_node,sub_node,'edge')
            nodes.append(sub_node)
            edges.append(edge)
            sub_node, sub_edge = get_nodes_edges(sort(tree['ltree']), sub_node, nodes, edges)
            label = tree['rtree']
            sub_node = (uuid.uuid4(), label)
            edge = (root_node, sub_node, 'edge')
            nodes.append(sub_node)
            edges.append(edge)
            return nodes, edges
    elif ((type(tree['ltree']).__name__!='dict' and type(tree['rtree']).__name__=='dict')):
            label = str(tree['rtree'].get('splitfeature'))+'\n'+str(tree['rtree'].get('val'))
            sub_node = (uuid.uuid4(),label)
            edge = (root_node,sub_node,'edge')
            nodes.append(sub_node)
            edges.append(edge)
            sub_node, sub_edge = get_nodes_edges(sort(tree['rtree']), sub_node, nodes, edges)
            label = tree['ltree']
            sub_node = (uuid.uuid4(), label)
            edge = (root_node, sub_node, 'edge')
            nodes.append(sub_node)
            edges.append(edge)
            return nodes, edges
def getEdge(edges):
    result = []
    for edge in edges:
        if(type(edge)is tuple):
            result.append(result)
    return result
def dot_decision(nodes,edges):
    content = 'digraph decision_tree {\n'
    for node in nodes:
        if(node==[]):
            print(node)
            continue
        content +='"{}"[label="{}"];\n'.format(node[0],node[1])
    for edge in edges:
        content += '"{}"->"{}"[labbel="{}"];\n'.format(edge[0],edge[1],edge[2])
    content += '}'
    return content

if __name__=='__main__':
    os.environ["PATH"] += os.pathsep + 'F:/Python/graphaviz/graphviz-2.38/release/bin/'
    data = cart.loadData('ex2test.txt')
    dataMat = np.mat(data)
    regtree3 = cart.createTree(dataMat, ops=(0, 1))
    sortedTree = sort(regtree3)
    nodes = [];
    edges = []
    nodes, edges = get_nodes_edges(sortedTree, nodes, edges)
    # 获取edges的值
    result = []
    last = getEdge(edges)
    ##生成dot
    # print(nodes)
    content = dot_decision(nodes, last)
    # print(content)
    with open('decision_figure.dot', 'w') as f:
        content = dot_decision(nodes, edges)
        f.write(content)
        # #dot -Tgif decision_figure.dot -o decision_figure.gif生成gif



    #后剪枝策略
    regree3prune = cart.prune(regtree3,dataMat)
    sortedTreePrune = sort(regree3prune)
    # print('later prune:\n',regree3prune)
    nodes = [];
    edges = []
    nodes, edges = get_nodes_edges(sortedTreePrune, nodes, edges)
    #获取edges的值
    result = []
    last = getEdge(edges)
    ##生成dot
    # print(nodes)
    content = dot_decision(nodes,last)
    # print(content)
    with open('decision_prune_figure.dot','w') as f:
        content = dot_decision(nodes, edges)
        f.write(content)
    # #dot -Tgif decision_prune_figure.dot -o decision_prune_figure.gif生成gif



