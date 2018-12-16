#encoding:utf-8_*_
#author：@robin
#create time：2018/11/27 11:27
#file：aprior.py
#IDE:PyCharm
import numpy as np
def loaddata():
    return [[1,2],[1,2,4],[3,4],[1,2,3],[2,3,5],[3,4,5,6]]
def createC1(dataSet):
    c1 = []
    for tranction in dataSet:
        for item in tranction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    return list(map(frozenset,c1))
def scanD(D,Ck,minsupport):
    scount = {}
    for tid in D:
        for  can in Ck:
            if can.issubset(tid):
                if not can in scount:
                    scount[can] = 1
                else:
                    scount[can] = scount.get(can)+1
    supportData = {}#频繁集支持度字典{频繁集：支持度}
    retList = []#支持度大于阈值
    for i in scount:
        support= scount[i]/(len(D))
        if support >= minsupport:
            retList.insert(0,i)
        supportData[i] = support
    return retList,supportData
def aprior_gen(Lk,n):#产生n个频繁项集{1,2} n=2
    retList = []
    count = len(Lk)
    for i in range(count):
        for j in range(i+1,count):
            L1 = list(Lk[i])[:n-2];L2 = list(Lk[j])[:n-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList
def aprior(dataset,minsupport=0.5):
    c1 = createC1(dataset)
    D = list(map(set,dataset))
    L1,supportData = scanD(D,c1,minsupport)
    all_L = [L1]
    k = 2
    while len(all_L[k-2])>0:
        Ck = aprior_gen(all_L[k-2],k)
        Lk,supk = scanD(D,Ck,minsupport)
        all_L.append(Lk)
        supportData.update(supk)
        k +=1
        print('k', k)
    return all_L,supportData
def geneRule(L,supportData,conf=0.7):
    rule = []
    #2个或者更多个元素产生规则
    for i in range(1,len(L)):
        # print('L',L[i])
        for frequence in L[i]:
            H1 = [frozenset([item]) for item in frequence]
            if i>1:#因为在传入数据的时候调用了sort函数，所以会按照：一个元素、两个元素、多个元素的顺序
                multi_item(frequence,H1,supportData,rule,conf=0.3)
            else:
                caculCon(frequence,H1,supportData,rule,conf=0.3)
    return rule
#多个频繁集计算规则
def multi_item(frequence,H,supportData,rule,conf=0.7):
    m = len(H[0])
    #循环条件：在一个频繁项中搜寻完所有的子集，len({1,2}) = len({1}) + 1终止循环，直接计算置信度；
    if len(frequence)> m+1:
        hamp = aprior_gen(H,m+1)
        # print('dimon:',hamp)
        hamp = caculCon(frequence,hamp,supportData,rule,conf)#父频繁项集大于置信度，子集频繁项才有可能大于置信度
        if len(hamp)>1:#父频繁项集大于一个，代表着可以合并
            multi_item(frequence,hamp,supportData,rule,conf)

#计算置信度
def caculCon(frequence,H,supportData,rule,conf=0.7):
    prunedH = []
    for conq in H:
        temp_conf = supportData[frequence]/supportData[frequence-conq]
        if temp_conf>conf:
            print(frequence-conq,'----->',conq)
            rule.append((frequence-conq,conq,temp_conf))
            prunedH.append(conq)
    return prunedH

if __name__=='__main__':
    data = loaddata()
    # c1 = createC1(data)
    # D = list(map(set,data))
    # print('invert dataSet:',D)
    # L1,supportData = scanD(D,c1,0.5)
    # print('support >0.5:',L1)
    # print('supportData >0.5:',supportData)
    #测试aprior_gen函数
    # test=[{1},{3},{2},{4}]
    # retList = aprior_gen(test,2)
    # print('generator n=2 set:',retList)

    #aprior算法频繁集产生测试
    all_L,supportData = aprior(data,minsupport=0.3)
    print('frequence item:',all_L)
    print('item support:',supportData)
    #aprior算法频规则产生测试
    rule = geneRule(all_L,supportData,conf=0.7)
    print(rule)
