#encoding:utf-8_*_
#author：@robin
#create time：2018/9/6 19:35
#file：jsh.py
#IDE:PyCharm
import numpy as np
import pymysql as sql
import re
from getdata import index_common


def insertjsh():
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
    # 插入到restdsh
    get_jsh = operatorjsh()

    # 备份数据库，备份上一次数据库
    try:
        if index_common.table_exists(cur, 'gkrestjsh.bak') == 1:
            cur.execute('drop table if exists `gkrestjsh.bak`  ')  # 在插入之前清除数据库
            cur.execute("CREATE TABLE if not exists `gkrestjsh.bak` SELECT * FROM `gkrestjsh`; ")
            cur.execute("ALTER TABLE `gkrestjsh.bak` ADD PRIMARY KEY(`jsh_id`); ")  # 设置主键
        else:
            # 删除表之前先备份
            cur.execute("CREATE TABLE if not exists `gkrestjsh.bak` SELECT * FROM `gkrestjsh`; ")
            cur.execute("ALTER TABLE `gkrestjsh.bak` ADD PRIMARY KEY(`jsh_id`); ")  # 设置主键
    except Exception as e:
        db.rollback()  # 出错回滚
    db.commit()

    # 入数据之前清空数据
    cur.execute('DELETE FROM `gkrestjsh` WHERE 1')  # 在插入之前清除数据库
    cur.connection.commit()
    print('清除成功')
    #单条插入测试
    for i in get_jsh:
        auto_increment = cur.lastrowid  # 获取最新自增id
        i.insert(0, auto_increment + 1)
        # print(i)
        cur.execute('INSERT INTO `gkrestjsh`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',i)
    #多条一次性插入
    # cur.executemany('INSERT INTO `gkrestjsh`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',get_jsh)

    cur.connection.commit()  # 执行commit操作，插入语句才能生效
    print("jsh insert ok")
def operatorjsh():
    #公司名称、统一社会信用代码、性质、授权查看人员、受权查看部门 、编号、届次、任期开始时间、任期结束时间、监事会成员、状态、届次时间、届次结束时间、角色信息、推荐方
    temp = []
    last = []
    opertor = r'restjsh.txt'
    count = len(open(opertor, encoding='utf-8').readlines())
    for i in range(count):
        result = index_common.read(operator=opertor, line=i)
        # print(result)
        if "公司名称" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            temp = []
            cname = re.split(r"\[|\]", index_common.read(operator=opertor, line=i + 1))
            # print(cname)
            # 公司名称
            temp.append(cname[2])
            # print('公司名称',cname[2])
        elif "统一社会信用代码" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            # 统一信用编码都为空
            commonCode = ''
            temp.append(commonCode)
        elif "性质" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            property = ''
            temp.append(property)
        elif "授权查看人员" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            allowPeople = ''
            temp.append(allowPeople)
        elif "受权查看部门" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            allowOrgnize = ''
            temp.append(allowOrgnize)
        elif "编号" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            number = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            if len(number) == 11:
                temp.append(number[5])
            else:
                temp.append('')
                # print("编号：",number[2])
        elif "届次时间" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            jieciDate = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(jieciDate)
            # print(len(jieciDate))
            if len(jieciDate) == 11:
                temp.insert(11,jieciDate[5])
            else:
                temp.append('')
        elif "届次结束时间" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            enddate = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(enddate)
            # print(len(enddate))
            if len(enddate) == 11:
                temp.insert(12,enddate[5])
            else:
                temp.append('')
        elif "届次" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            jieci = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(jieci[5])
            # print(len(jieci))
            if len(jieci) == 11:
                if jieci[5].startswith('第'):#是否已第开头
                    temp.append(jieci[5])
                else:
                    temp.append('')
        elif "任期开始时间" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            startDate = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(startDate)
            # print(len(startDate))
            if len(startDate) == 11:
                temp.insert(7,startDate[5])
            else:
                temp.append('')
        elif "任期结束时间" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            endDate = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(endDate)
            # print(len(endDate))
            if len(endDate) == 11:
                temp.insert(8,endDate[5])
            else:
                temp.append('')
        elif "监事会成员" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            supervisor = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(supervisor)
            # print(len(supervisor))
            if len(supervisor) == 11:
                temp.append(supervisor[5])
            else:
                temp.append('')
        elif "状态" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            status = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(status)
            # print(len(status))
            if len(status) == 11:
                temp.append(status[5])
            else:
                temp.append('')
        elif "角色信息" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            rolemessage = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(rolemessage)
            # print(len(rolemessage))
            if len(rolemessage) == 11:
                temp.append(rolemessage[5])
            else:
                temp.append('')
        elif "推荐方" in result and "<value>" in index_common.read(operator=opertor, line=i + 1):
            recommand = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(recommand)
            # print(len(recommand))
            if len(recommand) == 11:
                temp.append(recommand[5])
            else:
                temp.append('')
        last.append(temp)
    get = list(np.unique(np.array(last)))  # 去重
    get.remove([])  # 删除空
    return get

if __name__ == "__main__":
    #测试获取的监事会list
    # get_jsh = operatorjsh()
    # print(get_jsh[:3])
    #操作监事会
    insertjsh()