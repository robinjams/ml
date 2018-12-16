from  numpy import *
a = [3,2,56,1]
la = ['1','1','2','2']
re = argsort(a)
print(re)
for i in range(4):
    print(la[re[i]])