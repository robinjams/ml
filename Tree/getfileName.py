#encoding:utf-8_*_
#author：@robin
#create time：2018/8/9 11:23
#file：getfileName.py
#IDE:PyCharm
import sys,os
#获取当前文件名,出现结果文件，直接命名
def getfile_name():
    # print(sys.argv)
    file_name = os.path.basename(sys.argv[0]).split('.')[0]
    result = file_name+'_result'
    # print(file_name)
    return result