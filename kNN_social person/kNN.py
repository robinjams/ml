#encoding=utf-8
import numpy as np
import operator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties#解决显示中文问题
import matplotlib.lines as mlines
def create():
    group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return  group,labels

#文件数据转化为矩阵
def file2matric(filename):
    f = open(filename,'r')
    arr = f.readlines()
    num_row = len(arr)
    returnMatric  = np.zeros((num_row,3))
    labelVictor = []
    index = 0
    for line in arr:
        line = line.strip()
        lineFromline = line.split('\t')
        returnMatric[index,:] = lineFromline[0:3]#index 只是表示第index+1行
        labelVictor.append(int(lineFromline[-1]))#将标签量转化为数字向量
        index +=1
    return returnMatric,labelVictor#返回矩阵和标签向量


#matplotlib绘制数据图
def showdata(returnMatric,returnVictor):
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)  # 找到中文字体
    fig,axs = plt.subplots(2,2,sharey=False,sharex=False,figsize = (12,8))
    numlabel = len(returnVictor)
    colors = []
    for i in returnVictor:
        if i==1:
            colors.append('red')
        elif i==2:
            colors.append('orange')
        elif i==3:
            colors.append('black')
    #绘制图例，由于带有不同的标签，总会一次性绘制出图形，不同类别的图例标签无法表示，通过自己添加空数据类型，分类出实例
    #玩游戏、每周消费的冰激凌数目占比
    axs[0][0].scatter(returnMatric[:, 1], returnMatric[:, 2],c=colors)
    type1 = axs[0][0].scatter([],[],c='red',label = 'didntLike')
    type2 = axs[0][0].scatter([],[], c='orange',label = 'smallDoses')
    type3 = axs[0][0].scatter([],[], c='black',label = 'smallDoses')
    axs[0][0].set_title(u'玩游戏、每周消费的冰激凌数目占比',fontproperties = font_set,color = 'r')
    axs[0][0].set_xlabel(u'玩游戏', fontproperties=font_set,color = 'k')
    axs[0][0].set_ylabel(u'冰激凌数目', fontproperties=font_set,color = 'k')
    # 设置图例
    axs[0][0].legend(handles=[type1, type2, type3], labels=['didntLike', 'smallDoses', 'smallDoses'], loc='upper right')
    #飞行常客里程数与玩游戏
    axs[0][1].scatter(returnMatric[:, 0], returnMatric[:, 1], c=colors)
    axs[0][1].set_title(u'飞行常客里程数与玩游戏占比', fontproperties=font_set, color='r')
    axs[0][1].set_xlabel(u'飞行常客里程数', fontproperties=font_set, color='k')
    axs[0][1].set_ylabel(u'玩游戏', fontproperties=font_set, color='k')
    # 设置图例
    axs[0][1].legend(handles=[type1, type2, type3], labels=['didntLike', 'smallDoses', 'smallDoses'], loc='upper right')
    #飞行常客里程数与冰激凌
    axs[1][0].scatter(returnMatric[:, 0], returnMatric[:, 2], c=colors)
    axs[1][0].set_title(u'飞行常客里程数与冰激凌占比', fontproperties=font_set, color='r')
    axs[1][0].set_xlabel(u'飞行常客里程数', fontproperties=font_set, color='k')
    axs[1][0].set_ylabel(u'冰激凌', fontproperties=font_set, color='k')
    # 设置图例
    axs[1][0].legend(handles=[type1, type2, type3], labels=['didntLike', 'smallDoses', 'smallDoses'], loc='upper right')
    plt.tight_layout()
    plt.show()

#归一化数据
def autoNormal(dataset):
    min = dataset.min(0)
    max = dataset.max(0)
    range = max-min
    m = dataset.shape[0]
    normal = np.zeros(np.shape(dataset))
    #tile(A,reps)参数A是一个数组（多维或一维）
    # rep参数是一个元组，里面有几个数，最右边的数代表A的最深的维度的元素应该重复的次数，往左边一点的数代表A的次深的维度应该重复的次数。
    normal_1 = dataset - np.tile(min,(m,1))
    normal_fin = normal_1/np.tile(range,(m,1))
    return normal_fin,min,range

#分类
def classify(A,dateSet,labels,k):
    dateSize = dateSet.shape[0]
    relation  = np.tile(A,(dateSize,1))-dateSet
    squar = relation**2
    result = (squar.sum(axis=1))**0.5
    sort_re= result.argsort()
    Count = {}
    #只需要统计结果
    for i in range(k):
        vote = labels[sort_re[i]]
        Count[vote] = Count.get(vote,0)+1
    #将统计结果排序,items函数，将一个字典以列表的形式返回，因为字典是无序的，所以返回的列表也是无序的。
    final = sorted(Count.items(),key=operator.itemgetter(1),reverse=True)
    return final[0][0]#获取具体的某个分类

#对于输入数据进行分类测试，得到错误率
def data_classify_test():
    ratio = 0.1
    returnmatric,returnvictor = file2matric('datingTestSet2.txt')
    normal,min,range = autoNormal(returnmatric)
    m = normal.shape[0]
    errorCount = 0
    num = int(m*ratio)
    for i in np.arange(num):#int数据不能迭代
        classify_result = classify(normal[i,:],normal[num:m,:],returnvictor[num:m],3)#调用分类器
        # print('classifier get\'s result is: %d,And real character is %d\n'\
        #       % (classify_result,returnvictor[i]))
        if (classify_result != returnvictor[i]):
            errorCount +=1
    print('classifier error ratio is:%f' %(errorCount/float(num)))#错误率表示错误数除以总数

#用户具体输入某一个人，从而判断出这个人属于的类别
def classify_person():
    result = ['hate','just soso','fatastic']
    plane = float(input('plan spend on distance：'))
    ice_cream = float(input('ice cream eat number ：'))
    game = float(input('video&game spend on time:'))
    returnmatric, returnvictor = file2matric('datingTestSet2.txt')
    normal, min, range = autoNormal(returnmatric)
    person = [plane,game,ice_cream]
    result_number = classify((person-min)/range,normal,returnvictor,3)
    if result_number==3:
        result = 'fatastic'
    elif result_number==2:
        result='just soso'
    elif result_number==1:
        result='hate'
    print('System judge the person belong: %s'%result)