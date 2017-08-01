import math
import sys
import csv
import random
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 'truetype'

import pandas as pd
import numpy as np
from numpy import arange, sin, pi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)
class Tool():
    def TriToBin(self, x, y, z):

        """
        Turn an x-y-z triangular coord to an a-b coord.
        if z is negative, calc with its abs then return (a, -b).
        :param x,y,z: the three numbers of the triangular coord
        :type x,y,z: float or double are both OK, just numbers
        :return:  the corresponding a-b coord
        :rtype:   a tuple consist of a and b
        """

        if (z >= 0):
            if (x + y + z == 0):
                return (0, 0)
            else:
                Sum = x + y + z
                X = 100.0 * x / Sum
                Y = 100.0 * y / Sum
                Z = 100.0 * z / Sum
                if (X + Y != 0):
                    a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
                else:
                    a = Z / 2.0
                b = Z / 2.0 * (np.sqrt(3))
                return (a, b)
        else:
            z = abs(z)
            if (x + y + z == 0):
                return (0, 0)
            else:
                Sum = x + y + z
                X = 100.0 * x / Sum
                Y = 100.0 * y / Sum
                Z = 100.0 * z / Sum
                if (X + Y != 0):
                    a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
                else:
                    a = Z / 2.0
                b = Z / 2.0 * (np.sqrt(3))
                return (a, -b)

    def BinToTri(self, a, b):

        """
        Turn an a-b coord to an x-y-z triangular coord .
        if z is negative, calc with its abs then return (a, -b).
        :param a,b: the numbers of the a-b coord
        :type a,b: float or double are both OK, just numbers
        :return:  the corresponding x-y-z triangular coord
        :rtype:   a tuple consist of x,y,z
        """

        if (b >= 0):
            y = a - b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a + b / np.sqrt(3))
            return (x, y, z)
        else:
            y = a + b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a - b / np.sqrt(3))
            return (x, y, z)

    def Cross(self, A=[(0, 0), (10, 10)], B=[(0, 10), (100, 0)]):

        """
        Return the crosspoint of two line A and B.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return: the crosspoint of A and B
        :rtype: a list consist of two numbers, the x-y of the crosspoint
        """

        x0, y0 = A[0]
        x1, y1 = A[1]
        x2, y2 = B[0]
        x3, y3 = B[1]

        b1 = (y1 - y0) / (x1 - x0)
        b2 = (y3 - y2) / (x3 - x2)
        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        return ([x, y])

    def TriCross(self, A=[(100, 0, 0), (0, 50, 60)], B=[(50, 50, 0), (0, 0, 100)]):

        """
        Return the crosspoint of two line A and B in triangular coord.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return:  the crosspoint of A and B
        :rtype:   a list consist of three numbers, the x-y-z of the triangular coord
        """

        x0, y0 = self.TriToBin(A[0][0], A[0][1], A[0][2])
        x1, y1 = self.TriToBin(A[1][0], A[1][1], A[1][2])
        x2, y2 = self.TriToBin(B[0][0], B[0][1], B[0][2])
        x3, y3 = self.TriToBin(B[1][0], B[1][1], B[1][2])

        b1 = (y1 - y0) / (x1 - x0)
        b2 = (y3 - y2) / (x3 - x2)
        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        result = self.BinToTri(x, y)
        return (result)

    def Fill(self, P=[(100, 0), (85, 15), (0, 3)], Color='blue', Alpha=0.3):

        """
        Fill a region in planimetric rectangular coord.
        :param P: the peak points of the region in planimetric rectangular coord
        :type P: a list consist of at least three tuples, which are the points in planimetric rectangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        """
        a = []
        b = []

        for i in P:
            a.append(i[0])
            b.append(i[1])

        return (a, b)

    def TriFill(self, P=[(100, 0, 0), (85, 15, 0), (0, 3, 97)], Color='blue', Alpha=0.3):

        """
         Fill a region in triangular coord.
        :param P: the peak points of the region in triangular coord
        :type P: a list consist of at least three tuples, which are the points in triangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        """

        a = []
        b = []

        for i in P:
            a.append(self.TriToBin(i[0], i[1], i[2])[0])
            b.append(self.TriToBin(i[0], i[1], i[2])[1])

        return (a, b)
        #plt.fill(a, b, Color=Color, Alpha=Alpha, )

class Point():
    """
    a Point class
    :param X,Y: the values of its x-y coord
    :type X,Y: two float numbers
    :param Location: gather X and Y as a tuple for further use
    :type Location: just a tuple with two numbers
    :param Size: the size of the Point to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Point to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Point
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Point, telling what it is and distinguish it from other points
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    """

    X = 0
    Y = 0
    Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''

    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        """
        just set up the values
        """
        super().__init__()
        self.X = X
        self.Y = Y
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

class Points():
    """
    a class for multiple Points
    :param X,Y: the values of its x-y coords
    :type X,Y: two lists consist of float numbers
    :param Size: the size of the Points to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Points to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Points
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Points
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Points, telling what they are and distinguish them from other points
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    """

    X = []
    Y = []
    # Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''
    FontSize = 8

    def __init__(self, points=[(0, 0), (0, 1)], Size=12, Color='red', Alpha=0.3, Marker='o', Label='', FontSize=8):
        """
        just set up the values
        """
        super().__init__()
        self.X = []
        self.Y = []
        for i in points:
            self.X.append(i[0])
            self.Y.append(i[1])
        # self.Location = (self.X, self.Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label
        self.FontSize = FontSize

class Tag():
    """
    a class for Tag put on canvas
    :param Label: label of the Tag, telling what it is and distinguish them from other tags
    :type Label: a strings , if leave as "" or '' such kind of blank string, the label will not show on canvas
    :param Location: the location of the Tag
    :type Location: a tuple consist of x-y values of its coords
    :param X_offset,Y_offset: the values of its x-y offsets on coords
    :type X_offset,Y_offset: two float numbers
    :param FontSize: the size of font of the Tag
    :type FontSize: a number , int or maybe float also OK , better around 8 to 12, not too large or too small
    """

    Label = u'Label'
    Location = (0, 0)
    X_offset = -6
    Y_offset = 3
    FontSize = 12

    def __init__(self, Label=u'Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=12):
        """
        set up the values
        """

        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class Line():
    """
    a line class
    :param Begin: the Beginning point of the line
    :type Begin: a Point Instance
    :param End: the End point of the line
    :type End: a Point Instance
    :param Points: gathering all the Point Instances
    :type Points: a list
    :param X,Y: the gathered x and y values of the line to use in plotting
    :type X,Y: two lists containing float numbers
    :param Width: the width of the line
    :type Width: an int number , mayby float is OK
    :param Color: the color of the Line to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Style: the style used for the Line
    :type Style: a string; -, --,-., : maybe there would be some other types , from matplotlib
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Label: label of the Line, telling what it is and distinguish it from other lines
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    :param Sort: the sequence used for sorting the points consisting the line
    :type Sort: a string, x means sort the points with their x values, y means use y instead of x, other means use the sequence of points as these points are put to the line
    """

    Begin = Point(0, 0)
    End = Point(1, 1)
    Points = []
    X = [Begin.X, End.X]
    Y = [Begin.Y, End.Y]
    Width = 1
    Color = 'blue'
    Style = "-"
    Alpha = 0.3
    Label = ''
    Sort = ''

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style="-", Alpha=0.3, Label=''):
        """
        setup the datas
        """
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):
            self.X = [Points[0][0], Points[1][0]]
            self.Y = [Points[0][1], Points[1][1]]
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

        else:
            print("Cannot draw line with one point")

    def sequence(self):
        """
        sort the points in the line with given option
        """
        if (len(self.Points[0]) == 2):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            else:
                self.order(self.Points)

        if (len(self.Points[0]) == 3):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            elif (self.Sort == 'Z' or self.Sort == 'Z'):
                self.Points.sort(key=lambda x: x[2])
                self.order(self.Points)
            else:
                self.order(self.Points)

    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
        self.X = X_TMP
        self.Y = Y_TMP

