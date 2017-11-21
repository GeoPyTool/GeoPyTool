from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import pandas as pd



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



## Define a top-level widget to hold everything
window = QtGui.QWidget()

## Create some widgets to be placed inside
btn = QtGui.QPushButton('press me')
text = QtGui.QLineEdit('enter text')
listw = QtGui.QListWidget()
view = pg.PlotWidget()
view.addLegend()

view.plot(X[:, 0], X[:,1], pen=None, symbol='o', symbolPen=None, symbolSize=3, symbolBrush=(100, 255, 255, 88), name=y[0])

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
window.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(text, 1, 0)   # text edit goes in middle-left
layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
layout.addWidget(view, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
window.show()

## Start the Qt event loop
app.exec_()