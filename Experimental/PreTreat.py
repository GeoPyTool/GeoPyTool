# coding:utf-8

import math
import sys
import os
import csv
import random
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import matplotlib
import scipy.stats as st

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import ft2font
from matplotlib.font_manager import ttfFontProperty

import matplotlib.font_manager as font_manager
import matplotlib.image as mpimg

from pandas.plotting import radviz
from sklearn.neighbors import KNeighborsRegressor


def Del(prepath='/Volumes/Virtual/FastTmp/', path='raw', name='test.txt', head=3, end=-2):
    lines = open(path + '/' + name, 'r', encoding='windows-1252').readlines()
    open(prepath + 'new' + path + '/' + 'new' + name, 'w', encoding='utf-8').writelines(lines[head:end])


def OldJoin(prepath='/Volumes/Virtual/FastTmp/', path='Raw'):
    SourceList = os.listdir(path)
    for i in SourceList:
        if 'csv' in i and 'new' not in i and i[0] != '.':
            Del(prepath=prepath, path=path, name=i, head=3, end=-2)

    TargetList = []
    for i in SourceList:
        if 'csv' in i:
            df = pd.read_csv(prepath + 'new' + path + '/' + 'new' + i)

            TargetList.append(df)

    result = pd.concat(TargetList)

    result.reindex()

    result.to_csv(prepath + 'result.csv', sep=',', encoding='utf-8')

    return (result)


def Join(prepath='/Volumes/Virtual/FastTmp/', path='Excel', name='result'):
    SourceList = os.listdir(prepath + path)
    TargetList = []
    for i in SourceList:

        if 'csv' in i and '~' not in i and i[0] != '.':

            print(prepath + path + '/' + i)

            try:
                df = pd.read_csv(prepath + path + '/' + i)
            except():
                pass

        elif 'xls' in i and '~' not in i and i[0] != '.':
            try:
                df = pd.read_excel(prepath + path + '/' + i)
            except():
                pass

            TargetList.append(df)

    result = pd.concat(TargetList)

    result.reindex()

    result.to_excel(prepath + name + '.xlsx', encoding='utf-8')

    return (result)


def CsvToExcel(name='result'):
    if 'csv' in name and '~' not in name and name[0] != '.':
        df = pd.read_csv(name)
        df.to_excel('new' + name[0:-4] + '.xlsx', encoding='utf-8')
    pass


def ExcelToCsv(name='result'):
    if 'xls' in name and '~' not in name and name[0] != '.':
        df = pd.read_excel(name)
        df.to_csv('new' + name[0:-5] + '.csv', sep=',', encoding='utf-8')
    pass


prepath = '/Volumes/Virtual/FastTmp/'
path = 'Target'

df = pd.read_excel(prepath + 'XiaYing-SiO2-FeMg.xlsx')

# m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']

# for i in m:
#    df = df.drop(i, 1)

df.set_index('Label', inplace=True)

newdf = pd.concat([df.SiO2, df.Ratio], axis=1)

numpyMatrix = df.as_matrix()

# X = numpyMatrix[:, :3]  # we only take the first two features.
# y = df.index


X = numpyMatrix

y = df.index

color = []

for i in range(len(y)):
    if i == 0:
        color.append(1)
    else:
        if y[i] == y[0]:
            color.append(1)
        else:
            color.append(2)

# x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
# y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5

X_reduced = PCA(n_components=5).fit_transform(numpyMatrix)

df = pd.read_excel(prepath + 'XiaYing-SiO2-FeMg.xlsx')
df.set_index('Label', inplace=True)
x = df.SiO2
y = df.Ratio

xtouse = x.values
ytouse = y.values



XtoFit=[]
YtoFit=[]

for i in range(len(x.values)):
    if x.values[i] < 60:
        XtoFit.append(x.values[i])
        YtoFit.append(y.values[i])




z = np.polyfit(YtoFit, XtoFit, 3)

Yline = np.linspace(min(YtoFit), max(YtoFit), 30)
p = np.poly1d(z)
Xline = p(Yline)

newXline = []


#####################################



xmin,xmax = min(x),max(x)
ymin,ymax = min(y),max(y)

# Peform the kernel density estimate
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([x, y])
kernel = st.gaussian_kde(values)
f = np.reshape(kernel(positions).T, xx.shape)

fig = plt.figure()
ax = fig.gca()
# Contourf plot
cfset = ax.contourf(xx, yy, f, cmap='Blues',alpha=0.3)
## Or kernel density estimate plot instead of the contourf plot
#ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
# Contour plot
cset = ax.contour(xx, yy, f, colors='k',alpha=0.3)
# Label plot
ax.clabel(cset, inline=1, fontsize=10)








#####################################


plt.plot(Xline, Yline, 'b-')

alphatouse = []

leveldistance=[]

for i in range(len(xtouse)):
    tmp = abs(p(ytouse[i]) - xtouse[i])
    leveldistance.append(tmp)
    alphatouse.append(tmp)

a = []

group= 100


step= abs(min(alphatouse)-max(alphatouse))/group

for i in alphatouse:
    if min(alphatouse)<=i<min(alphatouse)+step:
        a.append(0.8)
    elif min(alphatouse)+step<=i<min(alphatouse)+2*step:
        a.append(0.6)
    elif min(alphatouse)+2*step<=i<min(alphatouse)+3*step:
        a.append(0.4)
    else:
        a.append(0.2)
    



#plt.scatter(x, y, label='', s=3, color='red', alpha=a)


for i in range(len(xtouse)):
    plt.scatter(xtouse[i], ytouse[i], label='', s=3, color='red', alpha=a[i])
    pass

#fig = plt.figure(1, figsize=(8, 6))
# ax = Axes3D(fig, elev=-150, azim=110)


# plt.scatter(X_reduced[:, 1], X_reduced[:, 2], c=color, cmap=plt.cm.Set1, edgecolor='k', s=40)

# plt.scatter(x, y, label='', s=3, color='blue', alpha=0.3)

# z= np.polyfit(x, y, 2)



# ax.set_title("First three PCA directions")
# ax.set_xlabel("SiO2")
# ax.w_xaxis.set_ticklabels([])
# ax.set_ylabel("TFeO")
# ax.w_yaxis.set_ticklabels([])
# ax.set_zlabel("MgO")
# ax.w_zaxis.set_ticklabels([])











plt.show()

tm=Join(path='塔木兰沟组',name='新塔木兰沟')


'''
SourceList = os.listdir(prepath + path)
TargetList = []
for i in SourceList:
    ExcelToCsv(path='塔木兰沟组',name=i)


#df = pd.read_excel(prepath+"塔木兰沟组数据交集.xlsx",keep_default_na=False, na_values=[""])
#tm=Join(path='Target',name='满克头鄂博组数据交集')

#DataToPlot = pd.read_excel(prepath+'result.xlsx')
#DataToPlot.plot()
#DataToPlot.plot.area()
#plt.figure()
#radviz(DataToPlot , 'Ag109')
#plt.show()




# created by Huang Lu
# 27/08/2016 17:05:45 
# Department of EE, Tsinghua Univ.

import cv2
import numpy as np

cap = cv2.VideoCapture(1)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 






for i in alphatouse:
    #tmp = - np.power(np.e,i / max(alphatouse))
    #tmp = 1- np.power(i / max(alphatouse),2)


    tmp = np.power(np.e,i)
    a.append(tmp)

'''