class TriTag(Tag, Tool):
    """
    inherit Tag and Tool,a Tag for triangular coord
    """

    def __init__(self, Label=u'Label', Location=(0, 1, 2), X_offset=-6, Y_offset=3, FontSize=12):
        """
        set up the values, transfer x,y,z coords to x-y coords
        """

        self.Label = Label
        self.Location = self.TriToBin(Location[0], Location[1], Location[2])
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class TriPoint(Point, Tool):
    """
    inherit Point and Tool, a Point class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    :param sum: a value used in calc of coord transfer
    :type sum: just a number, both int or float are OK
    """
    x = 0
    y = 0
    z = 0
    sum = 1

    def __init__(self, P=(10, 20, 70), Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        super().__init__()

        self.sum = P[0] + P[1] + abs(P[2])
        self.x = P[0] * 100 / self.sum
        self.y = P[1] * 100 / self.sum
        self.z = P[2] * 100 / self.sum

        self.Location = P
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

        self.X, self.Y = self.TriToBin(self.x, self.y, self.z)

class TriLine(Line, Tool):
    """
    inherit Line and Tool, line class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    """
    x = []
    y = []
    z = []

    X = []
    Y = []

    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', Style="-", Alpha=0.3, Label=''):
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):

            TriPoint(Points[0])

            self.x = [Points[0][0], Points[1][0]]
            self.y = [Points[0][1], Points[1][1]]
            self.z = [Points[0][2], Points[1][2]]
            self.tritrans()
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

            for i in Points:
                self.x.append(i[0])
                self.y.append(i[1])
                self.z.append(i[2])

        else:
            print("Cannot draw line with one point")



        self.sequence()
        self.tritrans()

    def tritrans(self):
        self.X = []
        self.Y = []
        for i in range(len(self.x)):
            self.X.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[0])
            self.Y.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[1])

    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        Z_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
            Z_TMP.append(i[2])
        self.x = X_TMP
        self.y = Y_TMP
        self.z = Z_TMP

class PandasModel(QtCore.QAbstractTableModel):

    _df= pd.DataFrame()
    _changed= False
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._changed= False

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    """
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))


    """
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            try:
                row = index.row()
                col = index.column()
                name = self._struct[col]['name']
                return self._data[row][name]
            except:
                pass
        elif role == QtCore.Qt.CheckStateRole:
            return None

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    """
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = index.row()
        col = index.column()
        name = self._struct[col]['name']
        self._data[row][name] = value
        self.emit(QtCore.SIGNAL('dataChanged()'))
        return True
    """
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        self._changed = True
        #self.emit(QtCore.SIGNAL('dataChanged()'))
        return True


    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class CustomQTableView(QtWidgets.QTableView):
    def __init__(self, *args):
        super().__init__(*args)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                             QtWidgets.QAbstractItemView.DoubleClicked)

    def keyPressEvent(self, event): #Reimplement the event here, in your case, do nothing
        return

class PlotModel(FigureCanvas):
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""

    _df= pd.DataFrame()
    _changed= False
    def __init__(self,parent=None, width=100, height=100, dpi=100,description = ""
                 ,tag = "",xlabel = r'$X$',ylabel = r'$Y$',xlim=(30,90),ylim=(0,20)):

        self.fig = Figure(figsize=(width, height), dpi=dpi)


        self.axes = self.fig.add_subplot(111, xlabel =xlabel +'\n'+description, ylabel = ylabel,xlim=xlim,ylim=ylim)
        # 设定横纵坐标轴的标签

        #每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        #self.axes.hold(False)




        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)





    def DrawLine(self,l=[(41, 0), (41, 3), (45, 3)] ,color= 'grey', linewidth=0.5, linestyle= '-', linelabel = '', alpha= 0.5 ):
        x=[]
        y=[]
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y,color = color, linewidth = linewidth, linestyle = linestyle , label = linelabel , alpha = alpha)
        return(x,y)




    def TAS(self,df = pd.DataFrame(),Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
                 Top=19, Y0=1,Y1=19, Y_Gap=19, FontSize=12,xLabel=r'$SiO_2 wt\%$', yLabel=r'$na_2O + K_2O wt\%$'):

        PointLabels=[]
        x=[]
        y=[]

        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])
        self.DrawLine([(41.75, 1), (52.5, 5)])
        #self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        #self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        #self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = "TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith"
        tag = "tas-Wilson1989-volcano"



        if(len(df)>0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size=df.at[i, 'Size']
                Color=df.at[i, 'Color']

                print(Color,df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha=df.at[i, 'Alpha']
                Marker=df.at[i, 'Marker']
                Label=TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']),marker=df.at[i, 'Marker'], s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'],label=TmpLabel, edgecolors='black')


            #self.axes.savefig('tas.png', dpi=300, bbox_inches='tight')
            #self.axes.savefig('tas.svg', dpi=300, bbox_inches='tight')
            #self.axes.savefig('tas.pdf', dpi=300, bbox_inches='tight')
            #self.axes.savefig('tas.eps', dpi=300, bbox_inches='tight')
            #self.axes.show()

            self.draw()



    def TASv(self,df = pd.DataFrame(),Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
                 Top=19, Y0=1,Y1=19, Y_Gap=19, FontSize=12,xlabel=r'$SiO_2 wt\%$', ylabel=r'$na_2O + K_2O wt\%$',width=12, height=12, dpi=300,xlim=(30,90),ylim=(0,20)):


        PointLabels=[]
        x=[]
        y=[]



        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]



        X_offset = -6
        Y_offset = 3

        TagNumber=min(len(Labels),len(Locations))

        for k in range(TagNumber):
            self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                               textcoords='offset points',
                               fontsize=8, color='grey', alpha=0.8)




        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])
        #self.DrawLine([(41.75, 1), (52.5, 5)])
        #self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        #self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        #self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = "TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith"
        tag = "tas-Wilson1989-volcano"



        if(len(df)>0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size=df.at[i, 'Size']
                Color=df.at[i, 'Color']

                print(Color,df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha=df.at[i, 'Alpha']
                Marker=df.at[i, 'Marker']
                Label=TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']),marker=df.at[i, 'Marker'], s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'],label=TmpLabel, edgecolors='black')


            xLabel = r'$SiO_2 wt\%$' +'\n'+description
            yLabel = r'$na_2O + K_2O wt\%$'
            #self.axes.xlabel(xLabel, fontsize=12)

            self.draw()

