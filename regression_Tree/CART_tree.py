#encoding:utf-8_*_
#author：@robin
#create time：2018/11/13 20:30
#file：CART_tree.py
#IDE:PyCharm
import numpy as np
def loadData(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        content = line.strip().split('\t')
        temp = []
        for con in content:
            # data = map(lambda x:float(x),content)#映射函数，将具体的一个list通过一个函数转化
            temp.append(float(con))
        dataMat.append(temp)
    return dataMat
def bindSplit(dataMat,feature,val):
    mat0 = dataMat[np.nonzero(dataMat[:,feature]>val)[0],:]#np.nonzero(dataMat[:,feature]>val)[0]找到非零的行索引
    mat1 = dataMat[np.nonzero(dataMat[:,feature]<=val)[0],:]
    return mat0,mat1
def regLeaf(dataMat):
    return np.mean(dataMat[:,-1])
def regtype(dataMat):
    return np.var(dataMat[:,-1]) * np.shape(dataMat)[0]
def choooseBestSplit(dataMat,leaftype,errortype,ops):
    tolS = ops[0];tolN = ops[1]
    if len(set(dataMat[:,-1].T.tolist()[0])) == 1:
        return None,leaftype(dataMat)
    m,n = np.shape(dataMat)
    S = errortype(dataMat)
    bestS = np.inf;bestfeature = 0;bestVal = 0
    for feat in range(n-1):
        # print(dataMat[:,feat].T.tolist()[0])
        for feature_val in set(dataMat[:,feat].T.tolist()[0]):
            mat0,mat1 = bindSplit(dataMat,feat,feature_val)
            if (np.shape(mat0)[0]<tolN) or (np.shape(mat1)[0]<tolN):
                continue
            error = errortype(mat0) + errortype(mat1)
            if error<bestS:
                bestS = error
                bestfeature = feat
                bestVal = feature_val
    mat0, mat1 = bindSplit(dataMat, bestfeature, bestVal)
    if S - bestS < tolS:
        return None,leaftype(dataMat)
    if (np.shape(mat0)[0] < tolN) or (np.shape(mat1)[0]<tolN):
        return None,leaftype(dataMat)
    return bestfeature,bestVal
#创建回归树，等待添加
def createTree(dataMat,leaftype = regLeaf,errortype = regtype,ops = (1,4)):
# def createTree(dataMat,leaftype = regLeaf,errortype = regtype,ops = (0,1)):#构造的树过于臃肿
    feature,val = choooseBestSplit(dataMat,leaftype,errortype,ops)
    if feature==None:return val
    regTree = {}
    regTree['splitfeature'] = feature
    regTree['val'] = val
    lset,rset = bindSplit(dataMat,feature,val)
    # print(lset)
    # print('-----------------------\n',rset)
    regTree['ltree'] = createTree(lset,leaftype,errortype,ops)
    regTree['rtree'] = createTree(rset,leaftype,errortype,ops)
    return regTree
def istree(obj):
    return type(obj).__name__=='dict'
def getMean(tree):
    if (istree(tree['ltree'])):
        tree['ltree'] = getMean(tree['ltree'])
    if (istree(tree['rtree'])):
        tree['rtree'] = getMean(tree['rtree'])
    return (tree['rtree']+tree['ltree'])/2
# 后剪枝算法，错误率降低算法，reduced-error pruning
def prune(tree,testData):
    # 如果没有测试数据直接进行塌陷处理
    if (np.shape(testData)[0]==0):
        return getMean(tree)
    if (istree(tree['ltree']) or istree(tree['rtree'])):
        lset,rset= bindSplit(testData,tree['splitfeature'],tree['val'])
        if istree(tree['ltree']):
            tree['ltree'] = prune(tree['ltree'],lset)
        if istree(tree['rtree']):
            tree['rtree'] = prune(tree['rtree'],rset)
    if not istree(tree['ltree']) and not istree(tree['rtree']):
        lset,rset= bindSplit(testData,tree['splitfeature'],tree['val'])
        # print(lset[:,-1]-tree['ltree'])
        # print(rset)
        errorNomerge = sum(np.power(lset[:,-1] - tree['ltree'],2))+\
                        sum(np.power(rset[:,-1]-  tree['rtree'],2))
        treeMean = (tree['ltree'] + tree['rtree'])/2
        errorMerge = sum(np.power(testData[:,-1]-treeMean,2))
        if errorNomerge<errorMerge:
            print('merging')
            return errorMerge
        else:
            return tree
    else:
        return tree#左右为非叶子节点，返回树
# 模型树的叶节点生成函数
def linear(dataSet):
    dataMat = np.mat(dataSet)
    m,n = np.shape(dataMat)
    x = np.mat(np.ones((m,n)));y =np.mat(np.ones((m,1)))
    #add cloumn is 1,intend to satisfy w.T * x + b, b's initial weight = 1
    x[:,1:n] = dataSet[:,0:n-1];y = dataSet[:,-1]
    xTx = x.T*x
    if np.linalg.det(xTx)==0.0:
        print('the matric is singuar ,not invert')
    ws = xTx.I * (x.T * y)
    return ws ,x,y
def modelLeaf(dataSet):
    ws,x,y = linear(dataSet)
    return ws
def modelError(dataSet):
    ws,x,y = linear(dataSet)
    y_predict = x * ws
    return sum(np.power(y_predict - y,2))

if __name__=='__main__':
    # #test ex00.txt data
    # data = loadData('ex00.txt')
    # dataMat = np.mat(data)
    # regree = createTree(dataMat)
    # print(' ex00.txt regree:\n',regree)

    #test ex0.txt data
    # data = loadData('ex0.txt')
    # dataMat = np.mat(data)
    # regree2 = createTree(dataMat)
    # print('ex0.txt retree:\n',regree2)

    # test ex0.txt data
    # data = loadData('ex2test.txt')
    # dataMat = np.mat(data)
    # regree3 = createTree(dataMat,ops=(0,1))
    # # print('ex0.txt retree:\n', regree3)
    # regree3prune = prune(regree3,dataMat)
    # print('later prune:\n',regree3prune)

    #exp2.txt data construct linear model tree
    data = loadData('exp2.txt')
    dataMat = np.mat(data)
    retree4 = createTree(dataMat,modelLeaf,modelError,ops=(1,10))
    print('exp2:\n',retree4)



