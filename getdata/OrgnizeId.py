#encoding:utf-8_*_
#author：@robin
#create time：2018/9/7 8:29
#file：OrgnizeId.py
#IDE:PyCharm
import requests
import json
from getdata import dsh,dw,jsh,jybz,jcxx,cgbl,index_common
import re
import pymysql as sql

#获取其中出现的id
def id():
    last = []#存储最终的所有公司名称id
    temp = []#临时存储变量
    dsh_id = []#存储董事会id
    jsh_id= []#存储监事会id
    dw_id = []#存储党委id
    jcxx_id = []#存储基础信息id
    jybz_id = []#存储经营班子id
    cgbl_id = []#存储持股比例id

    #获取董事会
    get_dsh_id = dsh.operatorrestdsh()
    for i in get_dsh_id:
        temp.append(i[0])
    # print('dsh over')
    dsh_id = list(set(temp))
    # print("董事会：",dsh_id)

    #获取监事会
    get_jsh_id = jsh.operatorjsh()
    temp = []
    for i in get_jsh_id:
        temp.append(i[0])
    # print('jsh over')
    jsh_id = list(set(temp))
    # print("监事会：",jsh_id)

    # 获取持股比例
    get_cgbl_id = cgbl.operaterestcgbl()
    temp = []
    for i in get_cgbl_id:
        temp.append(i[0])
    # print('cgbl over')
    cgbl_id = list(set(temp))

    # 获取党委
    get_dw_id = dw.operatordw()
    temp = []
    for i in get_dw_id:
        temp.append(i[0])
    # print('dw over')
    dw_id = list(set(temp))

    # 获取基础信息
    get_jcxx_id = jcxx.operatorjcxx()
    temp = []
    for i in get_jcxx_id:
        temp.append(i[0])
    # print('jcxx over')
    jcxx_id = list(set(temp))

    # 获取经营班子
    get_jybz_id = jybz.operatorjybz()
    temp = []
    for i in get_jybz_id:
        temp.append(i[0])
    # print('jybz over')
    jybz_id = list(set(temp))

    # 连接所有的id
    last_id = []#未去重前的id
    last_id.extend(jybz_id)
    last_id.extend(jcxx_id)
    last_id.extend(dw_id)
    last_id.extend(cgbl_id)
    last_id.extend(jsh_id)
    last_id.extend(dsh_id)
    #id去重获取最后的id
    last= list(set(last_id))
    # print(last_id)
    # print(last)
    return last

#获取id对应的组织名,并插入到数据库
def getName():
    temp_data = []#临时存放id----name值，最终插入数据库需要
    url = 'http://111.198.138.113:81/seeyon/rest/token/lichun/psw.seeyon@7898'
    result = requests.get(url)
    # print(result.cookies)
    json_str = json.loads(result.text)
    # print(json_str["id"])
    token = json_str["id"]
    headers = \
        {
            # 'Host' : '111.198.138.113:81',
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36",
            "content-type": "application/json",
            # 'cookie':"JSESSIONID=0CAFC4421EF851D9498B17B553237B12",
            'token': token,
            "Content-Type": "application/json;charset=UTF-8",
        }
    #连接数据库的参数
    db = sql.connect(
        host="localhost",
        user="root",
        password="",
        db="rest",
        port=3306,
        charset='utf8',
    )
    # SQL:使用cursor()方法获取操作游标
    cur = db.cursor()

    param = id()#获得了所有公司的id编码
    print("所有公司id输出：",param)#输出现有公司编号

    # 备份数据库，备份上一次数据库
    try:
        if index_common.table_exists(cur, 'gkrest_id_name.bak') == 1:
            cur.execute('drop table if exists `gkrest_id_name.bak`  ')  # 在插入之前清除数据库
            cur.execute("CREATE TABLE if not exists `gkrest_id_name.bak` SELECT * FROM `gkrest_id_name`; ")
            cur.execute("ALTER TABLE `gkrest_id_name.bak` ADD PRIMARY KEY(`id`); ")  # 设置主键
        else:
            # 删除表之前先备份
            cur.execute("CREATE TABLE if not exists `gkrest_id_name.bak` SELECT * FROM `gkrest_id_name`; ")
            cur.execute("ALTER TABLE `gkrest_id_name.bak` ADD PRIMARY KEY(`id`); ")  # 设置主键
    except Exception as e:
        db.rollback()  # 出错回滚
    db.commit()

    cur.execute('DELETE FROM `gkrest_id_name` WHERE 1')#在插入之前清除数据库
    cur.connection.commit()
    print('清除成功')
    count = 0#计算更新了几个公司名
    for pa in param:
        url = 'http://111.198.138.113:81/seeyon/rest/orgDepartment/' + pa#获取不同公司的信息
        response = requests.get(url, headers=headers)
        result = json.loads(response.text)#转化为json数据
        name = result['name']
        temp_data = [pa, name]
        # print(temp_data)
        cur.execute('INSERT INTO `gkrest_id_name`  VALUES (%s,%s)', temp_data)
        cur.connection.commit()
        count += 1
        print("%d"%(count))
    print("更新%d条数据"%len(param))

if __name__=='__main__':
    #获取每个公司的id
    id()
    #测试将id-name字段插入到数据库中
    getName()
