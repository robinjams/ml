#encoding:utf-8_*_
#author：@robin
#create time：2018/11/26 13:43
#file：map_point_cluter.py
#IDE:PyCharm
import numpy as np
import json
import re
import Cluster.Kmeans as kmean

def gene_data(filename):
    import xml.etree.ElementTree as ET
    import os
    import sys
    file = os.path.abspath(filename)
    print(file)
    data = []
    try:
        tree = ET.parse(file)
        print('tree type',type(tree))
        root = tree.getroot()
    except Exception as e:
        print('cml error')
        sys.exit()
    print(root.tag,'------',root.attrib)
    temp = ''
    for country in root:
        print(country.tag, '----', country.attrib)
        for stat in country:
            # print(stat.tag, '----', stat.attrib)
            for city in stat:
                # print(city.tag, '----', city.attrib,'-----',city.get('Name'))
                temp = '%s%s%s\n' % (country.get('Name'),stat.get('Name'),city.get('Name'))
                data.append(temp)
    return data
def write(data):
    with open('china.txt','w', encoding="utf-8") as fr:
        for in_data in data:
            fr.write(in_data)
    return
def lng_lat(filename):
    from  urllib.request import urlopen,quote
    import requests
    # 经度 Longitude
    # 纬度Latitude
    lng = [];lat = []
    ak = 'F3EsPx6ylsIgK7QbrxpA09NZdUtZekRE'
    with open(filename,'r',encoding="utf-8") as fr:
        for line in fr.readlines():
            # print(line.strip('\n'))
            print('location',line.strip('\n'))
            location = quote(line.strip('\n'))
            uri =  'http://api.map.baidu.com/geocoder/v2/?address='+location+'&output=json&ak='+ak+'&callback=showLocation'
            # print(uri)
            req = requests.get(uri)
            original = req.text
            result = re.split('[(|)]',original)[1]
            # print(result)#注意获取的json格式的标准化
            temp = json.loads(result)
            lng.append(temp['result']['location']['lng'])
            lat.append(temp['result']['location']['lat'])
    with open('lng_lat.txt','w') as fr:
        ln = json.dumps(lng)
        fr.write(ln)
        la = json.dumps(lat)
        fr.write(la)
    return lng,lat
def get_last_file():
    # 获取城市数据
    # data = gene_data('LocList.xml')
    # write(data)

    # 将城市数据转化为经纬度
    # lng,lat = lng_lat('china.txt')
    # print('lng',lng)
    # print('lat',lat)
    with open('lng_lat.txt') as fr:
        data_or = fr.read()
        data = re.split('[\[|\]]', data_or)
    print(len(data))
    lng = re.split('[\'|,]', data[1])
    lat = re.split('[\'|,]', data[3])
    m = len(lng)
    print(lng)
    # 转化为具体的经纬度
    list_lng = [];
    list_lat = []
    for i in range(m):
        list_lng.append(float(lng[i]))
        list_lat.append(float(lat[i]))
    # 写入到新的文件
    with open('china.txt', 'r', encoding='utf-8') as From_file:
        lines = From_file.readlines()
        for i in range(0, len(lines)):
            # 去除语句的换行符（strip()）
            lines[i] = lines[i].strip() + '\t' + str(list_lng[i]) + '\t' + str(list_lat[i]) + '\n'
            # print(lines[i])
    # 最终需要的文件china_result.txt
    with open('china_result.txt', 'w', encoding='utf-8') as Out_file:
        Out_file.writelines(lines)
def disCaculate(VecA,VecB):
    a = np.sin(VecA[0,1]*np.pi/180)*np.sin(VecB[0,1]*np.pi/180)
    b = np.cos(VecA[0,1]*np.pi/180)*np.cos(VecB[0,1]*np.pi/180)*np.cos((VecA[0,0]-VecB[0,0])*np.pi/180)
    # print(np.arccos(a+b)*6371.0)
    return np.arccos(a+b)*6371.0
    #数据的顺序：地名、经度、纬度
def plot(filename,num=5):
    from matplotlib import pyplot as plt
    data = []
    with open(filename,'r',encoding='utf-8') as fr:
        for line in fr.readlines():
            get_data = [float(line.strip().split('\t')[1]),float(line.strip().split('\t')[2])]
            data.append(get_data)

    dataMat= np.mat(data)
    print(dataMat[:3])
    centrios,storge = kmean.kmean(dataMat,num,distMeas=disCaculate)
    # print(centrios)
    # print(storge)
    # kmean.plot(data,centrios,storge)
    rect = [0.1,0.1,0.8,0.8]
    scattermarkers = ['*','2','p','h','^','o']
    axprops = dict(xticks=[],yticks=[])#使得坐标消失，方便两幅图形重合
    fig = plt.figure(figsize=(12,8))
    ax0 = fig.add_axes(rect,label='ax0',**axprops)
    imgP = plt.imread('china_new.png')#基于图像创建矩阵
    ax0.imshow(imgP,alpha=0.5)
    ax1 = fig.add_axes(rect,label = 'ax1',frameon=False)
    for i in range(num):
        point = dataMat[np.nonzero(storge[:,0]==i)[0],:]
        print(scattermarkers[i % len(scattermarkers)])
        markerStyle = scattermarkers[i % len(scattermarkers)]
        ax1.scatter(point[:,0].flatten().A[0],point[:,1].flatten().A[0],marker=markerStyle,s=90,alpha=0.6)
    ax1.scatter(centrios[:,0].flatten().A[0],centrios[:,1].flatten().A[0],marker='+',color='black',s=200,alpha=0.8)
    plt.show()

if __name__=='__main__':
    plot('china_result.txt',num=8)