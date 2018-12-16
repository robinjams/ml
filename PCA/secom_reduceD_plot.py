#encoding:utf-8_*_
#author：@robin
#create time：2018/12/3 8:49
#file：secom_reduceD_plot.py
#IDE:PyCharm
import numpy as np
from matplotlib import pyplot as  plt
from PCA.pca_reduce_dim import  *
data = deal_data('secom.data')
data_mean = np.mean(data,axis=0)
normal = data - data_mean
corr = np.cov(normal,rowvar=0)
feat_val,feat_vet = np.linalg.eig(np.mat(corr))
sort_index = np.argsort(feat_val)
sort_index = sort_index[::-1]
feat_val = feat_val[sort_index]
total = np.sum(feat_val)
var_percent = feat_val/total*100
print(var_percent)#由图像可知，方差会急剧降低

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(1, 21), var_percent[:20], marker='^')
plt.xlabel('Principal Component Number')
plt.ylabel('Percentage of Variance')
plt.show()

