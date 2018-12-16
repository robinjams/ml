from numpy  import *
#一维数组
a = array([5,1,3,2])
print(a.argsort())
print('----')
x = argsort(a)
print(a[x])
#二维数组
two = array([[1,256,3],[4,1,6],[1,23,3]])
sort_t = two.argsort(axis=1)
print(sort_t)
print(two[two[:,2].argsort()])#按照第三列对行进行排序
print(two[:,two[2].argsort()])#按照第三行对列进行排序