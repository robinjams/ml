#encoding:utf-8_*_
#author：@robin
#create time：2018/11/22 20:22
#file：Kmeans.py
#IDE:PyCharm
import numpy as np
import random
def loadfile(filename):
    dataMat = []
    with open(filename) as fr:
        for line in fr.readlines():

            # temp = []
            # array = line.strip().split('\t')
            # for content in array:
            #     temp.append(float(content))

            array = line.strip().split('\t')
            temp = list(map(float,array))

            dataMat.append(temp)
    return dataMat
def distCaculate(VecA,VecB):
    # print('test distance',np.sqrt(np.sum(np.power((VecA-VecB),2))))
    return np.sqrt(np.sum(np.power((VecA-VecB),2)))
def centrios(dataSet,k):
    n = np.shape(dataSet)[1]
    cen = np.mat(np.zeros((k,n)))
    for i in range(n):
        minI = min(dataSet[:,i])
        rangeI = max(dataSet[:,i])-minI
        cen[:,i] = minI + np.multiply( rangeI , np.random.rand(k,1))
    return cen
def kmean(dataSet,k,distMeas = distCaculate,Createcent = centrios):
    np.set_printoptions(suppress=True)#解决用科学计数法显示
    m = np.shape(dataSet)[0]
    storge = np.mat(np.zeros((m,2)))
    cent = Createcent(dataSet,k)
    cluterchanged = True
    while cluterchanged:
        cluterchanged = False
        for i in range(m):
            mindist = np.inf;minIndex = -1
            for j in range(k):
                # print('cent',cent[j,:])
                # print('data',dataSet[i,:])
                dis  = distMeas(cent[j,:],dataSet[i,:])
                if dis<mindist:
                    mindist = dis
                    minIndex = j
            #在计算每一个样本点与质心的距离后，只要有一个样本点修改了所属的簇，则继续迭代，直到所有样本点都属于固定簇
            if storge[i,0]!=minIndex:cluterchanged=True
            storge[i,:] = minIndex,mindist**2
            # print(storge[i,:])
        print('centrois:',cent)
        for c in range(k):
            point = dataSet[np.nonzero(storge[:,0]==c)[0]]
            cent[c,:] = np.mean(point,axis=0)
    return cent,storge