class MyPopup(QWidget):

    _df= pd.DataFrame()
    _changed= False

    def __init__(self,width=100, height=100, dpi=100, description = "TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith"
        , tag = "tas-Wilson1989-volcano", xlabel = r'$SiO_2 wt\%$', ylabel = r'$Na_2O + K_2O wt\%$', xlim = (30,
                                                                                                             90), ylim = (
        0, 20)):
        QWidget.__init__(self)

        self.initUI()

        self.MyCanvas = PlotModel(self, width=width, height=height, dpi=dpi, description = description, tag = tag, xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim)


        self.MyCanvas.setGeometry(QtCore.QRect(10, 10, 512, 512))


        self.MyCanvas.setObjectName("MyCanvas")


    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.MyCanvas.print_figure(ImgFileOutput, dpi= 300 )



    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Save Image', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(256, 550)
        btn.clicked.connect(self.saveImgFile)

        #self.setGeometry(500, 500, 500, 600)
        self.setWindowTitle('Image')

class Zircon(QMainWindow):

    _df= pd.DataFrame()
    _changed= False

    ylabel = r'Ln D $Zircon/Rock%$'

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Oxygen Fugacity Estimation by Ce(IV)/Ce(III) in Zircon (Ballard et al. 2002)')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved")

        self.create_main_frame()
        self.create_status_bar()

        self.raw=self._df

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()



        self.PointLabels = []

        self.Base = 0
        self.Zircon = []
        self.Elements = []
        self.Elements3 = []
        self.Elements3_Plot_Only = []
        self.Elements4 = []
        self.x = []
        self.x3 = []
        self.x3_Plot_Only = []
        self.x4 = []
        self.y = []
        self.y3 = []
        self.y3_Plot_Only = []
        self.y4 = []
        self.z3 = []
        self.z4 = []
        self.xCe3 = []
        self.yCe3 = []
        self.xCe4 = []
        self.yCe4 = []
        self.Ce3test = []
        self.DCe3test = []
        self.Ce4test = []
        self.DCe4test = []
        self.Ce4_3_Ratio = []

        self.ZirconCe = []

        self.DataToWrite = [["First", "Second", "Third"]]


    def save_plot(self):
        file_choices = "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)"

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100

        self.fig1 = Figure((8, 6), dpi=self.dpi)
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.setParent(self.main_frame)
        self.axes1 = self.fig1.add_subplot(111)
        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.main_frame)


        self.fig2 = Figure((8, 6), dpi=self.dpi)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.setParent(self.main_frame)
        self.axes2 = self.fig2.add_subplot(111)
        self.mpl_toolbar2 = NavigationToolbar(self.canvas2, self.main_frame)

        # Other GUI controls
        self.save_button1 = QPushButton("&Save Ce3 Figure")
        self.save_button1.clicked.connect(self.saveImgFile1)

        self.save_button2 = QPushButton("&Save Ce4 Figure")
        self.save_button2.clicked.connect(self.saveImgFile2)

        self.save_button3 = QPushButton("&Save Result")
        self.save_button3.clicked.connect(self.saveResult)

        self.detail_cb = QCheckBox("&Detail")
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.MultiBallard)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button3,self.detail_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar1)
        self.vbox.addWidget(self.save_button1)
        self.vbox.addWidget(self.canvas1)

        self.vbox.addWidget(self.mpl_toolbar2)
        self.vbox.addWidget(self.save_button2)
        self.vbox.addWidget(self.canvas2)

        self.vbox.addLayout(self.hbox)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveImgFile1(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas1.print_figure(ImgFileOutput, dpi= 300 )

    def saveImgFile2(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "C:/",
                                                         "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas2.print_figure(ImgFileOutput, dpi= 300)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "Excel Files (*.xlsx);;CSV Files (*.csv)")  # 数据文件保存输出

        if(DataFileOutput !=''):

            if ("csv" in DataFileOutput):self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ("xls" in DataFileOutput):self.newdf.to_excel(DataFileOutput, encoding='utf-8')


    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def MultiBallard(self):

        self.axes1.clear()
        self.axes2.clear()



        self.raw=self._df

        self.RockCe = self.raw.at[4, 'Ce']

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()



        self.PointLabels = []

        self.Base = 0
        self.Zircon = []
        self.Elements = []
        self.Elements3 = []
        self.Elements3_Plot_Only = []
        self.Elements4 = []
        self.x = []
        self.x3 = []
        self.x3_Plot_Only = []
        self.x4 = []
        self.y = []
        self.y3 = []
        self.y3_Plot_Only = []
        self.y4 = []
        self.z3 = []
        self.z4 = []
        self.xCe3 = []
        self.yCe3 = []
        self.xCe4 = []
        self.yCe4 = []
        self.Ce3test = []
        self.DCe3test = []
        self.Ce4test = []
        self.DCe4test = []
        self.Ce4_3_Ratio = []

        self.ZirconCe = []


        for i in range(len(self.raw)):
            if (self.raw.at[i, "DataType"] == "Base"):
                self.Base = i
            elif (self.raw.at[i, "DataType"] == "Zircon"):
                self.Zircon.append(i)



        for j in self.b:
            if (j == 'Ce'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):


                    self.xCe3.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
            elif (j == 'Ce4'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 4):
                    self.xCe4.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))

            elif (self.raw.at[1, j] == 'yes'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements3.append(j)

                elif (self.raw.at[0, j] == 4):
                    self.x4.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements4.append(j)
                    self.Elements.append(j)

            elif (self.raw.at[1, j] == 'no'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3_Plot_Only.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements3_Plot_Only.append(j)
                    self.Elements.append(j)


        for i in self.Zircon:
            self.ZirconCe.append(self.raw.at[i, 'Ce'])
            tmpy3 = []
            tmpy4 = []
            tmpy3_Plot_Only = []

            for j in self.b:
                if (j == 'Ce'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe3.append(ytemp)
                elif (j == 'Ce4'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe4.append(ytemp)
                elif (self.raw.at[1, j] == 'yes'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3.append(ytemp)

                    elif (self.raw.at[0, j] == 4):
                        tmpy4.append(ytemp)
                elif (self.raw.at[1, j] == 'no'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3_Plot_Only.append(ytemp)
            self.y3.append(tmpy3)
            self.y4.append(tmpy4)
            self.y3_Plot_Only.append(tmpy3_Plot_Only)

        for k in range(len(self.y3)):

            tmpz3 = np.polyfit(self.x3, self.y3[k], 1)
            self.z3.append(tmpz3)

            for i in range(len(self.x3)):
                x, y = self.x3[i], self.y3[k][i]


                self.axes1.scatter(x, y, s=3, color='blue', alpha=0.5,label='', edgecolors='black')


            if k == 0:
                for i in range(len(self.x3)):
                    self.axes1.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]),fontsize=8, xytext=(10, 25),
                                 textcoords='offset points',
                                 ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))



        for i in self.z3:
            Xline3 = np.linspace(min(self.x3), max(max(self.x3_Plot_Only), max(self.x3)), 30)
            p3 = np.poly1d(i)
            Yline3 = p3(Xline3)

            self.axes1.plot(Xline3,Yline3, 'b-')

            self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.RockCe))[0])
            self.DCe3test.append(np.power(np.e, p3(self.xCe3))[0])

        for k in range(len(self.yCe3)):

            x, y = self.xCe3, self.yCe3[k]

            self.axes1.scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes1.annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)),fontsize=8, xytext=(10, 25), textcoords='offset points',
                             ha='right',
                             va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y3_Plot_Only)):

            for i in range(len(self.x3_Plot_Only)):
                x, y = self.x3_Plot_Only[i], self.y3_Plot_Only[k][i]
                self.axes1.scatter(x, y, label='', s=3, color='blue', alpha=0.3)

            if k == 0:
                for i in range(len(self.x3_Plot_Only)):
                    self.axes1.annotate(self.Elements3_Plot_Only[i], xy=(self.x3_Plot_Only[i], self.y3_Plot_Only[0][i]),fontsize=8,
                                 xytext=(10, -25),
                                 textcoords='offset points', ha='right', va='bottom',
                                 bbox=dict(boxstyle='round,pad=0.5', fc='green', alpha=0.2),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))


        for k in range(len(self.y3)):

            tmpz3 = np.polyfit(self.x3, self.y3[k], 1)
            self.z3.append(tmpz3)

            for i in range(len(self.x3)):
                x, y = self.x3[i], self.y3[k][i]

                self.axes1.scatter(x, y, label='', s=3, color='blue', alpha=0.3)

            if k == 0:
                for i in range(len(self.x3)):
                    self.axes1.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]),fontsize=8, xytext=(10, 25),
                                 textcoords='offset points',
                                 ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z3:
            Xline3 = np.linspace(min(self.x3), max(max(self.x3_Plot_Only), max(self.x3)), 30)
            p3 = np.poly1d(i)
            Yline3 = p3(Xline3)
            self.axes1.plot(Xline3, Yline3, 'b-')

            self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.RockCe))[0])
            self.DCe3test.append(np.power(np.e, p3(self.xCe3))[0])

        for k in range(len(self.yCe3)):

            x, y = self.xCe3, self.yCe3[k]
            self.axes1.scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes1.annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), fontsize=8,xytext=(10, 25), textcoords='offset points',
                             ha='right',
                             va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))



        for k in range(len(self.y4)):

            tmpz4 = np.polyfit(self.x4, self.y4[k], 1)
            self.z4.append(tmpz4)

            for i in range(len(self.x4)):
                x, y = self.x4[i], self.y4[k][i]
                self.axes2.scatter(x, y, label='', s=3, color='r', alpha=0.5)

            if k == 0:
                for i in range(len(self.x4)):
                    self.axes2.annotate(self.Elements4[i], xy=(self.x4[i], self.y4[0][i]), fontsize=8,xytext=(10, 25),
                                 textcoords='offset points',
                                 ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z4:
            Xline4 = np.linspace(min(self.x4), max(self.x4), 30)
            p4 = np.poly1d(i)
            Yline4 = p4(Xline4)
            self.axes2.plot(Xline4, Yline4, 'r-')

            self.Ce4test.append(np.power(np.e, p4(self.xCe4) + np.log(self.RockCe))[0])
            self.DCe4test.append(np.power(np.e, p4(self.xCe4))[0])

        for k in range(len(self.yCe4)):

            x, y = self.xCe4, self.yCe4[k]
            self.axes2.scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes2.annotate('Ce4', xy=(self.xCe4[k], max(self.yCe4)),fontsize=8, xytext=(10, 25), textcoords='offset points',
                             ha='right',
                             va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))


        DataToWrite = [
            ["Zircon Sample Label", "Zircon Ce4_3 Ratio", "Melt Ce4_3 Ratio", "DCe4", "DCe3", "DCe Zircon/Melt"], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], "Label"]
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        ylabel = r'Ln D $Zircon/Rock%$'

        xlimleft3 = 0
        xlimleft4 = -0.005


        print("\n the value is ",min(min(self.y3)))



        ylimleft3 = min(min(min(self.y3)),min(min(self.y3_Plot_Only)))

        ylimleft4 = min(min(min(self.y4)),min(min(self.yCe4),min(self.yCe3)))

        xlimright3 = 0.06
        xlimright4 = 0.03

        ylimright3 = max(max(self.y3))
        ylimright4 = max(max(self.y4))


        if (self.detail_cb.isChecked()):


            self.axes1.plot((xlimleft3, xlimright3),(ylimleft3-1,ylimleft3-1), color= 'black', linewidth=0.8, alpha= 0.8)

            self.axes1.plot((xlimleft3, xlimleft3),(ylimleft3-1,ylimright3+1), color= 'black', linewidth=0.8, alpha= 0.8)




            self.axes2.plot((xlimleft4, xlimright4),(ylimleft4-1,ylimleft4-1), color= 'black', linewidth=0.8, alpha= 0.8)

            self.axes2.plot((xlimleft4, xlimleft4),(ylimleft4-1,ylimright4+1), color= 'black', linewidth=0.8, alpha= 0.8)



            self.axes1.annotate(ylabel, (0, ylimright3/2), xycoords='data', xytext=(0, 0),
                           textcoords='offset points',
                           fontsize=9, color='black', alpha=0.8, rotation=90)

            self.axes2.annotate(ylabel, (-0.005, ylimright4/2), xycoords='data', xytext=(0, 0),
                            textcoords='offset points',
                            fontsize=9, color='black', alpha=0.8, rotation=90)

        self.canvas1.draw()
        self.canvas2.draw()

        self.DataToWrite = [
            ["Zircon Sample Label", "Zircon Ce4_3 Ratio", "Melt Ce4_3 Ratio", "DCe4", "DCe3", "DCe Zircon/Melt"], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], "Label"]
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            self.DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        self.newdf = pd.DataFrame(self.DataToWrite)
        print("\n")
        print(self.newdf)

