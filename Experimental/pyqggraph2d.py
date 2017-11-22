from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import pandas as pd
import numpy as np
import scipy.stats as st
from PIL import Image

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])



prepath = '/Volumes/Virtual/FastTmp/'
path = 'Target'
df = pd.read_excel(prepath + 'XiaYing-SiO2-FeMg.xlsx')
# m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']
# for i in m:
#    df = df.drop(i, 1)
df.set_index('Label', inplace=True)

items=df.columns.values
y = df.index.values
numpyMatrix = df.as_matrix()
newdf = pd.concat([df.SiO2 ,df.Ratio, df.CaO], axis=1)
X= newdf.as_matrix()
XtoFit=X[:, 0]
YtoFit=X[:, 1]
z = np.polyfit(YtoFit, XtoFit, 4)
Yline = np.linspace(min(YtoFit), max(YtoFit), 30)
p = np.poly1d(z)
Xline = p(Yline)

xmin, xmax = min(XtoFit)*0.9, max(XtoFit)*1.1
ymin, ymax = min(YtoFit)*0.9, max(YtoFit)*1.1
DensityColorMap = 'Blues'
DensityAlpha = 0.3
DensityLineColor = 'grey'
DensityLineAlpha = 0.3
# Peform the kernel density estimate
xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([XtoFit, YtoFit])
kernel = st.gaussian_kde(values)
f = np.reshape(kernel(positions).T, xx.shape)


data = f




view = pg.PlotWidget()
view.addLegend()


img = pg.ImageItem(data)

## generate empty curves
curves = []


levels = np.linspace(data.min(), data.max(), 10)
for i in range(len(levels)):
    v = levels[i]
    ## generate isocurve with automatic color selection
    c = pg.IsocurveItem(level=v, pen=(i, len(levels) * 1.5))
    c.setParentItem(img)  ## make sure isocurve is always correctly displayed over image
    c.setZValue(10)
    curves.append(c)



imgLevels = (data.min(), data.max()*2 )

img.setImage(data, levels=imgLevels)

img.setScaledMode()

for c in curves:
    c.setData(data)

TargetWidth  = img.width()
TargetHeight = img.height()

OriginalWidth= abs(xmax - xmin)
OriginalHeight= abs(ymax - ymin)

xscale= TargetWidth/OriginalWidth
yscale= TargetHeight/OriginalHeight


XtoFitUsed=[]
YtoFitUsed=[]

XlineUsed=[]
YlineUsed=[]

'''
for i in range(len(XtoFit)):
    XtoFitUsed.append(xmin+(XtoFit[i]-xmin)*xscale)
    YtoFitUsed.append(ymin+(YtoFit[i]-ymin)*yscale)
'''



for i in range(len(XtoFit)):
    XtoFitUsed.append((XtoFit[i]-xmin)*xscale)
    YtoFitUsed.append((YtoFit[i]-ymin)*yscale)

for i in range(len(Xline)):
    XlineUsed.append((Xline[i] - xmin) * xscale)
    YlineUsed.append((Yline[i] - ymin) * yscale)

view.addItem(img)
#view.plot(XtoFit, YtoFit, pen=None, symbol='o', symbolPen=None, symbolSize=3, symbolBrush=(100, 255, 255, 48), name=y[0])
#view.plot(Xline, Yline, pen='b')


view.plot(XtoFitUsed, YtoFitUsed, pen=None, symbol='o', symbolPen=None, symbolSize=3, symbolBrush=(100, 255, 255, 48), name=y[0])
view.plot(XlineUsed, YlineUsed, pen='b')


view.show()

## Start the Qt event loop
app.exec_()