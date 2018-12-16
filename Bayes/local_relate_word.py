#encoding:utf-8_*_
#author：@robin
#create time：2018/8/10 15:02
#file：local_relate_word.py
#IDE:PyCharm
import numpy as np
import feedparser

#未完成可以忽略


#RSS源测试学习
# d = feedparser.parse('https://blog.csdn.net/qq_32679835/rss/list')
# print(d.feed.title)
# print(len(d.entries))
# ti = [e.title for e in d.entries][:5]
# print(ti)
# ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
print(len(sf.entries))