class AppForm(QMainWindow):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to AppForm")

        self.create_main_frame()
        self.create_status_bar()

    def DrawLine(self,l=[(41, 0), (41, 3), (45, 3)] ,color= 'grey', linewidth=0.5, linestyle= '-', linelabel = '', alpha= 0.5 ):
        x=[]
        y=[]
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y,color = color, linewidth = linewidth, linestyle = linestyle , label = linelabel , alpha = alpha)
        return(x,y)

    def save_plot(self):
        file_choices = "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)"

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.TAS)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TAS)  # int

        self.tag_cb = QCheckBox("&Tag")
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.more_cb = QCheckBox("&More")
        self.more_cb.setChecked(True)
        self.more_cb.stateChanged.connect(self.TAS)  # int

        self.detail_cb = QCheckBox("&Detail")
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.TAS)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.detail_cb,self.tag_cb,self.more_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)




        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi= 300 )

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

class TAS(AppForm):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to TAS")

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.TAS)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TAS)  # int

        self.tag_cb = QCheckBox("&Tag")
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.more_cb = QCheckBox("&More")
        self.more_cb.setChecked(True)
        self.more_cb.stateChanged.connect(self.TAS)  # int

        self.detail_cb = QCheckBox("&Detail")
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.TAS)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.detail_cb,self.tag_cb,self.more_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)




        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


    def TAS(self,Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
                 Top=19, Y0=1,Y1=19, Y_Gap=19, FontSize= 12 ,xlabel=r'$SiO_2 wt\%$', ylabel=r'$Na_2O + K_2O wt\%$',width=12, height=12, dpi=300):

        self.axes.clear()
        PointLabels=[]
        x=[]
        y=[]
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 5.2), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        X_offset = -6
        Y_offset = 3

        if(self.more_cb.isChecked()):
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'S/N/L']
            detail = "TAS (total alkali–silica) diagram Volcanic (after Wilson et al. 1989)."
            description="\n" \
                          "F: Foidite, Ph: Phonolite, Pc Pocrobasalt, U1: Tephrite (ol < 10%) Basanite(ol > 10%), U2: Phonotephrite, U3: Tephriphonolite,\n" \
                          "Ba: alkalic basalt,Bs: subalkalic baslt, S1: Trachybasalt, S2: Basaltic Trachyandesite, S3: Trachyandesite,\n" \
                          "O1: Basaltic Andesite, O2: Andesite, O3 Dacite, T: Trachyte , Td: Trachydacite , R: Rhyolite, Q: Silexite \n" \
                          "S/N/L: Sodalitite/Nephelinolith/Leucitolith"
        else:
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'T/U/I']
            detail = "TAS (total alkali–silica) diagram Intrusive (after Wilson et al. 1989)."
            description="\n" \
                          "F: Foidolite, Ph: Foid Syenite, Pc: Peridotgabbro, U1: Foid Gabbro, U2: Foid Monzodiorite, U3: Foid Monzosyenite,\n" \
                          "Ba: alkalic gabbro,Bs: subalkalic gabbro, S1: Monzogabbro, S2: Monzodiorite, S3: Monzonite,\n" \
                          "O1: Gabbroic Diorite, O2: Diorite, O3: Graodiorite, T: Syenite , Td: Quartz Monzonite , R: Granite, Q: Quartzolite \n" \
                          "T/U/I: Tawite/Urtite/Italite"

        TagNumber=min(len(Labels),len(Locations))
        if (self.tag_cb.isChecked()):
            for k in range(TagNumber):
                self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                                   textcoords='offset points',
                                   fontsize= 9, color='grey', alpha=0.8)



        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])

        #self.DrawLine([(41.75, 1), (52.5, 5)])
        #self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        #self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        #self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])



        if(self._changed):
            df=self._df
            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size=df.at[i, 'Size']
                Color=df.at[i, 'Color']

                print(Color,df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha=df.at[i, 'Alpha']
                Marker=df.at[i, 'Marker']
                Label=TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']),marker=df.at[i, 'Marker'], s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'],label=TmpLabel, edgecolors='black')




            if (self.legend_cb.isChecked()):
                a=int(self.slider.value())
                self.axes.legend(loc=a,fontsize= 9)

            if (self.detail_cb.isChecked()):
                self.DrawLine([(30, 0), (90, 0)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(30, 0), (30, 20)],color= 'black', linewidth=0.8, alpha= 0.8)

                self.DrawLine([(30, 0), (29, 0)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(30, 5), (29, 5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(30, 10), (29, 10)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(30, 15), (29, 15)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(30, 20), (29, 20)],color= 'black', linewidth=0.8, alpha= 0.8)

                self.DrawLine([(30, 0), (30, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(40, 0), (40, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(50, 0), (50, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(60, 0), (60, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(70, 0), (70, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(80, 0), (80, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)
                self.DrawLine([(90, 0), (90, -0.5)],color= 'black', linewidth=0.8, alpha= 0.8)

                self.axes.annotate("0", (29, 0), xycoords='data', xytext=(-10, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("5", (29, 5), xycoords='data', xytext=(-10, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("10", (29, 10), xycoords='data', xytext=(-13, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("15", (29, 15), xycoords='data', xytext=(-13, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("20", (29, 20), xycoords='data', xytext=(-13, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)


                self.axes.annotate("30", (30, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("40", (40, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("50", (50, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("60", (60, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("70", (70, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("80", (80, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)
                self.axes.annotate("90", (90, -0.5), xycoords='data', xytext=(0, -10),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)

                self.axes.annotate(xlabel, (55, -3), xycoords='data', xytext=(0, 0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8)

                self.axes.annotate(ylabel, (22, 13), xycoords='data', xytext=(0,0),
                                   textcoords='offset points',
                                   fontsize=9, color='black', alpha=0.8,rotation = 90)



            self.canvas.draw()

class REE(AppForm):

    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    xticklabels = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('REE Standardlized Pattern Diagram')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to REE")

        self.Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 15
        self.X_Gap = 15

        self.create_main_frame()
        self.create_status_bar()





    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.REE)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.REE)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.REE)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def REE(self,Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
                 Top=6, Y0=-1,
                 Y1=3, Y_Gap=5, FontSize=12,
                 xLabel=r'$REE-Standardlized-Pattern$', yLabel='' ,width=12, height=12, dpi=300):

        self.axes.clear()

        self.axes = self.fig.add_subplot(111)



        self.WholeData = []

        raw=self._df

        self.width = width
        self.height = height
        self.dpi = dpi


        self.X0 = 1
        self.X1 = len(self.Element) + 1

        self.X_Gap = X1

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        for l in range(len(raw)):
            if (raw.at[l, 'DataType'] == 'Standard' or raw.at[l, 'DataType'] == 'standard' or raw.at[
                l, 'DataType'] == 'STANDARD'):
                k = l

        for i in range(len(raw)):
            if (raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[
                i, 'DataType'] == 'USER'):

                TmpLabel = ''

                LinesX = []
                LinesY = []
                for j in range(len(self.Element)):
                    tmp = raw.at[i, self.Element[j]] / raw.at[k, self.Element[j]]
                    LinesX.append(j + 1)
                    LinesY.append(math.log(tmp, 10))
                    self.WholeData.append(math.log(tmp, 10))

                    if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        PointLabels.append(raw.at[i, 'Label'])
                        TmpLabel = raw.at[i, 'Label']

                    self.axes.scatter(j + 1, math.log(tmp, 10),  marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel, edgecolors='black')



                self.axes.plot(LinesX,LinesY,color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                     linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])


        Tale =0
        Head =0


        if(len(self.WholeData)>0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)


        Location= round(Tale - (Head-Tale)/5)

        count = round((Head - Tale)/5*7)


        if (self.legend_cb.isChecked()):
            a=int(self.slider.value())
            self.axes.legend(loc=a,fontsize= 9)

        self.DrawLine([(0,Location), (16,Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head+(Head-Tale)/5)], color='black', linewidth=0.8, alpha=0.8)

        for i in range(count):
            self.DrawLine([(0, round(Location+i)), ((Head - Tale)/50,round(Location+i))], color='black',
                          linewidth=0.8, alpha=0.8)

            self.axes.annotate(str(np.power(10.0,(Location+i))), ((Head - Tale)/50,round(Location+i)), xycoords='data', xytext=(-15, 0),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8,rotation = 90)


        for i in range(min(len(self.xticks),len(self.xticklabels))):
            self.DrawLine([(self.xticks[i], Location), (self.xticks[i], Location + (Head-Tale)/50)], color='black', linewidth=0.8, alpha=0.8)
            self.axes.annotate(self.xticklabels[i], (self.xticks[i], Location), xycoords='data', xytext=(-5, -10),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8)
       
        self.canvas.draw()

class Trace(AppForm):
    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
    xticklabels = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy', u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('37 Trace Elements Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            print("DataFrame recieved to Trace")

        self.Element = ['Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy', u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 37
        self.X_Gap = 37

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Trace)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Trace)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Trace)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Trace(self, Left=0, Right=16, X0=1, X1=37, X_Gap=37, Base=-1,
            Top=6, Y0=-1,
            Y1=3, Y_Gap=5, FontSize=12,
            xLabel=r'$REE-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        self.axes.clear()

        self.axes = self.fig.add_subplot(111)

        self.WholeData = []

        raw = self._df

        self.width = width
        self.height = height
        self.dpi = dpi

        self.X0 = 1
        self.X1 = len(self.Element) + 1

        self.X_Gap = X1

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        for l in range(len(raw)):
            if (raw.at[l, 'DataType'] == 'Standard' or raw.at[l, 'DataType'] == 'standard' or raw.at[
                l, 'DataType'] == 'STANDARD'):
                k = l

        for i in range(len(raw)):
            if (raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[
                i, 'DataType'] == 'USER'):

                TmpLabel = ''

                LinesX = []
                LinesY = []
                for j in range(len(self.Element)):
                    tmp = raw.at[i, self.Element[j]] / raw.at[k, self.Element[j]]
                    LinesX.append(j + 1)
                    LinesY.append(math.log(tmp, 10))
                    self.WholeData.append(math.log(tmp, 10))

                    if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        PointLabels.append(raw.at[i, 'Label'])
                        TmpLabel = raw.at[i, 'Label']

                    self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel, edgecolors='black')

                self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                               linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

        Tale =0
        Head =0


        if(len(self.WholeData)>0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7)

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, fontsize=9)

        self.DrawLine([(0, Location), (self.X1 , Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)
            print(Location+i)
            self.axes.annotate(str(np.power(10.0, (Location + i))), ((Head - Tale) / 50, round(Location + i)),
                               xycoords='data', xytext=(-15, 0),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8, rotation=90)

        for i in range(min(len(self.xticks), len(self.xticklabels))):
            self.DrawLine([(self.xticks[i], Location), (self.xticks[i], Location + (Head - Tale) / 50)], color='black',
                          linewidth=0.8, alpha=0.8)
            self.axes.annotate(self.xticklabels[i], (self.xticks[i], Location), xycoords='data', xytext=(-5, -10),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8)

        self.canvas.draw()

class Trace2(AppForm):
    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16,17,18,19,20,21,22,23,24,25,26,27]
    xticklabels = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd', u'Zr', u'Hf',
               u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('27 Trace Elements Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            print("DataFrame recieved to Trace")

        self.Element = ['Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd', u'Zr', u'Hf',
               u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 27
        self.X_Gap = 27

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Trace2)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Trace2)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Trace2)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Trace2(self, Left=0, Right=16, X0=1, X1=27, X_Gap=27, Base=-1,
            Top=6, Y0=-1,
            Y1=3, Y_Gap=5, FontSize=12,
            xLabel=r'$REE-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        self.axes.clear()

        self.axes = self.fig.add_subplot(111)

        self.WholeData = []

        raw = self._df

        self.width = width
        self.height = height
        self.dpi = dpi

        self.X0 = 1
        self.X1 = len(self.Element) + 1

        self.X_Gap = X1

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        for l in range(len(raw)):
            if (raw.at[l, 'DataType'] == 'Standard' or raw.at[l, 'DataType'] == 'standard' or raw.at[
                l, 'DataType'] == 'STANDARD'):
                k = l

        for i in range(len(raw)):
            if (raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[
                i, 'DataType'] == 'USER'):

                TmpLabel = ''

                LinesX = []
                LinesY = []
                for j in range(len(self.Element)):
                    tmp = raw.at[i, self.Element[j]] / raw.at[k, self.Element[j]]
                    LinesX.append(j + 1)
                    LinesY.append(math.log(tmp, 10))
                    self.WholeData.append(math.log(tmp, 10))

                    if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        PointLabels.append(raw.at[i, 'Label'])
                        TmpLabel = raw.at[i, 'Label']

                    self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel, edgecolors='black')

                self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                               linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])
        Tale =0
        Head =0


        if(len(self.WholeData)>0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7)

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, fontsize=9)

        self.DrawLine([(0, Location), (self.X1 , Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)
            print(Location+i)
            self.axes.annotate(str(np.power(10.0, (Location + i))), ((Head - Tale) / 50, round(Location + i)),
                               xycoords='data', xytext=(-15, 0),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8, rotation=90)

        for i in range(min(len(self.xticks), len(self.xticklabels))):
            self.DrawLine([(self.xticks[i], Location), (self.xticks[i], Location + (Head - Tale) / 50)], color='black',
                          linewidth=0.8, alpha=0.8)
            self.axes.annotate(self.xticklabels[i], (self.xticks[i], Location), xycoords='data', xytext=(-5, -10),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8)

        self.canvas.draw()

class Stereo(AppForm):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r''
    ylabel = r''

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Stereo Net Projection')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to Stereo")

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111,projection = 'polar')
        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Stereo)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Stereo)  # int

        self.tag_cb = QCheckBox("&Tag")
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.Stereo)  # int



        self.LineOrPoint_cb = QCheckBox("&Line")
        self.LineOrPoint_cb.setChecked(True)
        self.LineOrPoint_cb.stateChanged.connect(self.Stereo)  # int



        if (self.LineOrPoint_cb.isChecked()):
            self.LineOrPoint_cb.setText('Line')
        else:
            self.LineOrPoint_cb.setText("Point")


        self.Type_cb = QCheckBox("&Wulf")
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Stereo)  # int

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText("Schmidt")



        slider_label = QLabel('Step:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Stereo)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.LineOrPoint_cb,self.Type_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)




        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def eqar(self, A):
        return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))

    def eqan(self, A):
        return 90 * np.tan(np.pi * (90. - A) / (2. * 180.))

    def getangular(self, A, B, C):
        a = np.radians(A)
        b = np.radians(B)
        c = np.radians(C)
        result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
        result = np.rad2deg(result)
        return result

    def Trans(self, S=(0, 100, 110), D=(0, 30, 40)):
        a = []
        b = []

        for i in S:
            a.append(np.radians(90 - i))
        for i in D:
            b.append(self.eqar(i))

        return (a, b)


    def lines(self, Width=1, Color='k'):
        """
        read the Excel, then draw the wulf net and Plot points, job done~
        """
        self.axes.clear()

        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30.,  60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)




        raw = self._df

        Data = []
        Labels = []



        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                         raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]

            Label = raw.at[i, "Label"]
            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size = raw.at[i, "Size"]

            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size = raw.at[i, "Size"]

                Setting = [Width, Color, Alpha, Marker, Size]
            r = np.arange(Dip - 90, Dip + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                Line = (self.eqan(self.getangular(Dip_Angle, Dip, r)))
            else:
                self.Type_cb.setText("Schmidt")
                Line = (self.eqar(self.getangular(Dip_Angle, Dip, r)))


            self.axes.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha, label=Label)

        #self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=2, fontsize=9,bbox_to_anchor=(0, 0))

    def points(self, Width=1, Color='k'):
        """
        read the Excel, then draw the schmidt net and Plot points, job done~
        """
        self.axes.clear()




        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)





        raw = self._df


        Data = []
        Labels = []



        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]
        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)






        for i in range(len(raw)):
            Data.append(
                [raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                 raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Marker"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]

            Label = raw.at[i, "Label"]

            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size = raw.at[i, "Size"]

            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size = raw.at[i, "Size"]

                Setting = [Width, Color, Alpha, Marker, Size]



            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                self.axes.scatter(np.radians(90 - Dip), self.eqan(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')
            else:
                self.Type_cb.setText("Schmidt")
                self.axes.scatter(np.radians(90 - Dip), self.eqar(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')

        # plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        #self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])


        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, fontsize=9, bbox_to_anchor=(0, 0))




    def Stereo(self):
        self.Label = [u'N', u'S', u'W', u'E']
        self.LabelPosition = []




        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText("Schmidt")

        if (self.LineOrPoint_cb.isChecked()):
            self.LineOrPoint_cb.setText('Line')
            self.lines()
        else:
            self.LineOrPoint_cb.setText("Point")
            self.points()

        self.canvas.draw()

class Rose(AppForm):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r''
    ylabel = r''

    Gap = 10

    MultipleRoseName='Dip'

    SingleRoseName=["Dip"]

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Rose Map')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to Rose")

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 5.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111,projection = 'polar')
        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Rose)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Rose)  # int

        self.Type_cb = QCheckBox("&Wulf")
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Rose)  # int

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText("Schmidt")


        self.Rose_cb = QCheckBox("&Single Rose")
        self.Rose_cb.setChecked(True)
        self.Rose_cb.stateChanged.connect(self.Rose)  # int

        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
        else:
            self.Rose_cb.setText("Multiple Rose")


        slider_label = QLabel('Step:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1,30)
        self.slider.setValue(5)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Rose)  # int



        self.ChooseItems=['Strike','Dip','Dip-Angle']
        self.chooser_label = QLabel('Dip')
        self.chooser = QSlider(Qt.Horizontal)
        self.chooser.setRange(1,3)
        self.chooser.setValue(2)
        self.chooser.setTracking(True)
        self.chooser.setTickPosition(QSlider.TicksBothSides)
        self.chooser.valueChanged.connect(self.Rose)  # int

        self.chooser_label.setText(self.ChooseItems[self.chooser.value()-1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value()-1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value()-1])]


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.Type_cb,self.Rose_cb,
                  self.legend_cb, slider_label, self.slider, self.chooser,self.chooser_label]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def eqar(self, A):
        return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))

    def eqan(self, A):
        return 90 * np.tan(np.pi * (90. - A) / (2. * 180.))

    def getangular(self, A, B, C):
        a = np.radians(A)
        b = np.radians(B)
        c = np.radians(C)
        result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
        result = np.rad2deg(result)
        return result

    def Trans(self, S=(0, 100, 110), D=(0, 30, 40)):
        a = []
        b = []

        for i in S:
            a.append(np.radians(90 - i))
        for i in D:

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                b.append(self.eqan(i))
            else:
                self.Type_cb.setText("Schmidt")
                b.append(self.eqar(i))

        return (a, b)

    def lines(self, Width=1, Color='k'):
        """
        read the Excel, then draw the wulf net and Plot points, job done~
        """
        self.axes.clear()

        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30.,  60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)




        raw = self._df

        Data = []
        Labels = []



        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                         raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]

            Label = raw.at[i, "Label"]
            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size = raw.at[i, "Size"]

            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size = raw.at[i, "Size"]

                Setting = [Width, Color, Alpha, Marker, Size]
            r = np.arange(Dip - 90, Dip + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                Line = (self.eqan(self.getangular(Dip_Angle, Dip, r)))
            else:
                self.Type_cb.setText("Schmidt")
                Line = (self.eqar(self.getangular(Dip_Angle, Dip, r)))


            self.axes.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha, label=Label)

        #self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=2, fontsize=9,bbox_to_anchor=(0, 0))

    def points(self, Width=1, Color='k'):
        """
        read the Excel, then draw the schmidt net and Plot points, job done~
        """
        self.axes.clear()




        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)





        raw = self._df


        Data = []
        Labels = []



        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]
        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)






        for i in range(len(raw)):
            Data.append(
                [raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                 raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Marker"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]

            Label = raw.at[i, "Label"]

            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size = raw.at[i, "Size"]

            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size = raw.at[i, "Size"]

                Setting = [Width, Color, Alpha, Marker, Size]



            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                self.axes.scatter(np.radians(90 - Dip), self.eqan(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')
            else:
                self.Type_cb.setText("Schmidt")
                self.axes.scatter(np.radians(90 - Dip), self.eqar(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')

        # plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        #self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])


        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, fontsize=9, bbox_to_anchor=(0, 0))

    def singlerose(self,  Width=1, Color=['red']):
        """
        draw the rose map of single sample with different items~
        """
        self.chooser_label.setText(self.ChooseItems[self.chooser.value()-1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value()-1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value()-1])]

        Name=self.SingleRoseName

        self.axes.clear()
        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        self.raw = self._df

        real_max = []

        for k in range(len(Name)):

            Data = []
            S = []
            R = []
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])

            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())
            count = []

            for i in range(len(t)):
                tmp_count = 0
                for j in S:
                    if i < len(t) - 1:
                        if t[i] < j <= t[i + 1]:
                            tmp_count += 1
                count.append(tmp_count)

            count_max = max(count)
            real_max.append(count_max)

        maxuse = max(real_max)

        for k in range(len(Name)):
            Data = []
            S = []
            R = []
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])

            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())
            count = []

            for i in range(len(t)):
                tmp_count = 0
                for j in S:
                    if i < len(t) - 1:
                        if t[i] < j <= t[i + 1]:
                            tmp_count += 1
                count.append(tmp_count)
            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())

            R_factor = 90 / maxuse

            for i in count:
                TMP = 90 - i * R_factor
                R.append(TMP)

            m, n = self.Trans(t, R)
            self.axes.plot(m, n, color=Color[k], linewidth=1, alpha=0.6, marker='')
            self.axes.fill(m, n, Color=Color[k], Alpha=0.6, )




        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1) / 7))]
        list2.reverse()
        self.axes.set_rgrids(list1, list2)

        self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, fontsize=9, bbox_to_anchor=(0, 0))

    def multirose(self, Width=1, Name='Dip'):
        """
        draw the rose map of multiple samples~
        """

        Name = self.MultipleRoseName

        self.axes.clear()
        self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0,90)

        titles = list("NWSE")

        titles = ['N','330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)


        self.angles=np.array([  90.,  120.,  150.,  180.,  210.,  240.,  270.,  300.,  330.,
        360.,  30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        self.raw = self._df

        real_max = []


        S = []
        R = []
        Color = []
        Label = []
        Whole = {}

        for i in range(len(self.raw)):
            S.append(self.raw.at[i, Name])

            if self.raw.at[i, 'Color'] not in Color and self.raw.at[i, 'Color'] != '':
                Color.append(self.raw.at[i, 'Color'])
            if self.raw.at[i, 'Label'] not in Label and self.raw.at[i, 'Label'] != '':
                Label.append(self.raw.at[i, 'Label'])

        Whole = ({k: [] for k in Label})

        WholeCount = ({k: [] for k in Label})

        for i in range(len(self.raw)):
            for k in Label:
                if self.raw.at[i, 'Label'] == k:
                    Whole[k].append(self.raw.at[i, Name])

        t = tuple(np.linspace(0, 360, 360 / self.Gap + 1).tolist())
        real_max = 0

        for j in range(len(Label)):

            for i in range(len(t)):
                tmp_count = 0
                for u in Whole[Label[j]]:
                    if i < len(t) - 1:
                        if t[i] < u <= t[i + 1]:
                            tmp_count += 1
                real_max = max(real_max, tmp_count)
                WholeCount[Label[j]].append(tmp_count)

        maxuse = real_max
        R_factor = 90 / maxuse

        for j in range(len(Label)):

            R = []
            for i in WholeCount[Label[j]]:
                TMP = 90 - i * R_factor
                R.append(TMP)

            m, n = self.Trans(t, R)
            self.axes.plot(m, n, color=Color[j], linewidth=1, alpha=0.6, marker='', label=Label[j])
            self.axes.fill(m, n, Color=Color[j], Alpha=0.6)

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText("Schmidt")
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1) / 7))]
        list2.reverse()


        self.axes.set_rgrids(list1, list2)

        self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, fontsize=9, bbox_to_anchor=(0, 0))

    def Rose(self):


        self.Gap = self.slider.value()

        self.chooser_label.setText(self.ChooseItems[self.chooser.value()-1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value()-1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value()-1])]

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText("Schmidt")


        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
            self.singlerose()
        else:
            self.Rose_cb.setText("Multiple Rose")
            self.multirose()

        self.canvas.draw()

