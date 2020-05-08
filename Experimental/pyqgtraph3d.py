from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import pandas as pd
import pyqtgraph.opengl as gl
import numpy as np

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

pos = newdf.as_matrix()

xmin= min(df.SiO2)
xmax= max(df.SiO2)


ymin= min(df.Ratio)
ymax= max(df.Ratio)

zmin= min(df.CaO)
zmax= max(df.CaO)


xmean=np.mean(df.SiO2)
ymean=np.mean(df.Ratio)
zmean=np.mean(df.CaO)


ThreeDimView = gl.GLScatterPlotItem(pos=pos, color=(100, 255, 255, 88), size=0.1,pxMode=False)

x= df.SiO2.values
y= df.Ratio.values
z= df.CaO.values

x= [min(df.SiO2),max(df.SiO2)]

y= [min(df.Ratio),max(df.Ratio)]

z= [min(df.CaO),max(df.CaO)]

pts = np.vstack([x,y,z]).transpose()


line = gl.GLLinePlotItem(pos=pts, color=(100, 255, 255, 88), width=1, antialias=True)


w = gl.GLViewWidget()

w.pan(xmean,ymean,zmean)

w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')


## create three grids, add each to the view
xgrid = gl.GLGridItem()
ygrid = gl.GLGridItem()
zgrid = gl.GLGridItem()
w.addItem(xgrid)
w.addItem(ygrid)
w.addItem(zgrid)

## rotate x and y grids to face the correct direction
xgrid.rotate(90, 0, 1, 0)
ygrid.rotate(90, 1, 0, 0)

## scale each grid differently
xgrid.scale(12.8, 12.8, 12.8)
ygrid.scale(12.8, 12.8, 12.8)
zgrid.scale(12.8, 12.8, 12.8)

#xgrid.setTransform(xmean,ymean,zmean)


w.addItem(line)

w.addItem(ThreeDimView)



## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()