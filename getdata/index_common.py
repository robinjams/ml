#encoding:utf-8_*_
#author：@robin
#create time：2018/9/4 16:45
#file：index_common.py
#IDE:PyCharm
import requests
import json
import datetime
import time
import re
from getdata import dsh,dw,jsh,jybz,jcxx,cgbl,OrgnizeId,conn_gksql

#获取更新表的名单
def get():
    url = 'http://111.198.138.113:81/seeyon/rest/token/lichun/psw.seeyon@7898'
    result = requests.get(url)
    # print(result.cookies)
    json_str = json.loads(result.text)
    print("获取的token：%s"%json_str["id"])
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
    param = ['restcgbl', 'restdsh', 'restdw', 'restjsh', 'restjybz','restjcxx',]
    count = 0
    for index,pa in enumerate(param):
        url = 'http://111.198.138.113:81/seeyon/rest/form/export/' + pa + '?endDateTime=2018-9-5&beginDateTime=2017-01-01'
        # print('连接%s' % pa)
        response = requests.get(url, headers=headers)
        with open(pa + '.txt', 'w', encoding='utf-8') as fp:
            fp.truncate()#更新接口数据的时候，清空文件内容
            print('第%d个文件%s运行'%(index+1,pa))
            fp.write(response.text)
        count += 1
    print('完成%d个文件的更新' % count)


#向数据中添加各个值
def insert():
    cgbl.insertcgbl()#参股比例
    dsh.insertdsh()#董事会
    dw.insertdw()#党委
    jsh.insertjsh() #监事会
    jybz.insertjybz()#经营班子
    jcxx.insertjcxx()#基础信息



#读取文件特定的某一行,在创建各个表的时候用到
def read(operator,line):
    import linecache
    #修改文件名
    # operator = "restdsh"
    result = linecache.getline(filename=operator, lineno=line).strip()
    return result
#判断表是否存在
def table_exists(con,table_name):        #这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    # print(get_table)
    tables = [con.fetchall()]
    # print(str(tables))
    table_list = re.findall('(\'.*?\')',str(tables))#返回满足条件的多个表达式
    # print(table_list)
    table_list = [re.sub("'",'',each) for each in table_list]#正则替换
    # print(table_list)
    if table_name in table_list:
        return 1        #存在返回1
    else:
        return 0        #不存在返回0

if __name__ == '__main__':

    # 获取数据
    print('-------------start get data----------------')
    get()
    print('-------------end get data----------------')
    #插入数据
    print('-------------start insert data----------------')
    insert()
    print('-------------end insert data----------------')
    #关联表的插入
    print('-------------start relational data----------------')
    OrgnizeId.getName()
    print('-------------end relational data----------------')
    #关联到国科数据库
    print('-------------start gk sql----------------')
    conn_gksql.insert_rest_personlist()
    print('-------------end gk sql----------------')