class Tri(AppForm,Tool):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'C', u'A', u'B']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',
              u'Recycled \n Orogenic',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc']
    Locations = [(8.5, 1.5, 90),
                 (28.5, 1.5, 70),
                 (58.5, 1.5, 40),
                 (18, 22, 70),
                 (35, 30, 35),
                 (15, 60, 15),
                 (11, 80, 9)]
    Offset = [(-80, 2),
              (-80, 2),
              (-80, 2),
              (-20, -5),
              (-20, -8),
              (-60, -2),
              (-40, -5)]


    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Triangular')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to Tri")

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((15.0, 9.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,self.legend_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action



    def Tri(self):


        self.axes.clear()
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)


        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        #self.axes.spines['bottom'].set_color('none')
        #self.axes.spines['left'].set_color('none')



        s=[TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )



        a=[TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),
        TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),
        TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        T0 = (85, 15, 0)
        T1 = (0, 3, 97)
        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T5 = (45, 0, 55)
        T6 = (0, 75, 25)

        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        b=[TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),
        TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='')]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        c=[TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='')]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        p,q=self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p,q, Color='blue', Alpha=0.13, )

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)

        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        m,n=self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        self.axes.fill(m,n, Color='red', Alpha=0.13, )


        raw=self._df
        PointLabels = []
        TPoints=[]
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            TPoints.append(TriPoint((raw.at[i, 'F'], raw.at[i, 'L'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                 label=i.Label, edgecolors='black')



        if (self.legend_cb.isChecked()):
            #a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, fontsize=9, bbox_to_anchor=(1.1, 0.5))


        self.canvas.draw()

class QFL(AppForm,Tool):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Q', u'F', u'L']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',
              u'Recycled \n Orogenic',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc']
    Locations = [(8.5, 1.5, 90),
                 (28.5, 1.5, 70),
                 (58.5, 1.5, 40),
                 (18, 22, 70),
                 (35, 30, 35),
                 (15, 60, 15),
                 (11, 80, 9)]
    Offset = [(-80, 2),
              (-80, 2),
              (-80, 2),
              (-20, -5),
              (-20, -8),
              (-60, -2),
              (-40, -5)]


    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Q-F-L')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to Tri")

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox("&Tag")
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,self.legend_cb,self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action



    def Tri(self):


        self.axes.clear()
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)


        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        #self.axes.spines['bottom'].set_color('none')
        #self.axes.spines['left'].set_color('none')



        s=[TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )



        a=[TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),
        TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),
        TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        T0 = (85, 15, 0)
        T1 = (0, 3, 97)
        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T5 = (45, 0, 55)
        T6 = (0, 75, 25)

        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        b=[TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),
        TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='')]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        c=[TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='')]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        p,q=self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p,q, Color='blue', Alpha=0.13, )

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)

        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        m,n=self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        self.axes.fill(m,n, Color='red', Alpha=0.13, )


        raw=self._df
        PointLabels = []
        TPoints=[]
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            TPoints.append(TriPoint((raw.at[i, 'F'], raw.at[i, 'L'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                 label=i.Label, edgecolors='black')

        if(self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                             textcoords='offset points',
                             fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            #a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, fontsize=9, bbox_to_anchor=(1.1, 0.5))


        self.canvas.draw()

class QmFLt(AppForm,Tool):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Qm', u'F', u'Lt']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',

              u'Mixed',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc',

              u'Quartzose \n Recycled',
              u'Transitional \n Recycled',
              u'Lithic \n Recycled']
    Locations = [(15, 5, 90),
                 (30, 8, 62),
                 (60, 10, 30),

                 (30, 25, 45),
                 (40, 20, 40),
                 (40, 40, 20),
                 (20, 70, 10),

                 (10, 3, 60),
                 (10, 50, 40),
                 (10, 80, 10)]

    Offset = [(-66, 2),
              (-108, 2),
              (-95, 2),

              (-10, +10),
              (-10, -25),
              (-40, -20),
              (-30, -35),

              (+68, -28),
              (+50, -2),
              (+52, -15)]

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Qm-F-lt')

        self._df=df
        if(len(df)>0):
            self._changed = True
            print("DataFrame recieved to Tri")

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton("&Reset")
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox("&Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox("&Tag")
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,self.legend_cb,self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save your figure.")
        self.statusBar().addWidget(self.status_text, 1)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action



    def Tri(self):


        self.axes.clear()
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)


        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        #self.axes.spines['bottom'].set_color('none')
        #self.axes.spines['left'].set_color('none')



        s=[TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )





        a=[TriLine(Points=[(77, 23, 0), (0, 11, 89)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        T0 = (77, 23, 0)
        T1 = (0, 11, 89)
        T2 = (43, 0, 57)
        T3 = (0, 87, 13)

        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (43, 0, 57)
        T3 = (0, 87, 13)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)

        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)

        T8 = self.TriCross(A=[T0, T1], B=[T5, T6])


        b=[        TriLine(Points=[T4, T2], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),

        TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),

        TriLine(Points=[T7, T3], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),

        TriLine(Points=[T8, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),

        TriLine(Points=[T7, (0, 68, 32)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label=''),]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        T9 = (13, 87, 0)



        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T12 = self.TriCross(A=[T10, T11], B=[T0, T1])



        c=[TriLine(Points=[T9, T12], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label=''),]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        p,q= self.TriFill(P=[(100, 0, 0), T0, T1, (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p,q, Color='blue', Alpha=0.13, )



        m,n=self.TriFill(P=[T12, T11, (0, 100, 0), T1], Color='red', Alpha=0.13)

        self.axes.fill(m,n, Color='red', Alpha=0.13, )






        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T13 = (47, 53, 0)
        T14 = (0, 82, 18)

        T15 = self.TriCross(A=[T10, T11], B=[T13, T14])

        k=[TriLine(Points=[T15, T13], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),

        TriLine(Points=[T15, T14], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label=''),]


        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        T10 = (20, 0, 80)
        T16 = (0, 40, 60)

        T17 = self.TriCross(A=[T10, T16], B=[T0, T1])

        k=[TriLine(Points=[T17, T10], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),]


        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T18 = (0, 42, 59)
        T19 = (84, 0, 16)

        T20 = self.TriCross(A=[T10, T11], B=[T18, T19])

        k=[TriLine(Points=[T18, T20], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)

        T21 = (0, 71, 29)
        T22 = (58, 42, 0)

        T23 = self.TriCross(A=[T10, T11], B=[T21, T22])

        k=[TriLine(Points=[T23, T21], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label=''),]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle =i.Style, alpha=i.Alpha,
                  label=i.Label)


        raw=self._df
        PointLabels = []
        TPoints=[]
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            TPoints.append(TriPoint((raw.at[i, 'F'], raw.at[i, 'Lt'], raw.at[i, 'Qm']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                 label=i.Label, edgecolors='black')

        if(self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                             textcoords='offset points',
                             fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            #a = int(self.slider.value())
            #self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, fontsize=9, bbox_to_anchor=(1.1, 0.5))


        self.canvas.draw()

