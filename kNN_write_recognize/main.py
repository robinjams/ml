#encoding:utf-8_*_
#author：@robin
#create time：2018/8/4 17:12
#file：main.py
#IDE:PyCharm
import matplotlib.pyplot as plt
import numpy as np
import kNN_write_recognize.KNN_writer as kw
#获取当前路径
# import os
# cwd = os.getcwd()
# print(cwd)
# print(cwd+'\\trainingDigits\\0_0.txt')

#将图片转化为向量
# victor = kw.imag2Victor(cwd+'\\trainingDigits\\0_0.txt')#转化后的一维向量
# print(victor[0,11:19])

#手写识别
kw.hand_writer()