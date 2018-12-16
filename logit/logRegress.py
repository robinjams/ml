#encoding:utf-8_*_
#author：@robin
#create time：2018/8/22 15:36
#file：logRegress.py
#IDE:PyCharm
import numpy as np
import math
def loadDataSet():
    dataMatric = [];datalabel = []
    with open('testSet.txt') as fp:
        for line in fp.readlines():
            data = line.strip().split()
            dataMatric.append([1.0,float(data[0]),float(data[1])])
            datalabel.append(int(data[2]))
    return  dataMatric,datalabel
def sigmoid(inx):
    # return 1/(1+np.exp(-inx))
    # numpy.exp 返回值在 float64 中存储不下，会截取一部分，给的是个warning，不影响最终结果。如果想存储，可以使用 bigfloat
    return 1/(1+np.exp(-inx))

#梯度上升算法
def grad_ascend(matric_in,label_in):
    mat = np.mat(matric_in)
    mat_label = np.mat(label_in).transpose()
    alpha = 0.01
    maxCount = 1000
    m,n = np.shape(mat)
    weight = np.ones((n,1))
    for i in range(maxCount):
        h = sigmoid(mat * weight)#模型预测值
        # print(h)
        error = mat_label - h #预测值与真实值之间的误差
        weight = weight + alpha * (np.transpose(mat) * error) #交叉熵对所有参数的偏导
    return weight
#随机梯度上升，而不梯度上升，优势：不需要去处理所有数据
def stoGradAscend( matric, label ):
    import math
    alpha = 0.01
    count = 500
    m,n = np.shape(matric)
    weight = np.ones(n)#3*1
    for i in range(m):
        predictor = sigmoid(sum(matric * weight))#1*3 3*1
        # print(predictor)
        error = label[i] - predictor
        weight = weight + alpha * error * matric[i]
    return weight
#改进随机梯度上升，优势：1、随机进行权重的计算2、增加迭代次数
def stoGradAscend_imporve( matric, label, num=150 ):
    import random
    for j in range(num):
        m, n = np.shape(matric)
        dataIndex = list(range(m))
        weight = np.ones(n)  # 3*1
        for i in range(m):
            alpha = 3/ (1 + j + i) + 0.01
            randomIndex = int(random.uniform(0,len(dataIndex)))
            # print(randomIndex)
            predictor = sigmoid(sum(matric[randomIndex] * weight))  # 1*3 3*1
            # print(predictor)
            error = label[randomIndex] - predictor
            #遇到TypeError numpy.float64 object cannot be interpreted as anindex，使用dot()代替*
            weight = weight + alpha * np.dot(error, matric[randomIndex])
            #TypeError: 'range' object doesn't support item deletion
            #range不返回数组对象，而是返回range对象
            # del(dataIndex[randomIndex])#del删除的是变量，而不是实际的数值
            #解决方案：
            del (dataIndex[randomIndex])
    return weight

#绘制样本点，和决策曲线
def plotfit(wei):
    from matplotlib import pyplot   as plt
    weight = wei.getA()#将矩阵能够转化为数组
    matric, label = loadDataSet()
    # print(matric[:5])
    n = np.shape(matric)[0]  # 第0维度
    xcord1 = [];ycord1 = []
    xcord2 = [];ycord2 = []
    arr = np.array(matric)
    # print( n )
    for i in range(n):
        if int(label[i]) == 1:
            xcord1.append(arr[i, 1])
            ycord1.append(arr[i, 2])
        else:
            xcord2.append(arr[i, 1])
            ycord2.append(arr[i, 2])
    # print(xcord1[:5])
    # 获取数组对应元素（没用，只是为了知道xcord1.append(arr[i, 1])）
    arr2 = np.array(
        [[1, 2, 3], [2, 3, 4], [3, 5, 6], ])
    # print(arr2[2,2])
    plt.figure(num="拟合曲线")
    ax = plt.subplot( 1,1,1 )
    ax.scatter( xcord1, ycord1, c='red' )
    ax.scatter(xcord2, ycord2, c='blue')
    #给出拟合曲线的范围
    x = np.arange(-3.0,3.0,0.1)
    y = ( -weight[0] - weight[1]*x)/weight[2]

    ax.plot(x,y)
    plt.show()
#病马生死的预测
def classyVetor( index, weight):
    prop = sigmoid(sum( index * weight ))
    if prop >0.5 :
        return 1
    else:
        return 0
def colicTest():
    frtrain = open('horseColicTraining.txt')
    frtest = open('horseColicTest.txt')
    train = []; label = []
    for line in frtrain.readlines():
        linearr = []
        temp = line.strip().split('\t')
        for i in range(21):
            linearr.append( float(temp[i]) )#不能使用extend来添加，会将特征值全部转化为单个字节
        train.append( linearr )
        label.append( float(temp[21]) )
    weight = stoGradAscend_imporve( train, label, num=150 )
    # print(weight)
    numtest = 0; error = 0
    for line in frtest.readlines():
        numtest += 1
        linearr = []
        temp = line.strip().split('\t')
        for i in range(21):
            linearr.append(float(temp[i]))  # 不能使用extend来添加，会将特征值全部转化为单个字节
        if int(classyVetor( linearr, weight )) != int(temp[21]):#一定要注意是转化为int类型
            error += 1;
    errorprop = float(error/numtest)
    return errorprop
def mutiTest():
    sumprop = 0; numTest = 10
    for i in range(numTest):
        print('第%d错误率为%f' %( i, colicTest()))
        sumprop += colicTest();
    print('测试次数 %d 次，错误率为 %f' %( numTest, float(sumprop/numTest))  )

if __name__=='__main__':
    matric,label = loadDataSet()
    # print(matric[:5])
    # print(label[:5])

    #梯度上升训练后得到权重
    w_G = grad_ascend( matric, label )
    w = stoGradAscend( matric, label )
    #数组与矩阵之间转换，否则会报np.narray没有属性getA()
    w_SG = np.mat(w.reshape((3,1)))#随机梯度上升
    w_i = stoGradAscend_imporve( matric, label, num=100)
    w_SG_i = np.mat(w_i.reshape((3,1)))#改进后的权重
    print('梯度得到的数据权重：\n',w_G)
    print('随机梯度得到的数据权重：\n', w_SG)
    print('随机梯度改进得到的数据权重：\n', w_SG_i)
    # plotfit(w_G)#绘制梯度拟合曲线
    # plotfit(w_SG_i)#绘制随机梯度上升拟合曲线

    #测试了不同新建方式的差别
    # print(np.ones(3))
    # print(np.ones((3,1)))

    #测试训练得到的权重
    print('错误率：%f' %float(colicTest()))
    #多个测试求平均值
    mutiTest()
