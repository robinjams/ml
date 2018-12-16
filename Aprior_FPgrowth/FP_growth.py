#encoding:utf-8_*_
#author：@robin
#create time：2018/11/29 8:54
#file：FP_growth.py
#IDE:PyCharm
import numpy as np
class TreeNode:
    def __init__(self,name,numOccure,parentID):
        self.name = name
        self.count = numOccure
        self.NodeLink=None
        self.parentID = parentID
        self.children = {}
    def inc(self,numOccure):
        self.count += numOccure
    def display(self,ind=1):
        name = self.name
        print(' '*ind,self.name,'--',self.count)#'luo'*5 把文本输出对应的次数
        for chid in self.children.values():
            chid.display(ind+1)
def createTree(dataSet,minsupport):
    from  operator import itemgetter,attrgetter
    headerTable = {}
    for tranction in dataSet:
        for item in tranction:
            headerTable[item] = headerTable.get(item,0)+dataSet[tranction]#字典{item:个数}

    for item in list(headerTable.keys()):
        if headerTable[item]<minsupport:
            del (headerTable[item])
    frequence = set(headerTable.keys())
    if len(frequence)==0:
        return None,None
    retTree = TreeNode('null_set',1,None)
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]#{'a':1}----扩展字典---->{‘a’:[1,None]}
    #针对每一个项目集产生一条路径
    for data,count in dataSet.items():
        # print('data',data)
        localD = {}
        for item in data:
            if item in frequence:
                localD[item] = headerTable[item][0]#产生每个项目集字典：item:个数
        if len(localD)>0:
            orderItem = [v[0 ] for v in sorted(localD.items(),key=itemgetter(1),reverse=True)]#对于每一个项目集重新排序
            # print('order',orderItem)
            updateTree(orderItem,count,headerTable,retTree)
            # print(retTree.display())#每一个项目集结束之后，展示当前生成的fp-growth树
    return retTree,headerTable
def updateTree(orderItem,count,headerTable,retTree):
    if orderItem[0] in retTree.children:
        retTree.children[orderItem[0]].inc(count)
    else:
        retTree.children[orderItem[0]] = TreeNode(orderItem[0],1,retTree)
    #添加新节点后才需要更新链表索引，对于相同的节点，更新nodeLink（索引），在同一个节点遇到第三次的时候会出现死循环
    # if headerTable[orderItem[0]][1] == None:
    #     headerTable[orderItem[0]][1] = retTree.children[orderItem[0]]
    #     print(orderItem[0], '---', headerTable[orderItem[0]])
    # else:
    #     print('robin')
    #     update(headerTable[orderItem[0]][1], retTree.children[orderItem[0]])
        if headerTable[orderItem[0]][1] == None:
            headerTable[orderItem[0]][1] = retTree.children[orderItem[0]]
            # print(orderItem[0], '---', headerTable[orderItem[0]])
        else:
            update(headerTable[orderItem[0]][1], retTree.children[orderItem[0]])
    if len(orderItem)>1:
        #添加下一个节点
        updateTree(orderItem[1::],count,headerTable,retTree.children[orderItem[0]])#orderItem[1::]从第一个元素开始获取所有，步长为1
#链表添加结尾元素
def update(node,target):

    while (node.NodeLink is not None):
        node = node.NodeLink
    node.NodeLink = target#最终在headerTable中保存链表最后一个节点位置
def loadData():
    #对于商品种类，默认忽略每一件商品的个数，而是去发现商品是否出现
    data = [
        ['x','y','z','a','a'],
        ['f','t','x','e','m'],
        ['c'],
        ['l','y','z','r','a'],
        ['o','q','z','z','m'],
        # ['r', 'z', 'h', 'j', 'p'],
        #  ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
        #  ['z'],
        #  ['r', 'x', 'n', 'o', 's'],
        #  ['y', 'r', 'x', 'z', 'q', 't', 'p'],
        #  ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']


    ]
    return data
def get_data(data):
    dataDic = {}
    for item in data:
        dataDic[frozenset(item)] = 1
    return dataDic


#搜寻叶节点到根节点的路径
def ascanf_tree(leftnode,prefixpath):

    while leftnode.parentID is not None:
        # print('leftnode name',leftnode.name)
        prefixpath += '-'+(leftnode.name)
        leftnode = leftnode.parentID
    return prefixpath
        # ascanf_tree(leftnode.parentID,prefixpath)
#给定某个特定元素，查找所有路径
def get_prefixpath(basepath,treeNode):
    import re
    catP = {}
    while treeNode!=None:
        prefixpath = ""
        # print(treeNode.count)
        original = treeNode.count
        prefixpath=ascanf_tree(treeNode,prefixpath)
        prefixpath  = re.split('[-]',prefixpath)

        if len(prefixpath)>2:
            #字典的key不支持不可hash的类型：list、set:可变类型TypeError: unhashable type: 'set'
            #           支持可hash类型:tuple,frozenset:不可变类型
            catP[frozenset(prefixpath[2:])] = original
        treeNode = treeNode.NodeLink
    return catP
def sort_min(header):
    key = [];value = []
    for val  in header.items():
        key.append(val[0])
        value.append(val[1])


#递归查找频繁项集
def mineTree(retTree,headerTable,minsupport,prefix,freItem):
    bigL = [ v[0] for v in sorted(headerTable.items(),key=lambda p:str(p[1]))]
    for item in bigL:
        # print('item:',item)
        newFre = prefix.copy()
        newFre.append(item)#保存当前元素商品
        freItem.append(newFre)#用来统计所有的频繁集
        catP = get_prefixpath(item,headerTable[item][1])
        conditionTree,conditionHead = createTree(catP,minsupport)#创建生成fp子树
        if conditionTree==None:
            print('no fp-tree')
        else:
            print('display',conditionTree.display())
        # print('conditionHead',conditionHead)
        if conditionHead !=None:#如果树中还有元素，继续迭代
            mineTree(conditionTree,conditionHead,minsupport,newFre,freItem)
    return freItem

if __name__=='__main__':
    #产生节点测试
    # rootnode = TreeNode('vegtables',9,None)
    # rootnode.children['potato']= TreeNode('potatp',3,None)
    # rootnode.display()
    # data = {frozenset([1,2,3]):1,frozenset([1]):2}
    #产生数据测试
    formatdata = get_data(loadData())
    retTree,headerTable = createTree(formatdata,2)
    print('headerTable',headerTable)
    print('display',retTree.display())
    #测试产生条件模式集
    # catP = get_prefixpath('x',headerTable['x'][1])
    # print('a\'s condition pattern set:',catP)
    freItem = []
    freItem = mineTree(retTree,headerTable,2,prefix=[],freItem=[])
    print('last freItem',freItem)