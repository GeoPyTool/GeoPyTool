# coding:utf-8

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib
import scipy.stats as st

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

name ='xia.xls'
group = 100

LineColor='blue'
PointColor='red'




DensityColorMap='Blues'
DensityAlpha=0.3


DensityLineColor='grey'
DensityLineAlpha=0.3

df = pd.read_excel(name)

x = df.SiO2
y = df.Ratio



#####################################


xtouse = x.values
ytouse = y.values

XtoFit = []
YtoFit = []

for i in range(len(x.values)):
    if x.values[i] < 60:
        XtoFit.append(x.values[i])
        YtoFit.append(y.values[i])

z = np.polyfit(YtoFit, XtoFit, 3)

Yline = np.linspace(min(YtoFit), max(YtoFit), 30)
p = np.poly1d(z)
Xline = p(Yline)

newXline = []



xmin, xmax = min(x), max(x)
ymin, ymax = min(y), max(y)

# Peform the kernel density estimate
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([x, y])
kernel = st.gaussian_kde(values)
f = np.reshape(kernel(positions).T, xx.shape)

fig = plt.figure()
ax = fig.gca()
# Contourf plot
cfset = ax.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
## Or kernel density estimate plot instead of the contourf plot
# ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
# Contour plot
cset = ax.contour(xx, yy, f, colors=DensityLineColor , alpha=DensityLineAlpha)
# Label plot
ax.clabel(cset, inline=1, fontsize=10)

#####################################


plt.plot(Xline, Yline, 'b-')

alphatouse = []

for i in range(len(xtouse)):
    tmp = abs(p(ytouse[i]) - xtouse[i])
    alphatouse.append(tmp)

a = []

step = abs(min(alphatouse) - max(alphatouse)) / group

for i in alphatouse:
    if min(alphatouse) <= i < min(alphatouse) + step:
        a.append(0.8)
    elif min(alphatouse) + step <= i < min(alphatouse) + 2 * step:
        a.append(0.6)
    elif min(alphatouse) + 2 * step <= i < min(alphatouse) + 3 * step:
        a.append(0.4)
    else:
        a.append(0.2)


for i in range(len(xtouse)):
    plt.scatter(xtouse[i], ytouse[i], label='', s=3, color='red', alpha=a[i])

plt.show()