#书中代码
def kMeans(dataSet, k, distMeas=distCaculate, createCent=centrios):
    m = np.shape(dataSet)[0]
    clusterAssment = np.mat(np.zeros((m,2)))#create mat to assign data points
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = np.inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print('centroids',centroids)
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[np.nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = np.mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment
def biKmeans(dataSet, k, distMeas=distCaculate):
    m = np.shape(dataSet)[0]
    clusterAssment = np.mat(np.zeros((m,2)))
    centroid0 = np.mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #create a list with one centroid
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(np.mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE = np.inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[np.nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
            sseNotSplit = sum(clusterAssment[np.nonzero(clusterAssment[:,0].A!=i)[0],1])
            # print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[np.nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[np.nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        # print 'the bestCentToSplit is: ',bestCentToSplit
        # print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[np.nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
    return np.mat(centList), clusterAssment
#二分均值聚类算法
#自我总结：该算法理论上会达到全局最小，但是聚类的效果并没有理想中那么好
def biKmeans(dataSet,k,distMeas = distCaculate):
    m = np.shape(dataSet)[0]
    storge = np.mat(np.zeros((m,2)))
    centrios0 = np.mean(dataSet,axis=0)
    # print(type(centrios0))
    cenlist = [centrios0]
    for j in range(m):
        storge[j,1] = distMeas(centrios0,dataSet[j,:])
    # print(storge)
    i = 0
    while len(cenlist)<k:
        print('iter',i)
        i = i+1
        lowSSE = np.inf
        for i in range(len(cenlist)):
            point = dataSet[np.nonzero(storge[:,0]==i)[0]]
            cent,stor = kmean(point,2,distMeas)
            splite_SSE = np.sum(stor[:,1])
            splite_no_SSE = np.sum(storge[np.nonzero(storge[:,0]==i)[0],1])
            new_SSE = splite_SSE + splite_no_SSE
            if new_SSE<lowSSE:
                bestIndex = i
                lowSSE = new_SSE
                bestCentrois = cent
                bestStor = stor.copy()
        #修改对应的簇索引
        bestStor[np.nonzero(bestStor[:,0]==1)[0],0]=len(cenlist)
        bestStor[np.nonzero(bestStor[:,0]==0)[0],0]=bestIndex
        print('bestSplit:%d'%bestIndex)
        print('split length',len(bestStor))
        # print('split centrois',bestCentrois)
        # print('stor',stor)
        #在存储质点的list中添加划分后的质点
        cenlist[bestIndex] = bestCentrois[0,:]
        cenlist.append(bestCentrois[1,:])
        #更新数据
        storge[np.nonzero(storge[:,0]==bestIndex)[0]] = bestStor
    return cenlist,storge

def plot(dataSet,centrois,storge):
    import  matplotlib.pyplot as plt
    m = np.shape(dataSet)[0]
    one = [];two=[];three = [];four = []
    #TypeError: list indices must be integers or slices, not tuple一般是针对list使用了切片，可以转化为array
    dataSet = np.array(dataSet)
    for i in range(m):
        cluter = storge[i,0]
        if(cluter==0.0):
            one.append(dataSet[i,:]);continue
        elif(cluter==1.0):
            two.append(dataSet[i,:]);continue
        elif (cluter == 2.0):
            three.append(dataSet[i, :]);continue
        elif (cluter == 3.0):
            four.append(dataSet[i, :])
    x_one_cord = [x[0] for x in one];x_two_cord = [x[0] for x in two]
    x_three_cord = [x[0] for x in three];x_four_cord = [x[0] for x in four]
    y_one_cord = [x[1] for x in one];y_two_cord = [x[1] for x in two]
    y_three_cord = [x[1] for x in three];y_four_cord = [x[1] for x in four]

    # print('one',one)
    # print('test get one cloumn:',x_one_cord)
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    #测试生成的数据
    # all_xcord = dataSet[:,0];all_ycord = dataSet[:,1]
    # print('all_xcord',all_xcord)
    # ax.scatter(all_xcord,all_ycord,marker='x',color='g',label='one',s=30)
    #质点数据
    # x_centrois = [ x[0] for x in np.array(centrois)]
    # y_centrois = [x[1] for x in np.array(centrois)]
    # ax.scatter(x_centrois,y_centrois,marker='x',color='black',label='controis',s=45)
    ax.scatter(x_one_cord,y_one_cord,marker='x',color='g',label='one',s=30)
    ax.scatter(x_two_cord,y_two_cord,marker='+',color='b',label='two',s=30)
    ax.scatter(x_three_cord,y_three_cord,marker='^',color='r',label='three',s=30)
    ax.scatter(x_four_cord,y_four_cord,marker='*',color='c',label='four',s=30)
    plt.title('kmeans figure')
    plt.show()






if __name__=='__main__':
    # data = loadfile('testSet.txt')
    # dataMat = np.mat(data)
    # centrois = centrios(dataMat,6)
    # print(centrois)

    #验证中心点是否正确
    # print(min(dataMat[:,0]))
    # print(max(dataMat[:,0]))
    # print(min(dataMat[:,1]))
    # print(max(dataMat[:,1]))

    #kmeans在数据集上运行
    # dis = distCaculate(dataMat[0],dataMat[1])
    # print('distance',dis)
    # centrois,storge  = kmean(dataMat,4)
    # print('centrois',centrois)
    # print('storge',storge)

    #绘制散点图
    # plot(data,centrois,storge)

    data = loadfile('testSet2.txt')
    dataMat = np.mat(data)
    #2均值聚类算法
    centlist,storge = biKmeans(dataMat,3)
    # print('centlist',centlist)
    # print('storge',storge)
    plot(data,centlist,storge)





