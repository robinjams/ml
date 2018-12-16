#encoding:utf-8_*_
#author：@robin
#create time：2018/11/20 8:32
#file：compare_models.py
#IDE:PyCharm
import numpy as np
import regression_Tree.CART_tree as cart
#regression Tree & model Tree predict
#regression Tree
def regTreeEvalue(model,indata):
    return float(model)
#model tree
def modelTreeEvalue(model,indata):
    n = np.shape(indata)[1]
    x = np.mat(np.ones((1,n+1)))#传参一般是通过元组的形式
    x[:,1:n+1] = indata
    return float(x*model)
def TreeForCast(tree,indata,modelEvalue = regTreeEvalue):
    if not cart.istree(tree): return modelEvalue(tree,indata)

    if(indata[tree['splitfeature']]>tree['val']):
        if cart.istree(tree):
            return TreeForCast(tree['ltree'],indata,modelEvalue)
        else:
            return modelEvalue(tree['ltree'],indata)
    else:
        if cart.istree(tree):
            return TreeForCast(tree['rtree'],indata,modelEvalue)
        else:
            return modelEvalue(tree['rtree'],indata)
def createForCast(tree,testdata,modelEvalue=regTreeEvalue):
    m = np.shape(testdata)[0]
    y = np.mat(np.zeros((m,1)))
    for i in range(m):
        y[i,0] = TreeForCast(tree,np.mat(testdata[i]),modelEvalue)
    return y
if __name__=='__main__':

    # #回归树
    train = np.mat(cart.loadData('bikeSpeedVsIq_test.txt'))
    test = np.mat(cart.loadData('bikeSpeedVsIq_train.txt'))
    regTree = cart.createTree(train,ops=(1,20))
    yHat = createForCast(regTree,test[:,0])
    #使用hstack()堆叠
    x = np.vstack((np.hstack(yHat),np.hstack(test[:,1])))
    # 出错代码x = np.vstack(np.hstack(yHat),np.hstack(test[:,1]))#TypeError: vstack() takes 1 positional argument but 2 were given 以元组的形式传入参数（（a,b））而不是（a,b）
    # print('堆叠后的矩阵:',x)
    corr = np.corrcoef(yHat,test[:,1],rowvar=0)#计算同一个相关系数，不同的写法（一）
    corr1 = np.corrcoef(x)#计算同一个相关系数，不同的写法（er）
    print('regTree corrcoef:\n',corr1)

    #模型树
    modelTree = cart.createTree(train,cart.modelLeaf,cart.modelError,ops=(1,20))
    yHat_model = createForCast(modelTree,test[:,0],modelTreeEvalue)
    x = np.vstack((np.hstack(yHat_model),np.hstack(test[:,1])))
    corr_model = np.corrcoef(x)#计算同一个相关系数，不同的写法（er）
    print('modelTree corrcoef:\n',corr_model)

    #标准回归
    ws,x,y = cart.linear(train)
    m_test = np.shape(test)[0]
    yHat_stard = np.mat(np.zeros((m_test,1)))
    for i in range(m_test):
        yHat_stard[i] = test[i,0]*ws[1,0]+ws[0,0]
    # print(yHat_stard)
    x = np.vstack((np.hstack(yHat_stard), np.hstack(test[:, 1])))
    corr_stand = np.corrcoef(x)  # 计算同一个相关系数，不同的写法（er）
    print('corr_stand corrcoef:\n', corr_stand)