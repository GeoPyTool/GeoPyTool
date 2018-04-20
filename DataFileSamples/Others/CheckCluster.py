#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:14:22 2018

@author: cycleuser
"""
import scipy
import scipy.cluster.hierarchy as hc
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import cm
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import euclidean_distances

fig = plt.figure(figsize=(12, 12))
fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

df = pd.read_excel('Cluster.xlsx')

ItemsAvalibale =  df.columns.values.tolist()


if 'Label' in ItemsAvalibale:
    df = df.set_index('Label')
    
dataframe = df    
dataframe =  dataframe.dropna(axis=1,how='all')


ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
               'Style', 'Width']

for i in ItemsToTest:
    if i in ItemsAvalibale:
        dataframe = dataframe.drop(i, 1)
        
dataframe2 = dataframe.T
corr1 = 1 - dataframe.corr()  
corr2 = 1 - dataframe2.corr()  


able =True

axup = fig.add_axes([0.58,0.95,0.4,0.1])

corr_condensed1 = hc.distance.squareform(corr1)  # convert to condensed

z1 = hc.linkage(corr_condensed1, method='average')
Z1 = hc.dendrogram(abs(z1),labels=corr1.columns)
axup.set_xticks([])
axup.set_yticks([])


axmatrixup = fig.add_axes([0.58, 0.54, 0.4, 0.4])


imup = axmatrixup.matshow(corr1, aspect='auto', origin='lower', cmap='GnBu')


axmatrixup.set_xticks([])
axmatrixup.set_xticklabels([], minor=False)
axmatrixup.xaxis.set_label_position('bottom')
axmatrixup.xaxis.tick_bottom()

axmatrixup.set_yticks([])
axmatrixup.set_yticklabels( [], minor=False)
axmatrixup.yaxis.set_label_position('right')
axmatrixup.yaxis.tick_right()





axleft = fig.add_axes([0.0,0.1,0.13,0.4])


corr_condensed2 = hc.distance.squareform(corr2)  # convert to condensed

z2 = hc.linkage(corr_condensed2, method='average')
Z2 = hc.dendrogram(abs(z2),labels=corr2.columns,orientation='left')
#Z2 = hc.dendrogram(abs(z2),labels=corr2.columns,orientation='left')
axleft.set_xticks([])
axleft.set_yticks([])

axmatrixleft = fig.add_axes([0.14, 0.1, 0.4, 0.4])
imleft = axmatrixleft.matshow(corr2, aspect='auto', origin='lower', cmap='GnBu')




axmatrixleft.set_xticks([])
axmatrixleft.set_xticklabels([], minor=False)
axmatrixleft.xaxis.set_label_position('bottom')
axmatrixleft.xaxis.tick_bottom()

axmatrixleft.set_yticks([])
axmatrixleft.set_yticklabels( [], minor=False)
axmatrixleft.yaxis.set_label_position('right')
axmatrixleft.yaxis.tick_right()





axmatrix = fig.add_axes([0.58, 0.1, 0.4, 0.4])




idx1 = Z1['leaves']
idx2 = Z2['leaves']

done = np.ones(dataframe.shape)
a = np.dot(done, corr1)

b = np.dot(a.T, corr2)

D = b.T

D = D[idx2, :]
D = D[:, idx1]
im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap='Blues')

XLabelList = [corr1.columns[i] for i in idx1]
YLabelList = [corr2.columns[i] for i in idx2]

XstickList=[i for i in range(len(XLabelList))]
YstickList=[i for i in range(len(YLabelList))]

axmatrix.set_xticks(XstickList)
axmatrix.set_xticklabels( XLabelList, minor=False)
axmatrix.xaxis.set_label_position('bottom')
axmatrix.xaxis.tick_bottom()

axmatrix.set_yticks(YstickList)
axmatrix.set_yticklabels( YLabelList, minor=False)
axmatrix.yaxis.set_label_position('right')
axmatrix.yaxis.tick_right()


for (j,i),label in np.ndenumerate(corr1):
    axmatrixup.text(i,j,"%.2f" % label,ha='center',va='center')
    
for (j,i),label in np.ndenumerate(corr2):
    axmatrixleft.text(i,j,"%.2f" % label,ha='center',va='center')
    
for (j,i),label in np.ndenumerate(D):
    axmatrix.text(i,j,"%.2f" % label,ha='center',va='center')
    
    
axcolor1 = fig.add_axes([0.3, 0.54, 0.02, 0.4])

# Plot colorbar.

plt.colorbar(im, cax=axcolor1)