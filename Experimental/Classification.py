version = '0.6.59'

date = '2017-11-14'

dpi = 128
#coding:utf-8

import sys
import os
import matplotlib
# matplotlib.use('Qt5Agg')
import math
import csv
import random
import pyqtgraph as pg
import numpy as np
import pandas as pd
import sklearn as sk
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as font_manager

from xml.dom import minidom
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer, Binarizer, OneHotEncoder, Imputer, \
    PolynomialFeatures, FunctionTransformer
from sklearn.neighbors import NearestNeighbors

from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2
from sklearn.decomposition import PCA, FastICA
from sklearn import datasets
from scipy.stats import mode
from scipy.spatial.distance import *
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy as hc

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QMenu, QSizePolicy, QMessageBox, QWidget, QFileDialog, QAction, QLineEdit, \
    QApplication, QPushButton, QSlider, QLabel, QHBoxLayout, QVBoxLayout

from numpy import vstack, array, nan, mean, median, ptp, var, std, cov, corrcoef, arange, sin, pi
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import ttfFontProperty
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib import ft2font
from bs4 import BeautifulSoup



def stateval(data=np.ndarray):
    dict={'mean':mean(data),'ptp':ptp(data),'var':var(data),'std':std(data),'cv':mean(data)/std(data)}

    return(dict)

def relation(data1=np.ndarray,data2=np.ndarray):
    data=array([data1,data2])
    dict={'cov':cov(data,bias=1),'corrcoef':corrcoef(data)}
    return(dict)



prepath = '/Volumes/Virtual/FastTmp/'
path = 'Target'

df = pd.read_excel(prepath + '两组火山岩主量.xlsx')
# m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']
# for i in m:
#    df = df.drop(i, 1)
df.set_index('Label', inplace=True)

items=df.columns.values
y = df.index.values


StatResultDict={}

for i in items:

    StatResultDict[i]=stateval(df[i])

StdSortedList= sorted(StatResultDict.keys(), key=lambda x:StatResultDict[x]['std'])

StdSortedList.reverse()



for k in sorted(StatResultDict.keys(), key=lambda x:StatResultDict[x]['std']):
    print("%s=%s" % (k, StatResultDict[k]))



StatResultDf=pd.DataFrame.from_dict(StatResultDict,orient='index')

#StatResultDf=pd.DataFrame.from_dict(StatResultDict,orient='columns')

StatResultDf.to_excel('StatsResultDf.xlsx')


numpyMatrix = df.as_matrix()

newdf = pd.concat([df.SiO2 ,df.TFe2O3, df.CaO], axis=1)

X= newdf.as_matrix()




color=[]

#print(stateval(df.SiO2))
#print(relation(df.SiO2,df.Al2O3)['cov'])

for i in range(len(y)):

    if i==0:
        color.append('red')
    else:
        if y[i]==y[0]:
            color.append('red')

        else:
            color.append('blue')

index = df.index.values.tolist()
item = df.columns.values.tolist()


distance = []


minEtmp=euclidean(numpyMatrix[0],numpyMatrix[1])
maxEtmp=euclidean(numpyMatrix[0],numpyMatrix[1])

minCtmp=cosine(numpyMatrix[0],numpyMatrix[1])
maxCtmp=cosine(numpyMatrix[0],numpyMatrix[1])


minlabel=0
maxlabel=0


for i in range(len(y)):
    if i>0 and i< len(y)-1:
        Etmp = euclidean(numpyMatrix[i], numpyMatrix[i+1])
        Ctmp = cosine(numpyMatrix[i], numpyMatrix[i+1])

        if Etmp<=minEtmp:
            minEtmp=Etmp
            minlabel=i
        elif Etmp>= maxEtmp:
            maxEtmp=Etmp
            maxlabel=i

        if Ctmp <= minCtmp:
            minCtmp = Ctmp
        elif Ctmp >= maxCtmp:
            maxCtmp = Ctmp



color[minlabel]='grey'
color[maxlabel]='black'

print(minEtmp,maxEtmp,'\n',minCtmp,maxCtmp)

#distances = euclidean(df.SiO2, df.CaO)
#dist_matrix = squareform(distances)


#print(distances,'\n',dist_matrix)


            

x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

#X_reduced = PCA(n_components=3).fit_transform(numpyMatrix)
#X_reduced = FastICA(n_components=3).fit_transform(numpyMatrix)

fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)
#ax.scatter(X_reduced[:, 0], X_reduced[:,1], X_reduced[:, 2],c=color, alpha=0.4, cmap=plt.cm.Set1, edgecolor='blue', s=40)

ax.scatter(X[:, 0], X[:,1], X[:, 2],c=color, edgecolor='white', s=40)
ax.set_title("Tree Dimentional Distribution")
ax.set_xlabel("SiO2")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("TFe2O3")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("CaO")
ax.w_zaxis.set_ticklabels([])

#plt.show()

pg.plot(X[:, 0], X[:,1], X[:, 2])