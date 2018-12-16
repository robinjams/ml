#encoding:utf-8_*_
#author：@robin
#create time：2018/9/6 16:25
#file：jcxx.py
#IDE:PyCharm
import numpy as np
import pymysql as sql
import re
from getdata import index_common

def operatorjcxx():
    # 公司名称、成立日期、注册资本、注册地址、办公地址、法定代表人、统一社会信用代码、经营业务范围、性质、产业集群、行业、入资时间-停用、入资日期、主营业务、rest接口编号
    temp = []
    last = []
    opertor = r'restjcxx.txt'
    count = len(open(opertor, encoding='utf-8').readlines())
    for i in range(count):
        result = index_common.read(operator=opertor, line=i)
        if "公司名称" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            temp = []
            cname = re.split(r"\[|\]", index_common.read(operator=opertor, line=i + 1))
            # print(cname)
            # 公司名称
            temp.append(cname[2])
            # print('公司名称',cname[2])
        elif "成立日期" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            s_Date = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(s_Date) == 11:
                temp.append(s_Date[5])
            else:
                temp.append('')
        elif "注册资本" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            money = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(money) == 11:
                temp.append(money[5])
            else:
                temp.append('')
        elif "注册地址" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            z_address = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(z_address) == 11:
                temp.append(z_address[5])
            else:
                temp.append('')
        elif "办公地址" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            b_address = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(b_address) == 11:
                temp.append(b_address[5])
            else:
                temp.append('')
        elif "法定代表人" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            person1 = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(person1) == 11:
                temp.append(person1[5])
            else:
                temp.append('')
        elif "统一社会信用代码" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            code = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(code) == 11:
                temp.append(code[5])
            else:
                temp.append('')
        elif "经营业务范围" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            bus_range = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(bus_range) == 11:
                temp.append(bus_range[5])
            else:
                temp.append('')
        elif "性质"  in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            # 性质都为空
            proper = ''
            temp.append(proper)
        elif "产业集群" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            # 产业集群都为空
            indu_cluster = ''
            temp.append(indu_cluster)
        elif "行业"  in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            # 行业都为空
            industrail = ''
            temp.append(industrail)
        elif "入资时间-停用" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            enterDataStop = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(enterDataStop)
            # print(len(enterDataStop))
            if len(enterDataStop) == 11:
                temp.append(enterDataStop[5])
            else:
                temp.append('')
        elif "入资日期" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            enterData = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(enterData)
            # print(len(enterData))
            if len(enterData) == 11:
                temp.append(enterData[5])
            else:
                temp.append('')
        elif "主营业务" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            focus_com = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(focus_com)
            # print(len(focus_com))
            if len(focus_com) == 11:
                temp.append(focus_com[5])
            else:
                temp.append('')
        elif "rest接口编号" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            rest_num = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(rest_num)
            # print(len(rest_num))
            if len(rest_num) == 11:
                temp.append(rest_num[5])
            else:
                temp.append('')
        last.append(temp)
    get = list(np.unique(np.array(last)))  # 去重
    get.remove([])  # 删除空
    return get
def insertjcxx():
    db = sql.connect(
        host="localhost",
        user="root",
        password="",
        db="rest",
        port=3306,
        charset='utf8',
    )
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    # 插入到restdw
    get_jcxx = operatorjcxx()

    # 备份数据库，备份上一次数据库
    try:
        if index_common.table_exists(cur, 'gkrestjcxx.bak') == 1:
            cur.execute('drop table if exists `gkrestjcxx.bak`  ')  # 在插入之前清除数据库
            cur.execute("CREATE TABLE if not exists `gkrestjcxx.bak` SELECT * FROM `gkrestjcxx`; ")
            cur.execute("ALTER TABLE `gkrestjcxx.bak` ADD PRIMARY KEY(`jcxx_id`); ")  # 设置主键
        else:
            # 删除表之前先备份
            cur.execute("CREATE TABLE if not exists `gkrestjcxx.bak` SELECT * FROM `gkrestjcxx`; ")
            cur.execute("ALTER TABLE `gkrestjcxx.bak` ADD PRIMARY KEY(`jcxx_id`); ")  # 设置主键
    except Exception as e:
        db.rollback()  # 出错回滚
    db.commit()


    # 入数据之前清空数据
    cur.execute('DELETE FROM `gkrestjcxx` WHERE 1')  # 在插入之前清除数据库
    cur.connection.commit()
    print('清除成功')
    # print(get_jcxx)
    # 单条插入
    for i in get_jcxx:
        auto_increment = cur.lastrowid  # 获取最新自增id
        i.insert(0, auto_increment + 1)
        # print(i)
        cur.execute('INSERT INTO `gkrestjcxx`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',i)
    # #多条插入
    # cur.executemany('INSERT INTO `gkrestjcxx`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', get_jcxx)

    cur.connection.commit()  # 执行commit操作，插入语句才能生效
    print('jcxx insert over')
if __name__=="__main__":
    # get_jcxx = operatorjcxx()
    # print(get_jcxx[:1])
    # 操作持基础信息
    insertjcxx()
