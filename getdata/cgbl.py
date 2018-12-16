#encoding:utf-8_*_
#author：@robin
#create time：2018/9/6 20:07
#file：cgbl.py
#IDE:PyCharm
import numpy as np
import pymysql as sql
import re
from getdata import index_common

def operaterestcgbl():
    # dict = {'公司名称':'', "统一社会信用代码":"", "性质":"", "授权查看人员":"", "受权查看部门":"", "编号":"", "股东":"", "持股比例":"", "状态":"", "日期":""}
    temp = []
    last = []
    opertor = r'restcgbl.txt'
    count = len(open(r'restcgbl.txt', encoding='utf-8').readlines())
    for i in range(count):
        result = index_common.read(operator=opertor, line=i)
        # print(result)
        if "公司名称" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            temp = []
            cname = re.split(r"\[|\]", index_common.read(operator=opertor, line=i + 1))
            # print(cname)
            # 公司名称
            temp.append(cname[2])
            # print('公司名称',cname[2])
        elif "统一社会信用代码" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            # 统一信用编码都为空
            commonCode = ''
            temp.append(commonCode)
        elif "性质" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            property = ''
            temp.append(property)
        elif "授权查看人员" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            allowPeople = ''
            temp.append(allowPeople)
        elif "受权查看部门" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            allowOrgnize = ''
            temp.append(allowOrgnize)
        elif "状态" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            status = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            if len(status) == 11:
                temp.append(status[5])
            else:
                temp.append('')
            # print("状态：",status[2])
        elif "编号" in result and "<value>" in index_common.read(operator=opertor, line=i+1):

            number = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            if len(number)==11:
                temp.append(number[5])
            else:
                temp.append('')
            # print("编号：",number[2])
        elif "股东" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            board = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            if len(board)==11:
                temp.append(board[5])
            else:
                temp.append('')
            # print("股东：", board[2])
        elif "持股比例" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            percent = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            # print(percent)
            if len(percent) == 11:
                temp.append(percent[5])
            else:
                temp.append('')
        elif "日期" in result and "<value>" in index_common.read(operator=opertor, line=i+1):
            date = re.split(r"\[|\]|\>|\<", index_common.read(operator=opertor, line=i + 1).strip())
            if len(date) == 11:
                temp.append(date[5])
            else:
                temp.append('')
            # print("日期：", date[2])
        last.append(temp)
    get = list(np.unique(np.array(last)))#去重
    get.remove([])#删除空
    return get
def insertcgbl():
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

    # # 备份数据库，备份上一次数据库
    try:
        YN = index_common.table_exists(cur, 'gkrestcgbl.bak')
        if  YN== 1:
            cur.execute('drop table if exists `gkrestcgbl.bak`  ')  # 在插入之前清除数据库
            cur.execute("CREATE TABLE if not exists `gkrestcgbl.bak` SELECT * FROM `gkrestcgbl`; ")
            cur.execute("ALTER TABLE `gkrestcgbl.bak` ADD PRIMARY KEY(`id_cgbl`); ")  # 设置主键
        else :
            # 删除表之前先备份
            cur.execute("CREATE TABLE if not exists `gkrestcgbl.bak` SELECT * FROM `gkrestcgbl`; ")
            cur.execute("ALTER TABLE `gkrestcgbl.bak` ADD PRIMARY KEY(`id_cgbl`); ")  # 设置主键
    except Exception as e:
        db.rollback()#出错回滚
    db.commit()

    #插入数据之前清空数据
    cur.execute('DELETE FROM `gkrestcgbl` WHERE 1')  # 在插入之前清除数据库数据
    print('清除成功')
    # 插入到gkrestcgbl
    get_cgbl = operaterestcgbl()
    for i in get_cgbl:
        auto_increment = cur.lastrowid#获取最新自增id
        # print(auto_increment)
        i.insert(0,auto_increment+1)
        #解决持股比例为空的情况，导入数据库会报错，i[7]表示持股比例
        if i[7]=='':
            i[7] = float(0.0)

        cur.execute('INSERT INTO `gkrestcgbl`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', i)

    # cur.executemany('INSERT INTO `gkrestcgbl`  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', get_cgbl)

    cur.connection.commit()  # 执行commit操作，插入语句才能生效
    print("cgbl insert ok")

if __name__ == '__main__':
    # 操作持股比例
    # get_cgbl = operaterestcgbl()
    # print(get_cgbl[:2])
    insertcgbl()