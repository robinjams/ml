#encoding:utf-8_*_
#author：@robin
#create time：2018/9/10 16:11
#file：conn_gksql.py
#IDE:PyCharm
import numpy as np
import pymysql as sql
from getdata import dsh,dw,jsh,jybz,jcxx,cgbl,index_common

#获取果壳personlist中的name字段
def get_gk():
    name = []
    conn = sql.connect (host='192.168.139.206', user='root', passwd='psw.db7898', db='ict2', charset='utf8' )
    # conn = sql.connect (host='localhost', user='root', passwd='', db='rest', charset='utf8' )
    cur = conn.cursor()  # 获取一个游标
    cur.execute('SELECT * FROM `gkpersonlist`')
    data = cur.fetchall()
    for d in data:
        name.append([d[0],d[6]])
    cur.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return name

#获取所有接口数据的姓名参数
def out_value():
    temp = []#临时存储变量
    reback = []#最终返回所有姓名
    #董事会数据
    # dsh_name = []#保存董事会姓名
    result = dsh.operatorrestdsh()
    for i in result:
        # print(i)
        temp.append([i[9],i[13]])#添加姓名和职位,公司名称作为一个list
    dsh_name = list(set([tuple(te) for te in temp] ))#二维数组去重
    if ('', '', '') in dsh_name:
        dsh_name.remove(('', '', ''))  # 删除空元素
    reback = reback + dsh_name    #监事会数据

    #保存监事会姓名
    # jsh_name = []
    result = jsh.operatorjsh()
    temp = []
    for i in result:
        # print(i)
        temp.append([i[9], i[14]])  # 添加姓名和职位,公司名称作为一个list
    jsh_name = list(set([tuple(te) for te in temp]))  # 二维数组去重
    if ('', '', '') in jsh_name:
        jsh_name.remove(('', '', ''))  # 删除空元素
    reback = reback + jsh_name

    #基础信息
    # jcxx_name = []#保存基础信息姓名
    result = jcxx.operatorjcxx()
    temp = []
    for i in result:
        # print(i)
        temp.append([i[5], i[0]])  # 添加姓名和职位,公司名称作为一个list
    jcxx_name = list(set([tuple(te) for te in temp]))  # 二维数组去重
    reback = reback + jcxx_name
    #党委
    result = dw.operatordw()
    temp = []
    for i in result:
        # print(i)
        temp.append([i[9], i[0]])  # 添加姓名和职位,公司名称作为一个list
    dw_name = list(set([tuple(te) for te in temp]))  # 二维数组去重
    reback = reback + dw_name

    #经营班子
    result = jybz.operatorjybz()
    temp = []
    for i in result[:3]:
        # print(i)
        temp.append([i[9], i[0]])  # 添加姓名和职位,公司名称作为一个list
    jybz_name = list(set([tuple(te) for te in temp]))  # 二维数组去重
    reback = reback + jybz_name

    #reback去重
    reback = list(set([tuple(li) for li in reback]))
    return reback


#判断personlist和接口数据中人员数据是否相等，并且关联成二维的list
def out_relation_in():
    back_name = []
    name = get_gk()
    # print(name)
    out= out_value()
    for in_name in name:
        # print("in:",in_name)
        for out_name in out:
            if in_name[1] == out_name[0] :#判断本地数据库中的姓名是否与接口姓名相同
                contact = list(out_name)+list([in_name[0]])#连接list列表
                back_name.append(contact)
    print(back_name)
    return back_name

#将关联数据插入到gk_rest_relation数据库
def insert_rest_personlist():
    conn = sql.connect(
        host="localhost",
        user="root",
        password="",
        db="rest",
        port=3306,
        charset='utf8',
    )
    # 使用cursor()方法获取操作游标
    cur = conn.cursor()

    # 备份数据库，备份上一次数据库
    try:
        YN = index_common.table_exists(cur, 'gk_rest_relation.bak')
        if YN == 1:
            cur.execute('drop table if exists `gk_rest_relation.bak`  ')  # 在插入之前清除数据库
            cur.execute("CREATE TABLE if not exists `gk_rest_relation.bak` SELECT * FROM `gk_rest_relation`; ")
            cur.execute("ALTER TABLE `gk_rest_relation.bak` ADD PRIMARY KEY(`id`); ")  # 设置主键
        else:
            # 删除表之前先备份
            cur.execute("CREATE TABLE if not exists `gk_rest_relation.bak` SELECT * FROM `gk_rest_relation`; ")
            cur.execute("ALTER TABLE `gk_rest_relation.bak` ADD PRIMARY KEY(`id`); ")  # 设置主键
    except Exception as e:
        conn.rollback()  # 出错回滚
    conn.commit()

    # 获取数据
    data = out_relation_in()
    # 插入数据之前清空数据
    cur.execute('DELETE FROM `gk_rest_relation` WHERE 1')  # 在插入之前清除数据库数据
    print('清除成功')
    #单条插入数据
    for i in data:
        auto_increment = cur.lastrowid # 获取自增id
        i.insert(0, auto_increment+1)
        cur.execute('INSERT INTO `gk_rest_relation` VALUES (%s,%s,%s,%s)', i)
    print("ok")


if __name__=='__main__':
    #获取personlist中的id编号和
    # result = get_gk()
    # print(result)

    #获取接口数据姓名
    # reback = out_value()
    # print(reback)

    #personlist和接口姓名关联结果
    # out_relation_in()

    #插入到数据库
    insert_rest_personlist()