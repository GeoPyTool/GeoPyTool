version = '0.6.34'

date = '2017-11-5'

dpi = 128

# -*- coding: utf-8 -*-
#coding:utf-8

import math
import sys
import csv
import random




from bs4 import BeautifulSoup
import os
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import ft2font
from matplotlib.font_manager import ttfFontProperty

import matplotlib.font_manager as font_manager
import matplotlib.image as mpimg



LocationOfMySelf=os.path.dirname(__file__)

print(LocationOfMySelf)

fpath = ('wqy.ttf')

font = ft2font.FT2Font(fpath)
fprop = fm.FontProperties(fname=fpath)

ttfFontProp = ttfFontProperty(font)
fontprop = fm.FontProperties(family='sans-serif',
                            #name=ap.fontprop.name,
                            size=9,
                            fname=ttfFontProp.fname,
                            stretch=ttfFontProp.stretch,
                            style=ttfFontProp.style,
                            variant=ttfFontProp.variant,
                            weight=ttfFontProp.weight)

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['axes.unicode_minus']=False

import pandas as pd
import numpy as np

from scipy.cluster import hierarchy as hc
from scipy.cluster.hierarchy import dendrogram, linkage

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
from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)

from xml.dom import minidom

_translate = QtCore.QCoreApplication.translate

class Tool():
    def TriToBin(self, x, y, z):

        '''
        Turn an x-y-z triangular coord to an a-b coord.
        if z is negative, calc with its abs then return (a, -b).
        :param x,y,z: the three numbers of the triangular coord
        :type x,y,z: float or double are both OK, just numbers
        :return:  the corresponding a-b coord
        :rtype:   a tuple consist of a and b
        '''

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

        '''
        Turn an a-b coord to an x-y-z triangular coord .
        if z is negative, calc with its abs then return (a, -b).
        :param a,b: the numbers of the a-b coord
        :type a,b: float or double are both OK, just numbers
        :return:  the corresponding x-y-z triangular coord
        :rtype:   a tuple consist of x,y,z
        '''

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

        '''
        Return the crosspoint of two line A and B.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return: the crosspoint of A and B
        :rtype: a list consist of two numbers, the x-y of the crosspoint
        '''

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

        '''
        Return the crosspoint of two line A and B in triangular coord.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return:  the crosspoint of A and B
        :rtype:   a list consist of three numbers, the x-y-z of the triangular coord
        '''

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

        '''
        Fill a region in planimetric rectangular coord.
        :param P: the peak points of the region in planimetric rectangular coord
        :type P: a list consist of at least three tuples, which are the points in planimetric rectangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        '''
        a = []
        b = []

        for i in P:
            a.append(i[0])
            b.append(i[1])

        return (a, b)

    def TriFill(self, P=[(100, 0, 0), (85, 15, 0), (0, 3, 97)], Color='blue', Alpha=0.3):

        '''
         Fill a region in triangular coord.
        :param P: the peak points of the region in triangular coord
        :type P: a list consist of at least three tuples, which are the points in triangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        '''

        a = []
        b = []

        for i in P:
            a.append(self.TriToBin(i[0], i[1], i[2])[0])
            b.append(self.TriToBin(i[0], i[1], i[2])[1])

        return (a, b)
        # plt.fill(a, b, Color=Color, Alpha=Alpha, )


class Point():
    '''
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
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    '''

    X = 0
    Y = 0
    Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''

    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        '''
        just set up the values
        '''
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
    '''
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
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    '''

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
        '''
        just set up the values
        '''
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
    '''
    a class for Tag put on canvas
    :param Label: label of the Tag, telling what it is and distinguish them from other tags
    :type Label: a strings , if leave as '' or '' such kind of blank string, the label will not show on canvas
    :param Location: the location of the Tag
    :type Location: a tuple consist of x-y values of its coords
    :param X_offset,Y_offset: the values of its x-y offsets on coords
    :type X_offset,Y_offset: two float numbers
    :param FontSize: the size of font of the Tag
    :type FontSize: a number , int or maybe float also OK , better around 8 to 12, not too large or too small
    '''

    Label = u'Label'
    Location = (0, 0)
    X_offset = -6
    Y_offset = 3
    FontSize = 12

    def __init__(self, Label=u'Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=12):
        '''
        set up the values
        '''

        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize


class Line():
    '''
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
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    :param Sort: the sequence used for sorting the points consisting the line
    :type Sort: a string, x means sort the points with their x values, y means use y instead of x, other means use the sequence of points as these points are put to the line
    '''

    Begin = Point(0, 0)
    End = Point(1, 1)
    Points = []
    X = [Begin.X, End.X]
    Y = [Begin.Y, End.Y]
    Width = 1
    Color = 'blue'
    Style = '-'
    Alpha = 0.3
    Label = ''
    Sort = ''

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
        '''
        setup the datas
        '''
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

            # print('Cannot draw line with one point')
            pass

    def sequence(self):
        '''
        sort the points in the line with given option
        '''
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
    '''
    inherit Tag and Tool,a Tag for triangular coord
    '''

    def __init__(self, Label=u'Label', Location=(0, 1, 2), X_offset=-6, Y_offset=3, FontSize=12):
        '''
        set up the values, transfer x,y,z coords to x-y coords
        '''

        self.Label = Label
        self.Location = self.TriToBin(Location[0], Location[1], Location[2])
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize


class TriPoint(Point, Tool):
    '''
    inherit Point and Tool, a Point class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    :param sum: a value used in calc of coord transfer
    :type sum: just a number, both int or float are OK
    '''
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
    '''
    inherit Line and Tool, line class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    '''
    x = []
    y = []
    z = []

    X = []
    Y = []

    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
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
            # print('Cannot draw line with one point')
            pass

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
    _df = pd.DataFrame()
    _changed = False

    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._changed = False

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

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

    '''
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = index.row()
        col = index.column()
        name = self._struct[col]['name']
        self._data[row][name] = value
        self.emit(QtCore.SIGNAL('dataChanged()'))
        return True
    '''

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
        # self.emit(QtCore.SIGNAL('dataChanged()'))
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class CustomQTableView(QtWidgets.QTableView):
    def __init__(self, *args):
        super().__init__(*args)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                             QtWidgets.QAbstractItemView.DoubleClicked)

    def keyPressEvent(self, event):  # Reimplement the event here
        return


class PlotModel(FigureCanvas):
    _df = pd.DataFrame()
    _changed = False

    def __init__(self, parent=None, width=100, height=100, dpi=100, description=''
                 , tag='', xlabel=r'$X$', ylabel=r'$Y$', xlim=(30, 90), ylim=(0, 20)):

        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111, xlabel=xlabel + '\n' + description, ylabel=ylabel, xlim=xlim, ylim=ylim)
        # 设定横纵坐标轴的标签

        # 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        # self.axes.hold(False)




        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def DrawLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                 alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)

    def TAS(self, df=pd.DataFrame(), Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
            Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xLabel=r'$SiO_2 wt\%$', yLabel=r'$na_2O + K_2O wt\%$'):

        PointLabels = []
        x = []
        y = []

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
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = 'TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith'
        tag = 'tas-Wilson1989-volcano'

        if (len(df) > 0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel,
                                  edgecolors='black')

            # self.axes.savefig('tas.png', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.svg', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.pdf', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.eps', dpi=300, bbox_inches='tight')
            # self.axes.show()

            self.draw()

    def TASv(self, df=pd.DataFrame(), Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
             Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xlabel=r'$SiO_2 wt\%$', ylabel=r'$na_2O + K_2O wt\%$',
             width=12, height=12, dpi=300, xlim=(30, 90), ylim=(0, 20)):

        PointLabels = []
        x = []
        y = []

        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]

        X_offset = -6
        Y_offset = 3

        TagNumber = min(len(Labels), len(Locations))

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
        # self.DrawLine([(41.75, 1), (52.5, 5)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = 'TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith'
        tag = 'tas-Wilson1989-volcano'

        if (len(df) > 0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel,
                                  edgecolors='black')

            xLabel = r'$SiO_2 wt\%$' + '\n' + description
            yLabel = r'$na_2O + K_2O wt\%$'
            # self.axes.xlabel(xLabel, fontsize=12)

            self.draw()


class MyPopup(QWidget):
    _df = pd.DataFrame()
    _changed = False

    def __init__(self, width=100, height=100, dpi=100,
                 description='TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith'
                 , tag='tas-Wilson1989-volcano', xlabel=r'$SiO_2 wt\%$', ylabel=r'$Na_2O + K_2O wt\%$', xlim=(30,
                                                                                                              90),
                 ylim=(
                         0, 20)):
        QWidget.__init__(self)

        self.initUI()

        self.MyCanvas = PlotModel(self, width=width, height=height, dpi=dpi, description=description, tag=tag,
                                  xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim)

        self.MyCanvas.setGeometry(QtCore.QRect(10, 10, 512, 512))

        self.MyCanvas.setObjectName('MyCanvas')

    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.MyCanvas.print_figure(ImgFileOutput, dpi=300)

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Save Image', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(256, 550)
        btn.clicked.connect(self.saveImgFile)

        # self.setGeometry(500, 500, 500, 600)
        self.setWindowTitle('Image')


class Zircon(QMainWindow):
    _df = pd.DataFrame()
    _changed = False

    ylabel = r'Ln D $Zircon/Rock%$'
    reference = 'Ballard, J. R., Palin, M. J., and Campbell, I. H., 2002, Relative oxidation states of magmas inferred from Ce(IV)/Ce(III) in zircon: application to porphyry copper deposits of northern Chile: Contributions to Mineralogy and Petrology, v. 144, no. 3, p. 347-364.'

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Oxygen Fugacity Estimation by Ce(IV)/Ce(III) in Zircon (Ballard et al. 2002)')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df

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

        self.DataToWrite = [['First', 'Second', 'Third']]

    def save_plot(self):
        file_choices = 'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)'

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128

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
        self.save_button1 = QPushButton('&Save Ce3 Figure')
        self.save_button1.clicked.connect(self.saveImgFile1)

        self.save_button2 = QPushButton('&Save Ce4 Figure')
        self.save_button2.clicked.connect(self.saveImgFile2)

        self.save_button3 = QPushButton('&Save Result')
        self.save_button3.clicked.connect(self.saveResult)

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.MultiBallard)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button3, self.detail_cb]:
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
        self.textbox = QLineEdit(self)
        self.textbox.setText('Reference：' + '\n' + self.reference)
        self.statusBar().addWidget(self.textbox, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveImgFile1(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas1.print_figure(ImgFileOutput, dpi=300)

    def saveImgFile2(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas2.print_figure(ImgFileOutput, dpi=300)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.newdf.to_excel(DataFileOutput, encoding='utf-8')

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal='triggered()'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png' % icon))
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

        self.raw = self._df

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
            if (self.raw.at[i, 'DataType'] == 'Base'):
                self.Base = i
            elif (self.raw.at[i, 'DataType'] == 'Zircon'):
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

                self.axes1.scatter(x, y, s=3, color='blue', alpha=0.5, label='', edgecolors='black')

            if k == 0:
                for i in range(len(self.x3)):
                    self.axes1.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]), fontsize=8, xytext=(10, 25),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
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
                self.axes1.annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), fontsize=8, xytext=(10, 25),
                                    textcoords='offset points',
                                    ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y3_Plot_Only)):

            for i in range(len(self.x3_Plot_Only)):
                x, y = self.x3_Plot_Only[i], self.y3_Plot_Only[k][i]
                self.axes1.scatter(x, y, label='', s=3, color='blue', alpha=0.3)

            if k == 0:
                for i in range(len(self.x3_Plot_Only)):
                    self.axes1.annotate(self.Elements3_Plot_Only[i], xy=(self.x3_Plot_Only[i], self.y3_Plot_Only[0][i]),
                                        fontsize=8,
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
                    self.axes1.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]), fontsize=8, xytext=(10, 25),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
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
                self.axes1.annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), fontsize=8, xytext=(10, 25),
                                    textcoords='offset points',
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
                    self.axes2.annotate(self.Elements4[i], xy=(self.x4[i], self.y4[0][i]), fontsize=8, xytext=(10, 25),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
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
                self.axes2.annotate('Ce4', xy=(self.xCe4[k], max(self.yCe4)), fontsize=8, xytext=(10, 25),
                                    textcoords='offset points',
                                    ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        DataToWrite = [
            ['Zircon Sample Label', 'Zircon Ce4_3 Ratio', 'Melt Ce4_3 Ratio', 'DCe4', 'DCe3', 'DCe Zircon/Melt'], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], 'Label']
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        ylabel = r'Ln D $Zircon/Rock%$'

        xlimleft3 = 0
        xlimleft4 = -0.005

        # print('\n the value is ', min(min(self.y3)))

        ylimleft3 = min(min(min(self.y3)), min(min(self.y3_Plot_Only)))

        ylimleft4 = min(min(min(self.y4)), min(min(self.yCe4), min(self.yCe3)))

        xlimright3 = 0.06
        xlimright4 = 0.03

        ylimright3 = max(max(self.y3))
        ylimright4 = max(max(self.y4))

        if (self.detail_cb.isChecked()):
            self.axes1.plot((xlimleft3, xlimright3), (ylimleft3 - 1, ylimleft3 - 1), color='black', linewidth=0.8,
                            alpha=0.8)

            self.axes1.plot((xlimleft3, xlimleft3), (ylimleft3 - 1, ylimright3 + 1), color='black', linewidth=0.8,
                            alpha=0.8)

            self.axes2.plot((xlimleft4, xlimright4), (ylimleft4 - 1, ylimleft4 - 1), color='black', linewidth=0.8,
                            alpha=0.8)

            self.axes2.plot((xlimleft4, xlimleft4), (ylimleft4 - 1, ylimright4 + 1), color='black', linewidth=0.8,
                            alpha=0.8)

            self.axes1.annotate(ylabel, (0, ylimright3 / 2), xycoords='data', xytext=(0, 0),
                                textcoords='offset points',
                                fontsize=9, color='black', alpha=0.8, rotation=90)

            self.axes2.annotate(ylabel, (-0.005, ylimright4 / 2), xycoords='data', xytext=(0, 0),
                                textcoords='offset points',
                                fontsize=9, color='black', alpha=0.8, rotation=90)

        self.canvas1.draw()
        self.canvas2.draw()

        self.DataToWrite = [
            ['Zircon Sample Label', 'Zircon Ce4_3 Ratio', 'Melt Ce4_3 Ratio', 'DCe4', 'DCe3', 'DCe Zircon/Melt'], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], 'Label']
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            self.DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        self.newdf = pd.DataFrame(self.DataToWrite)
        # print('\n')
        # print(self.newdf)



class AppForm(QMainWindow):

    _df = pd.DataFrame()
    _changed = False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'
    reference = 'Print the reference here.'

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')

        self.create_main_frame()
        self.create_status_bar()

    def DrawLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                 alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)

    def DrawLogLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                    alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(math.log(i[0], 10))
            y.append(math.log(i[1], 10))

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)

    def save_plot(self):
        file_choices = 'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)'

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.TAS)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TAS)  # int

        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.more_cb = QCheckBox('&More')
        self.more_cb.setChecked(True)
        self.more_cb.stateChanged.connect(self.TAS)  # int

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.TAS)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.detail_cb, self.tag_cb, self.more_cb,
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
        self.textbox = QLineEdit(self)
        self.textbox.setText('Reference：' + '\n' + self.reference)
        self.statusBar().addWidget(self.textbox, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi=300)

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal='triggered()'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png' % icon))
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
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    reference = 'Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to TAS')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.TAS)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TAS)  # int

        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.more_cb = QCheckBox('&More')
        self.more_cb.setChecked(True)
        self.more_cb.stateChanged.connect(self.TAS)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.tag_cb, self.more_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def TAS(self, Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
            Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xlabel=r'$SiO_2 wt\%$', ylabel=r'$Na_2O + K_2O wt\%$', width=12,
            height=12, dpi=300):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        PointLabels = []
        x = []
        y = []
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 5.2), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        X_offset = -6
        Y_offset = 3

        if (self.more_cb.isChecked()):
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'S/N/L']
            detail = 'TAS (total alkali–silica) diagram Volcanic (after Wilson et al. 1989).'
            description = '\n' \
                          'F: Foidite, Ph: Phonolite, Pc Pocrobasalt, U1: Tephrite (ol < 10%) Basanite(ol > 10%), U2: Phonotephrite, U3: Tephriphonolite,\n' \
                          'Ba: alkalic basalt,Bs: subalkalic baslt, S1: Trachybasalt, S2: Basaltic Trachyandesite, S3: Trachyandesite,\n' \
                          'O1: Basaltic Andesite, O2: Andesite, O3 Dacite, T: Trachyte , Td: Trachydacite , R: Rhyolite, Q: Silexite \n' \
                          'S/N/L: Sodalitite/Nephelinolith/Leucitolith'
        else:
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'T/U/I']
            detail = 'TAS (total alkali–silica) diagram Intrusive (after Wilson et al. 1989).'
            description = '\n' \
                          'F: Foidolite, Ph: Foid Syenite, Pc: Peridotgabbro, U1: Foid Gabbro, U2: Foid Monzodiorite, U3: Foid Monzosyenite,\n' \
                          'Ba: alkalic gabbro,Bs: subalkalic gabbro, S1: Monzogabbro, S2: Monzodiorite, S3: Monzonite,\n' \
                          'O1: Gabbroic Diorite, O2: Diorite, O3: Graodiorite, T: Syenite , Td: Quartz Monzonite , R: Granite, Q: Quartzolite \n' \
                          'T/U/I: Tawite/Urtite/Italite'

        TagNumber = min(len(Labels), len(Locations))
        if (self.tag_cb.isChecked()):
            for k in range(TagNumber):
                self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)

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

        # self.DrawLine([(41.75, 1), (52.5, 5)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])



        if (self._changed):
            df = self._df
            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel,
                                  edgecolors='black')

            if (self.legend_cb.isChecked()):
                a = int(self.slider.value())
                #self.axes.legend(loc=a, fontsize=9)
                #fontproperties=fontprop
                #self.axes.legend(loc=a, prop = {'family': LocationOfMySelf + '/wqy.ttf', 'size': 9})
                self.axes.legend(loc=a, prop=fontprop)



            self.DrawLine([(30, 0), (90, 0)], color='black', linewidth=0.8, alpha=0.5)
            self.DrawLine([(30, 0), (30, 20)], color='black', linewidth=0.8, alpha=0.5)




            a=[[(30, 0), (29, 0)],
                [(30, 5), (29, 5)],
                [(30, 10), (29, 10)],
                [(30, 15), (29, 15)],
                [(30, 20), (29, 20)],]

            b=[[(30, 0), (30, -0.5)],
                [(40, 0), (40, -0.5)],
                [(50, 0), (50, -0.5)],
                [(60, 0), (60, -0.5)],
                [(70, 0), (70, -0.5)],
                [(80, 0), (80, -0.5)],
                [(90, 0), (90, -0.5)],]



            for i in a:
                self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
                self.axes.annotate(str(i[0][1]),i[1] , xycoords='data', xytext=(X_offset, Y_offset),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)


            for i in b:
                self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
                self.axes.annotate(str(i[0][0]),i[1] , xycoords='data', xytext=(X_offset, Y_offset-10),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)



            self.canvas.draw()


class REE(AppForm):
    reference = 'Print the reference here.'

    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    xticklabels = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    StandardsName = ['C1 Chondrite Sun and McDonough,1989', 'Chondrite Taylor and McLennan,1985',
                     'Chondrite Haskin et al.,1966', 'Chondrite Nakamura,1977', 'MORB Sun and McDonough,1989']

    # RefName=['Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.',]

    NameChosen = 'C1 Chondrite Sun and McDonough,1989'
    Standards = {
        'C1 Chondrite Sun and McDonough,1989': {'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
                                                'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
                                                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'Chondrite Taylor and McLennan,1985': {'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
                                               'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
                                               'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381},
        'Chondrite Haskin et al.,1966': {'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185, 'Eu': 0.071,
                                         'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                         'Yb': 0.186, 'Lu': 0.034},
        'Chondrite Nakamura,1977': {'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203, 'Eu': 0.077,
                                    'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                    'Yb': 0.22,
                                    'Lu': 0.034},
        'MORB Sun and McDonough,1989': {'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63, 'Eu': 1.02, 'Gd': 3.68,
                                        'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052, 'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05,
                                        'Lu': 0.46}}

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('REE Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to REE')

        self.Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 15
        self.X_Gap = 15

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        self.axes.axis('off')

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.REE)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.REE)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.REE)  # int

        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 4)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.REE)  # int

        self.standard_label = QLabel('Standard: ' + self.StandardsName[int(self.standard.value())])
        self.reference = self.StandardsName[int(self.standard.value())]+'Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, self.slider_label, self.slider, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def REE(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
            Top=6, Y0=-1,
            Y1=3, Y_Gap=5, FontSize=12,
            xLabel=r'$REE-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        self.axes.clear()

        self.axes.axis('off')

        self.WholeData = []

        raw = self._df

        self.FontSize = FontSize

        PointLabels = []
        k = 0

        standardnamechosen = self.StandardsName[int(self.standard.value())]
        standardchosen = self.Standards[standardnamechosen]

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            LinesX = []
            LinesY = []
            for j in range(len(self.Element)):
                tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]
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

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        self.DrawLine([(0, Location), (16, Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        self.standard_label.setText('Standard: ' + self.StandardsName[int(self.standard.value())])

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)

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


class Trace(AppForm):
    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
              30, 31, 32, 33, 34, 35, 36, 37]
    xticklabels = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
                   u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
                   u'Li',
                   u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']

    NameChosen = 'OIB'
    Standards = {
        'OIB': {'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                'K': 12000, 'La': 37, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200, 'Gd': 7.62,
                'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3},
        'EMORB': {'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                  'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155, 'P': 620,
                  'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                  'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                  'Yb': 2.37, 'Lu': 0.354},
        'C1': {'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
               'Ta': 0.014, 'K': 545, 'La': 0.237, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
               'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
               'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
               'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
               'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
               'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
               'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.737, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
               'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
        'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                  'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                  'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                  'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                  'Yb': 3.05, 'Lu': 0.455}, }

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Trace Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Trace')

        self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr',
                        u'Mo',
                        u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
                        u'Li',
                        u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

        self.WholeData = []
        self.X0 = 1
        self.X1 = 37
        self.X_Gap = 37

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Trace)

        self.Type_cb = QCheckBox('&CS-Lu (37 Elements)')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Trace)  # int

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Trace)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Trace)  # int

        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 4)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.Trace)  # int

        self.standard_label = QLabel('Standard: ' + self.StandardsName[int(self.standard.value())])
        self.reference = self.StandardsName[int(self.standard.value())]+ 'Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'
        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.Type_cb,
                  self.legend_cb, self.slider_label, self.slider, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def oldTrace(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
              Top=6, Y0=-1,
              Y1=3, Y_Gap=5, FontSize=12,
              xLabel=r'$Trace-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('&CS-Lu (37 Elements)')
            self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                            u'Pr', u'Mo',
                            u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb',
                            u'Dy', u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
            self.xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                           26, 27,
                           28, 29,
                           30, 31, 32, 33, 34, 35, 36, 37]
            self.xticklabels = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                                u'Pr', u'Mo',
                                u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb',
                                u'Dy',
                                u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            self.setWindowTitle('Trace Standardlized Pattern Diagram CS-Lu (37 Elements)')



        else:
            self.Type_cb.setText('&Rb-Lu (27 Elements)')
            self.Element = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd',
                            u'Zr', u'Hf',
                            u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            self.xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                           26, 27]
            self.xticklabels = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd',
                                u'Zr', u'Hf',
                                u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
            self.setWindowTitle('Trace Standardlized Pattern Diagram Rb-Lu (27 Elements)')

        self.axes.clear()
        self.axes.axis('off')

        self.WholeData = []

        raw = self._df

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        flag = 1

        standardnamechosen = self.StandardsName[int(self.standard.value())]
        standardchosen = self.Standards[standardnamechosen]

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            LinesX = []
            LinesY = []

            for j in range(len(self.Element)):

                flag = 1

                tmp = 1

                if self.Element[j] in raw.columns:
                    tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]

                elif self.Element[j] == 'K' and 'K2O' in raw.columns:
                    tmp = raw.at[i, 'K2O'] * (
                        2 * 39.0983 / 94.1956) * 10000 / standardchosen[
                              self.Element[j]]

                elif self.Element[j] == 'Ti' and 'TiO2' in raw.columns:
                    tmp = raw.at[i, 'TiO2'] * (
                        47.867 / 79.865) * 10000 / standardchosen[
                              self.Element[j]]

                else:
                    flag = 0

                if flag == 1:
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

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        self.DrawLine([(0, Location), (max(self.xticks), Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        self.standard_label.setText('Standard: ' + self.StandardsName[int(self.standard.value())])

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)

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

        pass
    def Trace(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
              Top=6, Y0=-1,
              Y1=3, Y_Gap=5, FontSize=12,
              xLabel=r'$Trace-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('&CS-Lu (37 Elements)')
            self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                            u'Pr', u'Mo',
                            u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb',
                            u'Dy', u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            CommonElements = [i for i in self.Element if i in self._df.columns]
            self.Element = CommonElements
            self.xticks = [i for i in range(1,len(CommonElements)+2)]
            self.xticklabels = CommonElements

            self.setWindowTitle('Trace Standardlized Pattern Diagram CS-Lu '+ str(len(CommonElements)+1) +' Elements')



        else:
            self.Type_cb.setText('&Rb-Lu (27 Elements)')
            self.Element = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd',
                            u'Zr', u'Hf',
                            u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            CommonElements = [i for i in self.Element if i in self._df.columns]
            self.Element = CommonElements
            self.xticks = [i for i in range(1,len(CommonElements)+2)]
            self.xticklabels = CommonElements

            self.setWindowTitle('Trace Standardlized Pattern Diagram Rb-Lu '+ str(len(CommonElements)+1) +' Elements')


        self.axes.clear()
        self.axes.axis('off')

        self.WholeData = []

        raw = self._df

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        flag = 1

        standardnamechosen = self.StandardsName[int(self.standard.value())]
        standardchosen = self.Standards[standardnamechosen]

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            LinesX = []
            LinesY = []

            for j in range(len(CommonElements)):

                flag = 1

                tmp = 1

                if CommonElements[j] in raw.columns:
                    tmp = raw.at[i, CommonElements[j]] / standardchosen[CommonElements[j]]

                elif CommonElements[j] == 'K' and 'K2O' in raw.columns:
                    tmp = raw.at[i, 'K2O'] * (
                        2 * 39.0983 / 94.1956) * 10000 / standardchosen[
                        CommonElements[j]]

                elif CommonElements[j] == 'Ti' and 'TiO2' in raw.columns:
                    tmp = raw.at[i, 'TiO2'] * (
                        47.867 / 79.865) * 10000 / standardchosen[
                        CommonElements[j]]

                else:
                    flag = 0

                if flag == 1:
                    if tmp==tmp:# to delete nan
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

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        self.DrawLine([(0, Location), (max(self.xticks), Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        self.standard_label.setText('Standard: ' + self.StandardsName[int(self.standard.value())])

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)

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
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Stereo Net Projection')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Stereo')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111, projection='polar')
        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Stereo)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Stereo)  # int

        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.Stereo)  # int

        self.LineOrPoint_cb = QCheckBox('&Line')
        self.LineOrPoint_cb.setChecked(True)
        self.LineOrPoint_cb.stateChanged.connect(self.Stereo)  # int

        if (self.LineOrPoint_cb.isChecked()):
            self.LineOrPoint_cb.setText('Line')
        else:
            self.LineOrPoint_cb.setText('Point')

        self.Type_cb = QCheckBox('&Wulf')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Stereo)  # int

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        slider_label = QLabel('Step:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Stereo)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.LineOrPoint_cb, self.Type_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

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
        '''
        read the Excel, then draw the wulf net and Plot points, job done~
        '''
        self.axes.clear()

        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        raw = self._df

        Data = []
        Labels = []

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, 'Name'], raw.at[i, 'Dip'], raw.at[i, 'Dip-Angle'], raw.at[i, 'Color'],
                         raw.at[i, 'Width'], raw.at[i, 'Alpha'], raw.at[i, 'Label']])
            Dip = raw.at[i, 'Dip']
            Dip_Angle = raw.at[i, 'Dip-Angle']

            Label = raw.at[i, 'Label']
            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ''

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, 'Width']
            Color = raw.at[i, 'Color']
            Alpha = raw.at[i, 'Alpha']
            Marker = raw.at[i, 'Marker']
            Size = raw.at[i, 'Size']

            if (Color not in Setting or Color != ''):
                Width = raw.at[i, 'Width']
                Color = raw.at[i, 'Color']
                Alpha = raw.at[i, 'Alpha']
                Marker = raw.at[i, 'Marker']
                Size = raw.at[i, 'Size']

                Setting = [Width, Color, Alpha, Marker, Size]
            r = np.arange(Dip - 90, Dip + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                Line = (self.eqan(self.getangular(Dip_Angle, Dip, r)))
            else:
                self.Type_cb.setText('Schmidt')
                Line = (self.eqar(self.getangular(Dip_Angle, Dip, r)))

            self.axes.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha, label=Label)

        # self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=2, prop=fontprop, bbox_to_anchor=(0, 0))

    def points(self, Width=1, Color='k'):
        '''
        read the Excel, then draw the schmidt net and Plot points, job done~
        '''
        self.axes.clear()

        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        raw = self._df

        Data = []
        Labels = []

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]
        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append(
                [raw.at[i, 'Name'], raw.at[i, 'Dip'], raw.at[i, 'Dip-Angle'], raw.at[i, 'Color'],
                 raw.at[i, 'Width'], raw.at[i, 'Alpha'], raw.at[i, 'Marker'], raw.at[i, 'Label']])
            Dip = raw.at[i, 'Dip']
            Dip_Angle = raw.at[i, 'Dip-Angle']

            Label = raw.at[i, 'Label']

            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ''

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, 'Width']
            Color = raw.at[i, 'Color']
            Alpha = raw.at[i, 'Alpha']
            Marker = raw.at[i, 'Marker']
            Size = raw.at[i, 'Size']

            if (Color not in Setting or Color != ''):
                Width = raw.at[i, 'Width']
                Color = raw.at[i, 'Color']
                Alpha = raw.at[i, 'Alpha']
                Marker = raw.at[i, 'Marker']
                Size = raw.at[i, 'Size']

                Setting = [Width, Color, Alpha, Marker, Size]

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                self.axes.scatter(np.radians(90 - Dip), self.eqan(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')
            else:
                self.Type_cb.setText('Schmidt')
                self.axes.scatter(np.radians(90 - Dip), self.eqar(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')

        # plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        # self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])


        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, prop=fontprop, bbox_to_anchor=(0, 0))

    def Stereo(self):
        self.Label = [u'N', u'S', u'W', u'E']
        self.LabelPosition = []

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        if (self.LineOrPoint_cb.isChecked()):
            self.LineOrPoint_cb.setText('Line')
            self.lines()
        else:
            self.LineOrPoint_cb.setText('Point')
            self.points()

        self.canvas.draw()


class Rose(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Gap = 10

    MultipleRoseName = 'Dip'

    SingleRoseName = ['Dip']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Rose Map')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Rose')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111, projection='polar')
        #self.axes.set_xlim(-90, 450)
        #self.axes.set_ylim(0, 90)




        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Rose)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Rose)  # int

        self.Type_cb = QCheckBox('&Wulf')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Rose)  # int

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        self.Rose_cb = QCheckBox('&Single Rose')
        self.Rose_cb.setChecked(True)
        self.Rose_cb.stateChanged.connect(self.Rose)  # int

        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
        else:
            self.Rose_cb.setText('Multiple Rose')

        slider_label = QLabel('Step:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 30)
        self.slider.setValue(5)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Rose)  # int

        self.ChooseItems = ['Strike', 'Dip', 'Dip-Angle']
        self.chooser_label = QLabel('Dip')
        self.chooser = QSlider(Qt.Horizontal)
        self.chooser.setRange(1, 3)
        self.chooser.setValue(2)
        self.chooser.setTracking(True)
        self.chooser.setTickPosition(QSlider.TicksBothSides)
        self.chooser.valueChanged.connect(self.Rose)  # int

        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.Type_cb, self.Rose_cb,
                  self.legend_cb, slider_label, self.slider, self.chooser, self.chooser_label]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

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
                self.Type_cb.setText('Schmidt')
                b.append(self.eqar(i))

        return (a, b)


    def singlerose(self, Width=1, Color=['red']):
        '''
        draw the rose map of single sample with different items~
        '''
        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        Name = self.SingleRoseName

        self.axes.clear()
        # self.axes.set_xlim(-90, 450)
        # self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
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
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1) / 7))]
        list2.reverse()
        self.axes.set_rgrids(list1, list2)

        #self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, prop=fontprop, bbox_to_anchor=(0, 0))

    def multirose(self, Width=1, Name='Dip'):
        '''
        draw the rose map of multiple samples~
        '''

        Name = self.MultipleRoseName

        self.axes.clear()
        # self.axes.set_xlim(-90, 450)
        # self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
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
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1) / 7))]
        list2.reverse()

        self.axes.set_rgrids(list1, list2)

        #self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=2, prop=fontprop, bbox_to_anchor=(0, 0))

    def Rose(self):

        self.Gap = self.slider.value()

        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
            self.singlerose()
        else:
            self.Rose_cb.setText('Multiple Rose')
            self.multirose()

        self.canvas.draw()


class MudStone(AppForm, Tool):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Clay', u'Sand', u'Silt']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-13, -2),
                     (104, -1)]

    Labels = [u'Y',
              u'SY',
              u'TY',
              u'YS',
              u'STY',
              u'YT',
              u'S',
              u'TS',
              u'ST',
              u'T',
              '20',
              '40',
              '60',
              '80',

              '80',
              '60',
              '40',
              '20',

              '80',
              '60',
              '40',
              '20', ]

    Locations = [(10, 10, 80),
                 (40, 10, 50),
                 (10, 40, 50),
                 (50, 10, 40),
                 (30, 30, 30),
                 (10, 50, 40),
                 (80, 10, 10),
                 (60, 30, 10),
                 (40, 50, 10),
                 (10, 80, 10),

                 (20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 20, 80),
                 (0, 40, 60),
                 (0, 60, 40),
                 (0, 80, 20),
                 ]
    Offset = [(0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),

              (-18, 0),
              (-18, 0),
              (-18, 0),
              (-18, 0),

              (0, -18),
              (0, -18),
              (0, -18),
              (0, -18),

              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0), ]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Sand-Silt-Clay')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

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
        self.dpi = 128
        self.fig = Figure((15.0, 9.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox('&Tag')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb, self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-15, 140)
        self.axes.set_ylim(-10, 100)

        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=16, )
        # 20间隔点坐标：
        Gap20 = [(20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 80, 20),
                 (0, 60, 40),
                 (0, 40, 60),
                 (0, 20, 80)]

        # 二等分点坐标：
        Gap50 = [(50, 0, 50),
                 (40, 20, 40),

                 (0, 50, 50),
                 (20, 40, 40),

                 (50, 50, 0),
                 (40, 40, 20), ]

        # 四等分点坐标：
        Gap25 = [(25, 0, 75),
                 (0, 25, 75),

                 (75, 0, 25),
                 (75, 25, 0),

                 (25, 75, 0),
                 (0, 75, 25), ]

        # 中心三角坐标：
        Middle = [(20, 20, 60),
                  (60, 20, 20),
                  (20, 60, 20), ]

        # 中心三角垂直链接四等分线坐标：
        Other = [(12.5, 12.5, 75),
                 (75, 12.5, 12.5),
                 (12.5, 75, 12.5), ]

        tmp = []
        # 中心三角绘制
        tmp.append(
            TriLine(Points=[Middle[0], Middle[1], Middle[2], Middle[0]], Sort='', Width=1, Color='black', Style='-',
                    Alpha=0.7,
                    Label=''))

        # 二等分和四等分线条绘制
        for i in range(len(Gap50)):

            if i % 2 == 0:
                tmp.append(
                    TriLine(Points=[Gap50[i], Gap50[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))
                tmp.append(
                    TriLine(Points=[Gap25[i], Gap25[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))

        # 中心外延线条绘制
        for i in range(len(Middle)):
            tmp.append(TriLine(Points=[Middle[i], Other[i]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                               Label=''))

        # 20网格线条绘制
        for i in range(len(Gap20)):
            if i <= len(Gap20) - 5:
                tmp.append(
                    TriLine(Points=[Gap20[i], Gap20[i + 4]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                            Label=''))
            else:
                tmp.append(
                    TriLine(Points=[Gap20[i], Gap20[-1 - i]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                            Label=''))

        for i in tmp:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        raw = self._df
        PointLabels = []
        TPoints = []
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            TPoints.append(TriPoint((raw.at[i, 'sand'], raw.at[i, 'silt'], raw.at[i, 'clay']), Size=raw.at[i, 'Size'],
                                    Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                    Label=TmpLabel))


            # TPoints.append(TriPoint((raw.at[i, 'X'], raw.at[i, 'Y'], raw.at[i, 'Z']), Size=raw.at[i, 'Size'],
            #         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
            #         Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')

        if (self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            # a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, prop=fontprop, bbox_to_anchor=(1.1, 0.5))

        self.canvas.draw()

        self.canvas.draw()


class QFL(AppForm, Tool):
    reference = 'Dickinson, W. R., and Suczek, C. A., 1979, Plate Tectonics and sandstone composition: Aapg Bulletin, v. 63, no. 12, p. 2164-2182.'
    _df = pd.DataFrame()
    _changed = False

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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Q-F-L')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

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
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox('&Tag')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb, self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)

        # self.axes.spines['right'].set_color('none')
        # self.axes.spines['top'].set_color('none')
        # self.axes.spines['bottom'].set_color('none')
        # self.axes.spines['left'].set_color('none')



        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=16, )

        a = [TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),
             TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),
             TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
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

        b = [TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),
             TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label='')]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        c = [TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label='')]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        p, q = self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p, q, Color='blue', Alpha=0.13, )

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)

        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        m, n = self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        self.axes.fill(m, n, Color='red', Alpha=0.13, )

        raw = self._df
        PointLabels = []
        TPoints = []
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

        if (self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            # a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, prop=fontprop, bbox_to_anchor=(1.1, 0.5))

        self.canvas.draw()


class QmFLt(AppForm, Tool):
    reference = 'Dickinson, W. R., and Suczek, C. A., 1979, Plate Tectonics and sandstone composition: Aapg Bulletin, v. 63, no. 12, p. 2164-2182.'
    _df = pd.DataFrame()
    _changed = False

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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Qm-F-lt')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

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
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox('&Tag')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb, self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)

        # self.axes.spines['right'].set_color('none')
        # self.axes.spines['top'].set_color('none')
        # self.axes.spines['bottom'].set_color('none')
        # self.axes.spines['left'].set_color('none')



        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=16, )

        a = [TriLine(Points=[(77, 23, 0), (0, 11, 89)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
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

        b = [TriLine(Points=[T4, T2], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T7, T3], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T8, T7], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T7, (0, 68, 32)], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label=''), ]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T9 = (13, 87, 0)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T12 = self.TriCross(A=[T10, T11], B=[T0, T1])

        c = [TriLine(Points=[T9, T12], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''), ]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        p, q = self.TriFill(P=[(100, 0, 0), T0, T1, (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p, q, Color='blue', Alpha=0.13, )

        m, n = self.TriFill(P=[T12, T11, (0, 100, 0), T1], Color='red', Alpha=0.13)

        self.axes.fill(m, n, Color='red', Alpha=0.13, )

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T13 = (47, 53, 0)
        T14 = (0, 82, 18)

        T15 = self.TriCross(A=[T10, T11], B=[T13, T14])

        k = [TriLine(Points=[T15, T13], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T15, T14], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label=''), ]

        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T10 = (20, 0, 80)
        T16 = (0, 40, 60)

        T17 = self.TriCross(A=[T10, T16], B=[T0, T1])

        k = [TriLine(Points=[T17, T10], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]

        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T18 = (0, 42, 59)
        T19 = (84, 0, 16)

        T20 = self.TriCross(A=[T10, T11], B=[T18, T19])

        k = [TriLine(Points=[T18, T20], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T21 = (0, 71, 29)
        T22 = (58, 42, 0)

        T23 = self.TriCross(A=[T10, T11], B=[T21, T22])

        k = [TriLine(Points=[T23, T21], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        raw = self._df
        PointLabels = []
        TPoints = []
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

        if (self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            # a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(1.5, 0.5))
            self.axes.legend(loc=4, prop=fontprop, bbox_to_anchor=(1.1, 0.5))

        self.canvas.draw()


class CIPW(AppForm):
    addon = 'Name Author DataType Label Marker Color Size Alpha Style Width TOTAL total LOI loi'

    Minerals = ['Quartz',
                'Zircon',
                'K2SiO3',
                'Anorthite',
                'Na2SiO3',
                'Acmite',
                'Diopside',
                'Sphene',
                'Hypersthene',
                'Albite',
                'Orthoclase',
                'Wollastonite',
                'Olivine',
                'Perovskite',
                'Nepheline',
                'Leucite',
                'Larnite',
                'Kalsilite',
                'Apatite',
                'Halite',
                'Fluorite',
                'Anhydrite',
                'Thenardite',
                'Pyrite',
                'Magnesiochromite',
                'Chromite',
                'Ilmenite',
                'Calcite',
                'Na2CO3',
                'Corundum',
                'Rutile',
                'Magnetite',
                'Hematite',
                'Q',
                'A',
                'P',
                'F', ]

    Calced = ['Fe3+/(Total Fe) in rock',
              'Mg/(Mg+Total Fe) in rock',
              'Mg/(Mg+Fe2+) in rock',
              'Mg/(Mg+Fe2+) in silicates',
              'Ca/(Ca+Na) in rock',
              'Plagioclase An content',
              'Differentiation Index']
    DataWeight = {}
    DataVolume = {}
    DataBase = {}
    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('CIPW Norm)')

        self._df = df
        self.raw = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveImgFile)

        self.qapf_button = QPushButton('&QAPF')
        self.qapf_button.clicked.connect(self.QAPF)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.ChooseItems = ['Mass', 'Volume', 'Mole', 'Index']
        self.chooser_label = QLabel('Show Result of Mass')
        self.chooser = QSlider(Qt.Horizontal)
        self.chooser.setRange(1, 4)
        self.chooser.setValue(1)
        self.chooser.setTracking(True)
        self.chooser.setTickPosition(QSlider.TicksBothSides)
        self.chooser.valueChanged.connect(self.CIPW)  # int

        self.chooser_label.setText('Show Result of ' + self.ChooseItems[self.chooser.value() - 1])

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.qapf_button, self.chooser_label, self.chooser]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Calc(self):

        self.DataBase.update({'Quartz': [60.0843, 2.65]})
        self.DataBase.update({'Zircon': [183.3031, 4.56]})
        self.DataBase.update({'K2SiO3': [154.2803, 2.5]})
        self.DataBase.update({'Anorthite': [278.2093, 2.76]})
        self.DataBase.update({'Na2SiO3': [122.0632, 2.4]})
        self.DataBase.update({'Acmite': [462.0083, 3.6]})
        self.DataBase.update({'Diopside': [229.0691997, 3.354922069]})
        self.DataBase.update({'Sphene': [196.0625, 3.5]})
        self.DataBase.update({'Hypersthene': [112.9054997, 3.507622212]})
        self.DataBase.update({'Albite': [524.446, 2.62]})
        self.DataBase.update({'Orthoclase': [556.6631, 2.56]})
        self.DataBase.update({'Wollastonite': [116.1637, 2.86]})
        self.DataBase.update({'Olivine': [165.7266995, 3.68429065]})
        self.DataBase.update({'Perovskite': [135.9782, 4]})
        self.DataBase.update({'Nepheline': [284.1088, 2.56]})
        self.DataBase.update({'Leucite': [436.4945, 2.49]})
        self.DataBase.update({'Larnite': [172.2431, 3.27]})
        self.DataBase.update({'Kalsilite': [316.3259, 2.6]})
        self.DataBase.update({'Apatite': [493.3138, 3.2]})
        self.DataBase.update({'Halite': [66.44245, 2.17]})
        self.DataBase.update({'Fluorite': [94.0762, 3.18]})
        self.DataBase.update({'Anhydrite': [136.1376, 2.96]})
        self.DataBase.update({'Thenardite': [142.0371, 2.68]})
        self.DataBase.update({'Pyrite': [135.9664, 4.99]})
        self.DataBase.update({'Magnesiochromite': [192.2946, 4.43]})
        self.DataBase.update({'Chromite': [223.8366, 5.09]})
        self.DataBase.update({'Ilmenite': [151.7452, 4.75]})
        self.DataBase.update({'Calcite': [100.0892, 2.71]})
        self.DataBase.update({'Na2CO3': [105.9887, 2.53]})
        self.DataBase.update({'Corundum': [101.9613, 3.98]})
        self.DataBase.update({'Rutile': [79.8988, 4.2]})
        self.DataBase.update({'Magnetite': [231.5386, 5.2]})
        self.DataBase.update({'Hematite': [159.6922, 5.25]})
        self.b = self.raw.columns
        self.WeightCorrectionFactor = []
        self.BaseMass = {}
        self.Elements = ['SiO2',
                         'TiO2',
                         'Al2O3',
                         'Fe2O3',
                         'FeO',
                         'MnO',
                         'MgO',
                         'CaO',
                         'Na2O',
                         'K2O',
                         'P2O5',
                         'CO2',
                         'SO3',
                         'S',
                         'F',
                         'Cl',
                         'Sr',
                         'Ba',
                         'Ni',
                         'Cr',
                         'Zr']
        self.DataMole = []
        self.DataCalculating = {}
        self.DataResult = {}

        self.ElementsMass = [('SiO2', 60.083),
                             ('TiO2', 79.865),
                             ('Al2O3', 101.960077),
                             ('Fe2O3', 159.687),
                             ('FeO', 71.844),
                             ('MnO', 70.937044),
                             ('MgO', 40.304),
                             ('CaO', 56.077000000000005),
                             ('Na2O', 61.978538560000004),
                             ('K2O', 94.1956),
                             ('P2O5', 141.942523996),
                             ('CO2', 44.009),
                             ('SO3', 80.057),
                             ('S', 32.06),
                             ('F', 18.998403163),
                             ('Cl', 35.45),
                             ('Sr', 87.62),
                             ('Ba', 137.327),
                             ('Ni', 58.6934),
                             ('Cr', 51.9961),
                             ('Zr', 91.224)]

        self.BaseMass = {'SiO2': 60.083,
                         'TiO2': 79.865,
                         'Al2O3': 101.960077,
                         'Fe2O3': 159.687,
                         'FeO': 71.844,
                         'MnO': 70.937044,
                         'MgO': 40.304,
                         'CaO': 56.077000000000005,
                         'Na2O': 61.978538560000004,
                         'K2O': 94.1956,
                         'P2O5': 141.942523996,
                         'CO2': 44.009,
                         'SO3': 80.057,
                         'S': 32.06,
                         'F': 18.998403163,
                         'Cl': 35.45,
                         'Sr': 87.62,
                         'Ba': 137.327,
                         'Ni': 58.6934,
                         'Cr': 51.9961,
                         'Zr': 91.224}

        for i in range(len(self.raw)):
            TmpWhole = 0
            TmpMole = {}

            for j in self.Elements:
                '''
                Get the Whole Mole of the dataset
                '''

                try:
                    T_TMP = self.raw.at[i, j]
                except(KeyError):
                    T_TMP = 0

                if j == 'Sr':
                    TMP = T_TMP / (87.62 / 103.619 * 10000)

                elif j == 'Ba':
                    TMP = T_TMP / (137.327 / 153.326 * 10000)


                elif j == 'Ni':
                    TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)

                elif j == 'Cr':
                    TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)

                elif j == 'Zr':
                    # Zr Multi 2 here
                    TMP = T_TMP / ((2 * 91.224) / 123.22200000000001 * 10000)

                else:
                    TMP = T_TMP

                V = TMP

                try:
                    TmpWhole += float(V)
                except ValueError:
                    pass

            self.WeightCorrectionFactor.append(100 / TmpWhole)

            for j in self.Elements:
                '''
                Get the Mole percentage of each element
                '''

                try:
                    T_TMP = self.raw.at[i, j]
                except(KeyError):
                    T_TMP = 0

                if j == 'Sr':
                    TMP = T_TMP / (87.62 / 103.619 * 10000)

                elif j == 'Ba':
                    TMP = T_TMP / (137.327 / 153.326 * 10000)

                elif j == 'Ni':
                    TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)

                elif j == 'Cr':
                    TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)

                elif j == 'Zr':
                    # Zr not Multiple by 2 Here
                    TMP = T_TMP / ((91.224) / 123.22200000000001 * 10000)

                else:
                    TMP = T_TMP

                try:
                    M = TMP / self.BaseMass[j] * self.WeightCorrectionFactor[i]
                except TypeError:
                    pass

                # M= TMP/NewMass(j) * WeightCorrectionFactor[i]

                TmpMole.update({j: M})
            self.DataMole.append(TmpMole)

        self.DataCalculating = {k: [] for k in self.Elements}

        for i in range(len(self.DataMole)):
            k = self.raw.at[i, 'Label']
            self.DataResult.update({k: {}})
            self.DataWeight.update({k: {}})
            self.DataVolume.update({k: {}})
            self.DataCalced.update({k: {}})

            a = self.DataMole[i]
            for j in list(a):
                self.DataCalculating[j].append(a[j])

            Fe3 = self.DataCalculating['Fe2O3'][i]
            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]
            Ca = self.DataCalculating['CaO'][i]
            Na = self.DataCalculating['Na2O'][i]

            try:
                self.DataCalced[k].update({'Fe3+/(Total Fe) in rock': 100 * Fe3 * 2 / (Fe3 * 2 + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Fe3+/(Total Fe) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Mg/(Mg+Total Fe) in rock': 100 * Mg / (Mg + Fe3 * 2 + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Mg/(Mg+Total Fe) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in rock': 100 * Mg / (Mg + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Ca/(Ca+Na) in rock': 100 * Ca / (Ca + Na * 2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Ca/(Ca+Na) in rock': 0})
                pass

            self.DataCalculating['CaO'][i] += self.DataCalculating['Sr'][i]
            self.DataCalculating['Sr'][i] = 0

            self.DataCalculating['K2O'][i] += 2 * self.DataCalculating['Ba'][i]
            self.DataCalculating['Ba'][i] = 0

            try:
                if self.DataCalculating['CaO'][i] >= 10 / 3 * self.DataCalculating['P2O5'][i]:
                    self.DataCalculating['CaO'][i] -= 10 / 3 * self.DataCalculating['P2O5'][i]
                else:
                    self.DataCalculating['CaO'][i] = 0
            except(ZeroDivisionError):
                pass

            self.DataCalculating['P2O5'][i] = self.DataCalculating['P2O5'][i] / 1.5

            Apatite = self.DataCalculating['P2O5'][i]

            # IF(S19>=T15,S19-T15,0)

            if self.DataCalculating['F'][i] >= self.DataCalculating['P2O5'][i]:
                self.DataCalculating['F'][i] -= self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['F'][i] = 0

            if self.DataCalculating['F'][i] >= self.DataCalculating['P2O5'][i]:
                self.DataCalculating['F'][i] -= self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['F'][i] = 0

            if self.DataCalculating['Na2O'][i] >= self.DataCalculating['Cl'][i]:
                self.DataCalculating['Na2O'][i] -= self.DataCalculating['Cl'][i]
            else:
                self.DataCalculating['Na2O'][i] = 0

            Halite = self.DataCalculating['Cl'][i]

            # IF(U12>=(U19/2),U12-(U19/2),0)
            if self.DataCalculating['CaO'][i] >= 0.5 * self.DataCalculating['F'][i]:
                self.DataCalculating['CaO'][i] -= 0.5 * self.DataCalculating['F'][i]
            else:
                self.DataCalculating['CaO'][i] = 0

            self.DataCalculating['F'][i] *= 0.5

            Fluorite = self.DataCalculating['F'][i]

            # =IF(V17>0,IF(V13>=V17,'Thenardite',IF(V13>0,'Both','Anhydrite')),'None')
            AorT = 0
            if self.DataCalculating['SO3'][i] <= 0:
                AorT = 'None'
            else:
                if self.DataCalculating['Na2O'][i] >= self.DataCalculating['SO3'][i]:
                    AorT = 'Thenardite'
                else:
                    if self.DataCalculating['Na2O'][i] > 0:
                        AorT = 'Both'
                    else:
                        AorT = 'Anhydrite'

            # =IF(W26='Anhydrite',V17,IF(W26='Both',V12,0))
            # =IF(W26='Thenardite',V17,IF(W26='Both',V17-W17,0))

            if AorT == 'Anhydrite':
                self.DataCalculating['Sr'][i] = 0
            elif AorT == 'Thenardite':
                self.DataCalculating['Sr'][i] = self.DataCalculating['SO3'][i]
                self.DataCalculating['SO3'][i] = 0
            elif AorT == 'Both':
                self.DataCalculating['Sr'][i] = self.DataCalculating['SO3'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['SO3'][i] = self.DataCalculating['CaO'][i]
            else:
                self.DataCalculating['SO3'][i] = 0
                self.DataCalculating['Sr'][i] = 0

            self.DataCalculating['CaO'][i] -= self.DataCalculating['SO3'][i]

            self.DataCalculating['Na2O'][i] -= self.DataCalculating['Sr'][i]

            Anhydrite = self.DataCalculating['SO3'][i]
            Thenardite = self.DataCalculating['Sr'][i]

            Pyrite = 0.5 * self.DataCalculating['S'][i]

            # =IF(W9>=(W18*0.5),W9-(W18*0.5),0)

            if self.DataCalculating['FeO'][i] >= self.DataCalculating['S'][i] * 0.5:
                self.DataCalculating['FeO'][i] -= self.DataCalculating['S'][i] * 0.5
            else:
                self.DataCalculating['FeO'][i] = 0

            # =IF(X24>0,IF(X9>=X24,'Chromite',IF(X9>0,'Both','Magnesiochromite')),'None')

            if self.DataCalculating['Cr'][i] > 0:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['Cr'][i]:
                    CorM = 'Chromite'
                elif self.DataCalculating['FeO'][i] > 0:
                    CorM = 'Both'
                else:
                    CorM = 'Magnesiochromite'
            else:
                CorM = 'None'

            # =IF(Y26='Chromite',X24,IF(Y26='Both',X9,0))
            # =IF(Y26='Magnesiochromite',X24,IF(Y26='Both',X24-Y24,0))

            if CorM == 'Chromite':
                self.DataCalculating['Cr'][i] = self.DataCalculating['Cr'][i]
                self.DataCalculating['Ni'][i] = 0

            elif CorM == 'Magnesiochromite':
                self.DataCalculating['Ni'][i] = self.DataCalculating['Cr'][i]
                self.DataCalculating['Cr'][i] = 0

            elif CorM == 'Both':
                self.DataCalculating['Ni'][i] = self.DataCalculating['Cr'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['Cr'][i] = self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['Cr'][i] = 0
                self.DataCalculating['Ni'][i] = 0

            self.DataCalculating['MgO'][i] -= self.DataCalculating['Ni'][i]

            Magnesiochromite = self.DataCalculating['Ni'][i]
            Chromite = self.DataCalculating['Cr'][i]

            # =IF(X9>=Y24,X9-Y24,0)

            if self.DataCalculating['FeO'][i] >= self.DataCalculating['Cr'][i]:
                self.DataCalculating['FeO'][i] -= self.DataCalculating['Cr'][i]
            else:
                self.DataCalculating['FeO'][i] = 0

            # =IF(Y6>0,IF(Y9>=Y6,'Ilmenite',IF(Y9>0,'Both','Sphene')),'None')

            if self.DataCalculating['TiO2'][i] < 0:
                IorS = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['TiO2'][i]:
                    IorS = 'Ilmenite'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        IorS = 'Both'
                    else:
                        IorS = 'Sphene'

            # =IF(Z26='Ilmenite',Y6,IF(Z26='Both',Y9,0))
            # =IF(Z26='Sphene',Y6,IF(Z26='Both',Y6-Z6,0))

            if IorS == 'Ilmenite':
                self.DataCalculating['TiO2'][i] = self.DataCalculating['TiO2'][i]
                self.DataCalculating['MnO'][i] = 0

            elif IorS == 'Sphene':
                self.DataCalculating['MnO'][i] = self.DataCalculating['TiO2'][i]
                self.DataCalculating['TiO2'][i] = 0

            elif IorS == 'Both':

                self.DataCalculating['MnO'][i] = self.DataCalculating['TiO2'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['TiO2'][i] = self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['TiO2'][i] = 0
                self.DataCalculating['MnO'][i] = 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['TiO2'][i]

            Ilmenite = self.DataCalculating['TiO2'][i]

            # =IF(Z16>0,IF(Z12>=Z16,'Calcite',IF(Z12>0,'Both','Na2CO3')),'None')


            if self.DataCalculating['CO2'][i] <= 0:
                CorN = 'None'
            else:
                if self.DataCalculating['CaO'][i] >= self.DataCalculating['CO2'][i]:
                    CorN = 'Calcite'
                else:
                    if self.DataCalculating['CaO'][i] > 0:
                        CorN = 'Both'
                    else:
                        CorN = 'Na2CO3'

            # =IF(AA26='Calcite',Z16,IF(AA26='Both',Z12,0))


            # =IF(AA26='Na2CO3',Z16,IF(AA26='Both',Z16-AA16,0))

            if CorN == 'None':
                self.DataCalculating['CO2'][i] = 0
                self.DataCalculating['SO3'][i] = 0

            elif CorN == 'Calcite':
                self.DataCalculating['CO2'][i] = self.DataCalculating['CO2'][i]
                self.DataCalculating['SO3'][i] = 0

            elif CorN == 'Na2CO3':
                self.DataCalculating['SO3'][i] = self.DataCalculating['SO3'][i]
                self.DataCalculating['CO2'][i] = 0

            elif CorN == 'Both':
                self.DataCalculating['SO3'][i] = self.DataCalculating['CO2'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['CO2'][i] = self.DataCalculating['CaO'][i]

            self.DataCalculating['CaO'][i] -= self.DataCalculating['CO2'][i]

            Calcite = self.DataCalculating['CO2'][i]

            Na2CO3 = self.DataCalculating['SO3'][i]

            # =IF(AA17>Z13,0,Z13-AA17)
            if self.DataCalculating['SO3'][i] > self.DataCalculating['Na2O'][i]:
                self.DataCalculating['Na2O'][i] = 0
            else:
                self.DataCalculating['Na2O'][i] -= self.DataCalculating['SO3'][i]

            self.DataCalculating['SiO2'][i] -= self.DataCalculating['Zr'][i]
            Zircon = self.DataCalculating['Zr'][i]

            # =IF(AB14>0,IF(AB7>=AB14,'Orthoclase',IF(AB7>0,'Both','K2SiO3')),'None')

            if self.DataCalculating['K2O'][i] <= 0:
                OorK = 'None'
            else:
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['K2O'][i]:
                    OorK = 'Orthoclase'
                else:
                    if self.DataCalculating['Al2O3'][i] > 0:
                        OorK = 'Both'
                    else:
                        OorK = 'K2SiO3'

            # =IF(AC26='Orthoclase',AB14,IF(AC26='Both',AB7,0))
            # =IF(AC26='K2SiO3',AB14,IF(AC26='Both',AB14-AB7,0))

            if OorK == 'None':
                self.DataCalculating['K2O'][i] = 0
                self.DataCalculating['P2O5'][i] = 0


            elif OorK == 'Orthoclase':
                self.DataCalculating['K2O'][i] = self.DataCalculating['K2O'][i]
                self.DataCalculating['P2O5'][i] = 0


            elif OorK == 'K2SiO3':
                self.DataCalculating['P2O5'][i] = self.DataCalculating['K2O'][i]
                self.DataCalculating['K2O'][i] = 0



            elif OorK == 'Both':

                self.DataCalculating['P2O5'][i] = self.DataCalculating['K2O'][i] - self.DataCalculating['Al2O3'][i]
                self.DataCalculating['K2O'][i] = self.DataCalculating['Al2O3'][i]

            self.DataCalculating['Al2O3'][i] -= self.DataCalculating['K2O'][i]

            # =IF(AC13>0,IF(AC7>=AC13,'Albite',IF(AC7>0,'Both','Na2SiO3')),'None')

            if self.DataCalculating['Na2O'][i] <= 0:
                AorN = 'None'
            else:
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['Na2O'][i]:
                    AorN = 'Albite'
                else:
                    if self.DataCalculating['Al2O3'][i] > 0:
                        AorN = 'Both'
                    else:
                        AorN = 'Na2SiO3'

            # =IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)

            if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['Na2O'][i] and self.DataCalculating['Al2O3'][
                i] > 0:
                self.DataCalculating['Al2O3'][i] -= self.DataCalculating['Na2O'][i]
            else:
                self.DataCalculating['Al2O3'][i] = 0

            # =IF(AD26='Albite',AC13,IF(AD26='Both',AC7,0))
            # =IF(AD26='Na2SiO3',AC13,IF(AD26='Both',AC13-AD13,0))


            if AorN == 'Albite':
                self.DataCalculating['Cl'][i] = 0

            elif AorN == 'Both':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Na2O'][i] - self.DataCalculating['Al2O3'][i]
                self.DataCalculating['Na2O'][i] = self.DataCalculating['Al2O3'][i]

            elif AorN == 'Na2SiO3':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Na2O'][i]
                self.DataCalculating['Na2O'][i] = 0

            elif AorN == 'None':
                self.DataCalculating['Na2O'][i] = 0
                self.DataCalculating['Cl'][i] = 0

            # =IF(AD7>0,IF(AD12>0,'Anorthite','None'),'None')

            '''
            Seem like should be =IF(AD7>0,IF(AD12>AD7,'Anorthite','Corundum'),'None')

            If Al2O3 is left after alloting orthoclase and albite, then:
            Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
            If Al2O3 exceeds CaO in the preceding calculation, then:
            Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
            Corundum = Al2O3, CaO =0, Al2O3 = 0


                if self.DataCalculating['Al2O3'][i]<=0:
                    AorC='None'
                else:
                    if self.DataCalculating['CaO'][i]>self.DataCalculating['Al2O3'][i]:
                        AorC= 'Anorthite'
                    else:
                        Aorc='Corundum'

            '''

            if self.DataCalculating['Al2O3'][i] <= 0:
                AorC = 'None'
            else:
                if self.DataCalculating['CaO'][i] > 0:
                    AorC = 'Anorthite'
                else:
                    Aorc = 'None'

            # =IF(AE26='Anorthite',IF(AD12>AD7,0,AD7-AD12),AD7)

            # =IF(AE26='Anorthite',IF(AD7>AD12,0,AD12-AD7),AD12)

            # =IF(AE26='Anorthite',IF(AD7>AD12,AD12,AD7),0)

            if AorC == 'Anorthite':
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['CaO'][i]:
                    self.DataCalculating['Sr'][i] = self.DataCalculating['CaO'][i]
                    self.DataCalculating['Al2O3'][i] -= self.DataCalculating['CaO'][i]
                    self.DataCalculating['CaO'][i] = 0

                else:
                    self.DataCalculating['Sr'][i] = self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['CaO'][i] -= self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['Al2O3'][i] = 0

            else:
                self.DataCalculating['Sr'][i] = 0

            Corundum = self.DataCalculating['Al2O3'][i]
            Anorthite = self.DataCalculating['Sr'][i]

            # =IF(AE10>0,IF(AE12>=AE10,'Sphene',IF(AE12>0,'Both','Rutile')),'None')

            if self.DataCalculating['MnO'][i] <= 0:
                SorR = 'None'
            else:
                if self.DataCalculating['CaO'][i] >= self.DataCalculating['MnO'][i]:
                    SorR = 'Sphene'
                elif self.DataCalculating['CaO'][i] > 0:
                    SorR = 'Both'
                else:
                    SorR = 'Rutile'

            # =IF(AF26='Sphene',AE10,IF(AF26='Both',AE12,0))

            # =IF(AF26='Rutile',AE10,IF(AF26='Both',AE10-AE12,0))

            if SorR == 'Sphene':
                self.DataCalculating['MnO'][i] = self.DataCalculating['MnO'][i]
                self.DataCalculating['S'][i] = 0

            elif SorR == 'Rutile':
                self.DataCalculating['S'][i] = self.DataCalculating['MnO'][i]
                self.DataCalculating['MnO'][i] = 0


            elif SorR == 'Both':
                self.DataCalculating['S'][i] = self.DataCalculating['MnO'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['MnO'][i] = self.DataCalculating['CaO'][i]

            elif SorR == 'None':
                self.DataCalculating['MnO'][i] = 0
                self.DataCalculating['S'][i] = 0

            self.DataCalculating['CaO'][i] -= self.DataCalculating['MnO'][i]

            Rutile = self.DataCalculating['S'][i]

            # =IF(AND(AF20>0),IF(AF8>=AF20,'Acmite',IF(AF8>0,'Both','Na2SiO3')),'None')

            if self.DataCalculating['Cl'][i] <= 0:
                ACorN = 'None'
            else:
                if self.DataCalculating['Fe2O3'][i] >= self.DataCalculating['Cl'][i]:
                    ACorN = 'Acmite'
                else:
                    if self.DataCalculating['Fe2O3'][i] > 0:
                        ACorN = 'Both'
                    else:
                        ACorN = 'Na2SiO3'

            # =IF(AG26='Acmite',AF20,IF(AG26='Both',AF8,0))


            # =IF(AG26='Na2SiO3',AF20,IF(AG26='Both',AF20-AG19,0))

            if ACorN == 'Acmite':
                self.DataCalculating['F'][i] = self.DataCalculating['Cl'][i]
                self.DataCalculating['Cl'][i] = 0

            elif ACorN == 'Na2SiO3':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Cl'][i]
                self.DataCalculating['F'][i] = 0

            elif ACorN == 'Both':
                self.DataCalculating['F'][i] = self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Cl'][i] = self.DataCalculating['Cl'][i] - self.DataCalculating['F'][i]

            elif ACorN == 'None':
                self.DataCalculating['F'][i] = 0
                self.DataCalculating['Cl'][i] = 0

            self.DataCalculating['Fe2O3'][i] -= self.DataCalculating['F'][i]

            Acmite = self.DataCalculating['F'][i]

            # =IF(AG8>0,IF(AG9>=AG8,'Magnetite',IF(AG9>0,'Both','Hematite')),'None')


            if self.DataCalculating['Fe2O3'][i] <= 0:
                MorH = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['Fe2O3'][i]:
                    MorH = 'Magnetite'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        MorH = 'Both'
                    else:
                        MorH = 'Hematite'

            # =IF(AH26='Magnetite',AG8,IF(AH26='Both',AG9,0))
            # =IF(AH26='Hematite',AG8,IF(AH26='Both',AG8-AG9,0))



            if MorH == 'Magnetite':
                self.DataCalculating['Fe2O3'][i] = self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Ba'][i] = 0

            elif MorH == 'Hematite':
                self.DataCalculating['Fe2O3'][i] = 0
                self.DataCalculating['Ba'][i] = self.DataCalculating['FeO'][i]


            elif MorH == 'Both':
                self.DataCalculating['Fe2O3'][i] = self.DataCalculating['FeO'][i]
                self.DataCalculating['Ba'][i] = self.DataCalculating['Fe2O3'][i] - self.DataCalculating['FeO'][i]


            elif MorH == 'None':
                self.DataCalculating['Fe2O3'][i] = 0
                self.DataCalculating['Ba'][i] == 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['Fe2O3'][i]

            Magnetite = self.DataCalculating['Fe2O3'][i]
            Hematite = self.DataCalculating['Ba'][i]

            # =IF(AH11>0,AH11/(AH11+AH9),0)

            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]

            if Mg > 0:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 100 * Mg / (Mg + Fe2)})
            else:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 0})

            self.DataCalculating['FeO'][i] += self.DataCalculating['MgO'][i]

            self.DataCalculating['MgO'][i] = 0

            # =IF(AI12>0,IF(AI9>=AI12,'Diopside',IF(AI9>0,'Both','Wollastonite')),'None')


            if self.DataCalculating['CaO'][i] <= 0:
                DorW = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['CaO'][i]:
                    DorW = 'Diopside'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        DorW = 'Both'
                    else:
                        DorW = 'Wollastonite'

            # =IF(AJ26='Diopside',AI12,IF(AJ26='Both',AI9,0))

            # =IF(AJ26='Wollastonite',AI12,IF(AJ26='Both',AI12-AI9,0))



            if DorW == 'Diopside':
                self.DataCalculating['CaO'][i] = self.DataCalculating['CaO'][i]
                self.DataCalculating['S'][i] = 0

            elif DorW == 'Wollastonite':
                self.DataCalculating['S'][i] = self.DataCalculating['CaO'][i]
                self.DataCalculating['CaO'][i] = 0

            elif DorW == 'Both':
                self.DataCalculating['S'][i] = self.DataCalculating['CaO'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['CaO'][i] = self.DataCalculating['FeO'][i]

            elif DorW == 'None':
                self.DataCalculating['CaO'][i] = 0
                self.DataCalculating['S'][i] = 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['CaO'][i]

            Diopside = self.DataCalculating['CaO'][i]

            Quartz = self.DataCalculating['SiO2'][i]

            Zircon = self.DataCalculating['Zr'][i]
            K2SiO3 = self.DataCalculating['P2O5'][i]

            Na2SiO3 = self.DataCalculating['Cl'][i]

            Sphene = self.DataCalculating['MnO'][i]

            Hypersthene = self.DataCalculating['FeO'][i]

            Albite = self.DataCalculating['Na2O'][i]

            Orthoclase = self.DataCalculating['K2O'][i]

            Wollastonite = self.DataCalculating['S'][i]

            # =AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)

            Quartz -= (Zircon +
                       K2SiO3 +
                       Anorthite * 2 +
                       Na2SiO3 +
                       Acmite * 4 +
                       Diopside * 2 +
                       Sphene +
                       Hypersthene +
                       Albite * 6 +
                       Orthoclase * 6 +
                       Wollastonite)

            # =IF(AL5>0,AL5,0)

            if Quartz > 0:
                Quartz = Quartz
            else:
                Quartz = 0

            # =IF(AL13>0,IF(AL5>=0,'Hypersthene',IF(AL13+(2*AL5)>0,'Both','Olivine')),'None')

            if Hypersthene <= 0:
                HorO = 'None'
            else:
                if Quartz >= 0:
                    HorO = 'Hypersthene'
                else:
                    if Hypersthene + 2 * Quartz > 0:
                        HorO = 'Both'
                    else:
                        HorO = 'Olivine'

            # =IF(AN26='Hypersthene',AL13,IF(AN26='Both',AL13+(2*AL5),0))
            # =IF(AN26='Olivine',AL13*0.5,IF(AN26='Both',ABS(AL5),0))
            Old_Hypersthene = Hypersthene
            if HorO == 'Hypersthene':
                Hypersthene = Hypersthene
                Olivine = 0

            elif HorO == 'Both':
                Hypersthene = Hypersthene + Quartz * 2
                Olivine = abs(Quartz)

            elif HorO == 'Olivine':
                Olivine = Hypersthene / 2
                Hypersthene = 0

            elif HorO == 'None':
                Hypersthene = 0
                Olivine = 0

            # =AL5+AL13-(AN13+AN17)
            Quartz += Old_Hypersthene - (Hypersthene + Olivine)

            # =IF(AL12>0,IF(AN5>=0,'Sphene',IF(AL12+AN5>0,'Both','Perovskite')),'None')

            if Sphene <= 0:
                SorP = 'None'
            else:
                if Quartz >= 0:
                    SorP = 'Sphene'
                else:
                    if Sphene + Quartz > 0:
                        SorP = 'Both'
                    else:
                        SorP = 'Perovskite'

            # =IF(AO26='Sphene',AL12,IF(AO26='Both',AL12+AN5,0))
            # =IF(AO26='Perovskite',AL12,IF(AO26='Both',AL12-AO12,0))

            Old_Sphene = Sphene

            if SorP == 'Sphene':
                Sphene = Sphene
                Perovskite = 0

            elif SorP == 'Perovskite':
                Perovskite = Sphene
                Sphene = 0

            elif SorP == 'Both':
                Sphene += Quartz
                Perovskite = Old_Sphene - Sphene

            elif SorP == 'None':
                Sphene = 0
                Perovskite = 0

            Quartz += Old_Sphene - Sphene

            # =IF(AL14>0,IF(AO5>=0,'Albite',IF(AL14+(AO5/4)>0,'Both','Nepheline')),'None')


            if Albite <= 0:
                AlorNe = 'None'
            else:
                if Quartz >= 0:
                    AlorNe = 'Albite'
                else:
                    if Albite + (Quartz / 4) > 0:
                        AlorNe = 'Both'
                    else:
                        AlorNe = 'Nepheline'

            # =AO5+(6*AL14)-(AP14*6)-(AP19*2)


            # =IF(AP26='Albite',AL14,IF(AP26='Both',AL14+(AO5/4),0))
            # =IF(AP26='Nepheline',AL14,IF(AP26='Both',AL14-AP14,0))


            Old_Albite = Albite

            if AlorNe == 'Albite':
                Albite = Albite
                Nepheline = 0

            elif AlorNe == 'Nepheline':
                Nepheline = Albite
                Albite = 0

            elif AlorNe == 'Both':
                Albite += Quartz / 4
                Nepheline = Old_Albite - Albite

            elif AlorNe == 'None':
                Nepheline = 0
                Albite = 0

            Quartz += (6 * Old_Albite) - (Albite * 6) - (Nepheline * 2)

            # =IF(AL8=0,0,AL8/(AL8+(AP14*2)))

            if Anorthite == 0:
                self.DataCalced[k].update({'Plagioclase An content': 0})
            else:
                self.DataCalced[k].update({'Plagioclase An content': 100 * Anorthite / (Anorthite + 2 * Albite)})

            # =IF(AL15>0,IF(AP5>=0,'Orthoclase',IF(AL15+(AP5/2)>0,'Both','Leucite')),'None')

            if Orthoclase <= 0:
                OorL = 'None'
            else:
                if Quartz >= 0:
                    OorL = 'Orthoclase'
                else:
                    if Orthoclase + Quartz / 2 > 0:
                        OorL = 'Both'
                    else:
                        OorL = 'Leucite'

            # =IF(AQ26='Orthoclase',AL15,IF(AQ26='Both',AL15+(AP5/2),0))
            # =IF(AQ26='Leucite',AL15,IF(AQ26='Both',AL15-AQ15,0))

            Old_Orthoclase = Orthoclase

            if OorL == 'Orthoclase':
                Orthoclase = Orthoclase
                Leucite = 0

            elif OorL == 'Leucite':
                Leucite = Orthoclase
                Orthoclase = 0

            elif OorL == 'Both':
                Orthoclase += Quartz / 2
                Leucite = Old_Orthoclase - Orthoclase

            elif OorL == 'None':
                Orthoclase = 0
                Leucite = 0

            # =AP5+(AL15*6)-(AQ15*6)-(AQ20*4)

            Quartz += (Old_Orthoclase * 6) - (Orthoclase * 6) - (Leucite * 4)

            # =IF(AL16>0,IF(AQ5>=0,'Wollastonite',IF(AL16+(AQ5*2)>0,'Both','Larnite')),'None')
            if Wollastonite <= 0:
                WorB = 'None'
            else:
                if Quartz >= 0:
                    WorB = 'Wollastonite'
                else:
                    if Wollastonite + Quartz / 2 > 0:
                        WorB = 'Both'
                    else:
                        WorB = 'Larnite'

            # =IF(AR26='Wollastonite',AL16,IF(AR26='Both',AL16+(2*AQ5),0))
            # =IF(AR26='Larnite',AL16/2,IF(AR26='Both',(AL16-AR16)/2,0))

            Old_Wollastonite = Wollastonite
            if WorB == 'Wollastonite':
                Wollastonite = Wollastonite
                Larnite = 0

            elif WorB == 'Larnite':
                Larnite = Wollastonite / 2
                Wollastonite = 0

            elif WorB == 'Both':
                Wollastonite += Quartz * 2
                Larnite = (Old_Wollastonite - Wollastonite) / 2

            elif WorB == 'None':
                Wollastonite = 0
                Larnite = 0

            # =AQ5+AL16-AR16-AR21
            Quartz += Old_Wollastonite - Wollastonite - Larnite

            # =IF(AL11>0,IF(AR5>=0,'Diopside',IF(AL11+AR5>0,'Both','LarniteOlivine')),'None')

            if Diopside <= 0:
                DorL = 'None'
            else:
                if Quartz >= 0:
                    DorL = 'Diopside'
                else:
                    if Diopside + Quartz > 0:
                        DorL = 'Both'
                    else:
                        DorL = 'LarniteOlivine'

            # =IF(AS26='Diopside',AL11,IF(AS26='Both',AL11+AR5,0))
            # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AN17
            # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AR21

            Old_Diopside = Diopside
            Old_Larnite = Larnite
            Old_Olivine = Olivine
            if DorL == 'Diopside':
                Diopside = Diopside



            elif DorL == 'LarniteOlivine':
                Larnite += Diopside / 2
                Olivine += Diopside / 2
                Diopside = 0

            elif DorL == 'Both':
                Diopside += Quartz
                Larnite += Old_Diopside - Diopside
                Olivine += Old_Diopside - Diopside



            elif DorL == 'None':
                Diopside = 0

            # =AR5+(AL11*2)+AN17+AR21-AS21-(AS11*2)-AS17
            Quartz += (Old_Diopside * 2) + Old_Olivine + Old_Larnite - Larnite - (Diopside * 2) - Olivine

            # =IF(AQ20>0,IF(AS5>=0,'Leucite',IF(AQ20+(AS5/2)>0,'Both','Kalsilite')),'None')

            if Leucite <= 0:
                LorK = 'None'
            else:
                if Quartz >= 0:
                    LorK = 'Leucite'
                else:
                    if Leucite + Quartz / 2 > 0:
                        LorK = 'Both'
                    else:
                        LorK = 'Kalsilite'

            # =IF(AT26='Leucite',AQ20,IF(AT26='Both',AQ20+(AS5/2),0))
            # =IF(AT26='Kalsilite',AQ20,IF(AT26='Both',AQ20-AT20,0))


            Old_Leucite = Leucite

            if LorK == 'Leucite':
                Leucite = Leucite
                Kalsilite = 0

            elif LorK == 'Kalsilite':
                Kalsilite = Leucite
                Leucite = 0

            elif LorK == 'Both':
                Leucite += Quartz / 2
                Kalsilite = Old_Leucite - Leucite

            elif LorK == 'None':
                Leucite = 0
                Kalsilite = 0

            # =AS5+(AQ20*4)-(AT20*4)-(AT22*2)
            Quartz += Old_Leucite * 4 - Leucite * 4 - Kalsilite * 2

            Q = Quartz
            A = Orthoclase
            P = Anorthite + Albite
            F = Nepheline + Leucite + Kalsilite

            for i in self.Minerals:
                exec('self.DataResult[k].update({\'' + i + '\':' + i + '}) ')

                if i == 'Q':
                    m = 'Quartz'

                    exec('self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]}) ')

                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]/self.DataBase[\'' + m + '\'][1]}) ')



                elif i == 'A':
                    m = 'Orthoclase'

                    exec('self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]}) ')
                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]/self.DataBase[\'' + m + '\'][1]}) ')


                elif i == 'P':
                    a = 'Anorthite'
                    b = 'Albite'

                    exec(
                        'self.DataWeight[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]+' + b + '*self.DataBase[\'' + b + '\'][0]}) ')
                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]/self.DataBase[\'' + a + '\'][1]+' + b + '*self.DataBase[\'' + b + '\'][0]/self.DataBase[\'' + b + '\'][1]}) ')


                elif i == 'F':
                    a = 'Nepheline'
                    b = 'Leucite'
                    c = 'Kalsilite'

                    exec(
                        'self.DataWeight[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]+' + b + '*self.DataBase[\'' + b + '\'][0]+' + c + '*self.DataBase[\'' + c + '\'][0]}) ')
                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]/self.DataBase[\'' + a + '\'][1]+' + b + '*self.DataBase[\'' + b + '\'][0]/self.DataBase[\'' + b + '\'][1]+' + c + '*self.DataBase[\'' + c + '\'][0]/self.DataBase[\'' + c + '\'][1]}) ')

                if i not in ['Q', 'A', 'P', 'F', ]:
                    exec('self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + i + '\'][0]}) ')
                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + i + '\'][0]/self.DataBase[\'' + i + '\'][1]}) ')

            self.DI = 0
            # for i in ['Quartz', 'Anorthite', 'Albite', 'Orthoclase', 'Nepheline', 'Leucite', 'Kalsilite']:
            # exec('self.DI+=' + i + '*self.DataBase[\'' + i + '\'][0]')

            exec('self.DI= Quartz +  Anorthite +  Albite +  Orthoclase +  Nepheline +  Leucite +  Kalsilite ')
            DI = Quartz + Anorthite + Albite + Orthoclase + Nepheline + Leucite + Kalsilite

            # print('\n\n DI is\n',DI,'\n\n')
            self.DataCalced[k].update({'Differentiation Index': DI})

    def WriteData(self, target='DataResult'):
        DataToWrite = []
        TMP_DataToWrite = ['Label']

        TMP_DataToWrite = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']

        for j in self.Minerals:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite = []
            k = self.raw.at[i, 'Label']
            TMP_DataToWrite = [self.raw.at[i, 'Label'], self.raw.at[i, 'Marker'], self.raw.at[i, 'Color'],
                               self.raw.at[i, 'Size'], self.raw.at[i, 'Alpha'], self.raw.at[i, 'Style'],
                               self.raw.at[i, 'Width']]
            for j in self.Minerals:
                command = 'TMP_DataToWrite.append((self.' + target + '[k][j]))'
                try:
                    exec(command)
                except(KeyError):
                    pass
            DataToWrite.append(TMP_DataToWrite)
        return (DataToWrite)

    def WriteCalced(self, target='DataCalced'):
        DataToWrite = []
        TMP_DataToWrite = ['Label']

        TMP_DataToWrite = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
        for j in self.Calced:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite = []
            k = self.raw.at[i, 'Label']
            TMP_DataToWrite = [self.raw.at[i, 'Label'], self.raw.at[i, 'Marker'], self.raw.at[i, 'Color'],
                               self.raw.at[i, 'Size'], self.raw.at[i, 'Alpha'], self.raw.at[i, 'Style'],
                               self.raw.at[i, 'Width']]

            for j in self.Calced:
                command = 'TMP_DataToWrite.append((self.' + target + '[k][j]))'
                try:

                    exec('#print((self.' + target + '[k][j]))')

                    exec(command)
                except(KeyError):
                    pass

            DataToWrite.append(TMP_DataToWrite)

        # print('\n',DataToWrite,'\n')
        return (DataToWrite)

    def CIPW(self):

        self.chooser_label.setText('Show Result of ' + self.ChooseItems[self.chooser.value() - 1])
        self.Calc()
        a = []
        a.append(self.WriteData(target='DataResult'))
        a.append(self.WriteData(target='DataWeight'))
        a.append(self.WriteData(target='DataVolume'))
        a.append(self.WriteCalced(target='DataCalced'))

        tmp = a[self.chooser.value() - 1]

        labels = tmp[0]
        newtmp = []

        for s in range(len(tmp)):
            if s != 0:
                newtmp.append(tmp[s])

        self.newdf = pd.DataFrame.from_records(newtmp, columns=labels)

        ##print('\n',tmp,'\n')

        # self.newdf = pd.DataFrame(tmp)



        self.model = PandasModel(self.newdf)
        self.tableView.setModel(self.model)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.newdf.to_excel(DataFileOutput, encoding='utf-8')

    def QAPF(self):
        self.qapfpop = QAPF(df=self.newdf)
        try:
            self.qapfpop.QAPF()
        except(TypeError):
            pass
        self.qapfpop.show()


class QAPF(AppForm, Tool):

    infotext ='Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%.'
    reference = 'Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Q', u'A', u'P', u'F']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1),
                     (49, -50 * np.sqrt(3) - 4)]

    Labels = ['quartzolite',

              'quartz-rich\ngranitoid',

              'granite',

              'alkali\nfeldspar\ngranite',
              '(syeno\ngranite)',
              '(monzo\ngranite)',
              'granodiorite',
              'tonalite',

              'quartz\nalkali\nfeldspar\nsyenite',
              'quartz\nsyenite',
              'quartz\nmonzonite',
              'quartz\nmonzodiorite\nquartz\nmonzogabbro',
              'quartz\ndiorite\nquartz gabbro\n quartz\nanorthosite',

              'alkali\nfeldspar\nsyenite',
              'syenite',
              'monzonite',
              'monzodiorite\nmonzogabbro',
              'diorite\ngabbro\nanorthosite',

              'foid-bearing\nalkali\nfeldspar\nsyenite',
              'foid-bearing\nsyenite',
              'foid-bearing\nmonzonite',
              'foid-bearing\nmonzodiorite\nfoid-bearing\nmonzogabbro',
              'foid-bearing\ndiorite\nfoid-bearing gabbro\nfoid-bearing\nanorthosite',

              'foid\nsyenite',
              'foid\nmonzosyenite',
              'foid\nmonzodiorite\nfoid\nmonzogabbro',
              'foid\ndiorite\nfoid\ngabbro',
              'foidolite']

    Locations = [(5, 5, 95),

                 (10, 10, 80),

                 (35, 15, 50),

                 (45, 5, 50),
                 (45, 25, 30),
                 (35, 35, 30),
                 (25, 45, 30),
                 (5, 45, 50),

                 (85, 5, 10),
                 (75, 15, 10),
                 (45, 45, 10),
                 (15, 75, 10),
                 (5, 85, 10),

                 (93, 5, 2),
                 (83, 15, 2),
                 (53, 53, 2),
                 (15, 83, 2),
                 (5, 93, 2),

                 (95, 3, -8),
                 (75, 23, -8),
                 (49, 49, -8),
                 (23, 75, -8),
                 (3, 95, -8),

                 (63, 7, -30),
                 (50, 20, -30),
                 (20, 50, -30),
                 (7, 63, -30),
                 (10, 10, -80)]

    Offset = [(-30, 0),

              (-30, 0),

              (-20, 0),

              (-70, 30),
              (-50, 30),
              (-30, 0),
              (0, 0),
              (30, 20),

              (-70, 15),
              (-10, 0),
              (-40, 0),
              (-50, -5),
              (30, 15),

              (-80, 5),
              (0, 0),
              (-40, 0),
              (-50, -5),
              (60, 5),

              (-80, -15),
              (-40, 0),
              (-40, 0),
              (-20, -15),
              (50, -30),

              (-80, 0),
              (-40, 0),
              (-40, 0),
              (60, 0),
              (-30, 0)]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to DualTri')

        self.raw = self._df
        self.create_main_frame()
        self.create_status_bar()

        TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (35, 65, 0)], Sort='',
                Width=1, Color='black', Style='-',
                Alpha=0.7, Label='')

        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8, 12), dpi=self.dpi)
        # 8 * np.sqrt(3)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.QAPF)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.QAPF)  # int

        self.Tag_cb = QCheckBox('&Plutonic')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.QAPF)  # int

        if (self.Tag_cb.isChecked()):
            self.Tag_cb.setText('&Plutonic')
        else:
            self.Tag_cb.setText('&Volcanic')

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.QAPF)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.Tag_cb, self.detail_cb, self.legend_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.detailtext = QLineEdit(self)
        self.detailtext.setText(self.infotext)
        self.vbox.addWidget(self.detailtext)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def QAPF(self):

        self.axes.clear()
        self.axes.axis('off')
        self.Tags = []

        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)

        s = [TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (0, 100, 0)], Sort='',
                     Width=1, Color='black', Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        if (self.Tag_cb.isChecked()):

            self.Labels = ['quartzolite',

                           'quartz-rich\ngranitoid',

                           'granite',

                           'alkali\nfeldspar\ngranite',
                           '(syeno\ngranite)',
                           '(monzo\ngranite)',
                           'granodiorite',
                           'tonalite',

                           'quartz\nalkali\nfeldspar\nsyenite',
                           'quartz\nsyenite',
                           'quartz\nmonzonite',
                           'quartz\nmonzodiorite\nquartz\nmonzogabbro',
                           'quartz\ndiorite\nquartz gabbro\n quartz\nanorthosite',

                           'alkali\nfeldspar\nsyenite',
                           'syenite',
                           'monzonite',
                           'monzodiorite\nmonzogabbro',
                           'diorite\ngabbro\nanorthosite',

                           'foid-bearing\nalkali\nfeldspar\nsyenite',
                           'foid-bearing\nsyenite',
                           'foid-bearing\nmonzonite',
                           'foid-bearing\nmonzodiorite\nfoid-bearing\nmonzogabbro',
                           'foid-bearing\ndiorite\nfoid-bearing gabbro\nfoid-bearing\nanorthosite',

                           'foid\nsyenite',
                           'foid\nmonzosyenite',
                           'foid\nmonzodiorite\nfoid\nmonzogabbro',
                           'foid\ndiorite\nfoid\ngabbro',
                           'foidolite']

            self.Locations = [(5, 5, 95),

                              (10, 10, 80),

                              (35, 15, 50),

                              (45, 5, 50),
                              (45, 25, 30),
                              (35, 35, 30),
                              (25, 45, 30),
                              (5, 45, 50),

                              (85, 5, 10),
                              (75, 15, 10),
                              (45, 45, 10),
                              (15, 75, 10),
                              (5, 85, 10),

                              (93, 5, 2),
                              (83, 15, 2),
                              (53, 53, 2),
                              (15, 83, 2),
                              (5, 93, 2),

                              (95, 3, -8),
                              (75, 23, -8),
                              (49, 49, -8),
                              (23, 75, -8),
                              (3, 95, -8),

                              (63, 7, -30),
                              (50, 20, -30),
                              (20, 50, -30),
                              (7, 63, -30),
                              (10, 10, -80)]

            self.Offset = [(-30, 0),

                           (-30, 0),

                           (-20, 0),

                           (-70, 30),
                           (-50, 30),
                           (-30, 0),
                           (0, 0),
                           (30, 20),

                           (-70, 15),
                           (-10, 0),
                           (-40, 0),
                           (-50, -5),
                           (30, 15),

                           (-80, 5),
                           (0, 0),
                           (-40, 0),
                           (-50, -5),
                           (60, 5),

                           (-80, -15),
                           (-40, 0),
                           (-40, 0),
                           (-20, -15),
                           (50, -30),

                           (-80, 0),
                           (-40, 0),
                           (-40, 0),
                           (60, 0),
                           (-30, 0)]
            self.Tag_cb.setText('&Plutonic')

            self.setWindowTitle(
                'QAPF modal classification of plutonic rocks (based on Streckeisen, 1976, Fig. 1a).')

            D1 = (0, 0, 100)
            L1 = [(10, 0, 90), (0, 10, 90)]
            L2 = [(40, 0, 60), (0, 40, 60)]
            L3 = [(80, 0, 20), (0, 80, 20)]

            L4 = [(95, 0, 5), (0, 95, 5)]

            SL1 = [D1, (90, 10, 0)]
            SL2 = [D1, (65, 35, 0)]
            SL3 = [D1, (35, 65, 0)]
            SL4 = [D1, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL21 = self.TriCross(SL2, L2)
            CL22 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L2)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL21 = [CL21, CL22]
            NSL22 = [CL22, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, (10, 90, 0)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            D2 = (0, 0, -100)
            L2 = [(40, 0, -60), (0, 40, -60)]
            L3 = [(90, 0, -10), (0, 90, -10)]

            SL1 = [D2, (90, 10, 0)]
            SL2 = [D2, (65, 35, 0)]
            SL3 = [D2, (35, 65, 0)]
            SL4 = [D2, (10, 90, 0)]

            SL5 = [(20, 20, -60), (45, 45, -10)]

            CL1 = self.TriCross(SL1, L2)
            CL2 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L3)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL2 = [CL2, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, (10, 90, 0)]

            s = [
                TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=SL5, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label='')]
            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)


        else:
            self.Labels = ['rhyolite',

                           'alkali\nfeldspar\rhyolite',

                           'dacite',

                           'quartz\nalkali\nfeldspar\ntrachyte',
                           'quartz\ntrachyte',
                           'quartz\nlatite',
                           'basalt\nandesite',

                           'alkali\nfeldspar\ntrachyte',
                           'trachyte',
                           'latite',

                           'foid-bearing\nalkali\nfeldspar\ntrachyte',
                           'foid-bearing\ntrachyte',
                           'foid-bearing\nlatite',

                           'phonolite',
                           'tephritic\nphonolite',
                           ' phonolitic\nbasanite\n(olivine > 10%)\nphonolitic\ntephrite\n(olivine < 10%)',
                           ' basanite\n(olivine > 10%)\ntephrite\n(olivine < 10%)',
                           'phonolitic\nfoidite',
                           'tephritic\nfoidite',
                           'foidoite']

            self.Locations = [(35, 15, 50),

                              (45, 5, 50),

                              (20, 50, 30),

                              (85, 5, 10),
                              (75, 15, 10),
                              (45, 45, 10),
                              (15, 75, 10),

                              (93, 5, 2),
                              (83, 15, 2),
                              (53, 53, 2),

                              (95, 3, -8),
                              (75, 23, -8),
                              (49, 49, -8),

                              (63, 7, -30),
                              (50, 20, -30),
                              (20, 50, -30),
                              (7, 63, -30),
                              (16, 8, -76),
                              (8, 16, -76),
                              (4, 4, -92)]

            self.Offset = [(-20, 0),

                           (-70, 30),

                           (0, 0),

                           (-70, 15),
                           (-10, 0),
                           (-40, 0),
                           (-30, -5),

                           (-80, 5),
                           (0, 0),
                           (-40, 0),

                           (-80, -15),
                           (-40, 0),
                           (-40, 0),

                           (-80, 0),
                           (-40, 0),
                           (-40, 0),
                           (60, 0),
                           (-40, 20),
                           (0, 20),
                           (-20, 0)]
            self.Tag_cb.setText('&Volcanic')

            self.setWindowTitle(
                'QAPF modal classification of volcanic rocks (based on Streckeisen, 1978, Fig. 1).\nQ = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%.')

            D = (0, 0, 100)
            L1 = [(10, 0, 90), (0, 10, 90)]
            L2 = [(40, 0, 60), (0, 40, 60)]
            L3 = [(80, 0, 20), (0, 80, 20)]

            L4 = [(95, 0, 5), (0, 95, 5)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''), ]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            SL1 = [D, (90, 10, 0)]
            SL2 = [D, (65, 35, 0)]
            SL3 = [D, (35, 65, 0)]
            SL4 = [D, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL21 = self.TriCross(SL2, L2)
            CL22 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L2)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            TL4 = self.TriCross(SL3, L4)

            NL4 = [(95, 0, 5), TL4]

            NSL1 = [CL1, (90, 10, 0)]
            NSL21 = [CL21, CL22]
            NSL22 = [CL22, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, CL42]

            s = [TriLine(Points=NL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            D = (0, 0, -100)
            L1 = [(10, 0, -90), (0, 10, -90)]
            L2 = [(40, 0, -60), (0, 40, -60)]
            L3 = [(90, 0, -10), (0, 90, -10)]

            SL5 = [(5, 5, -90), (45, 45, -10)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=SL5, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            SL1 = [D, (90, 10, 0)]
            SL2 = [D, (65, 35, 0)]
            SL3 = [D, (35, 65, 0)]
            SL4 = [D, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL2 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L3)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL2 = [CL2, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, CL42]

            s = [TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=8, )

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

        if (self.detail_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

        raw = self._df
        PointLabels = []
        TPoints = []

        for i in range(len(raw)):
            q = raw.at[i, 'Q']
            f = raw.at[i, 'F']
            a = raw.at[i, 'A']
            p = raw.at[i, 'P']

            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            if (q != 0 and q != ''):
                TPoints.append(TriPoint((a, p, q), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))
            else:
                TPoints.append(TriPoint((a, p, 0 - f), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')

        if (self.legend_cb.isChecked()):
            # a = int(self.slider.value())
            # self.axes.legend(loc=a, fontsize=9,bbox_to_anchor=(0, 0))
            self.axes.legend(loc=3,prop=fontprop, bbox_to_anchor=(0, 0))

        self.canvas.draw()


class Pearce(AppForm):
    reference = 'Pearce, J. A., Harris, N. B. W., and Tindle, A. G., 1984, Trace Element Discrimination Diagrams for the Tectonic Interpretation of Granitic Rocks: Journal of Petrology, v. 25, no. 4, p. 956-983.'
    Lines = []
    Tags = []
    description = 'Pearce diagram (after Julian A. Pearce et al., 1984).\n syn-COLG: syn-collision granites\n VAG: volcanic arc granites\n WPG: within plate granites\n ORG: ocean ridge granites '
    text = [u'0.1', u'1', u'10', u'100', u'1000', u'10000', u'100000', u'1000000', u'10000000']

    Condation0 = {'BaseLines': [[(2, 80), (55, 300)],
                                [(55, 300), (400, 2000)],
                                [(55, 300), (51.5, 8)],
                                [(51.5, 8), (50, 1)],
                                [(51.5, 8), (2000, 400)], ],
                  'xLabel': r'Y+Nb (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(1, 3), (1, 1), (2.4, 2.4), (3, 1)],
                  'Frame': [[(0, 0), (0, 4)],
                            [(0, 0), (4, 0)],],

                  'BaseY': [[(0, 1), (-0.1, 1)],
                            [(0, 2), (-0.1, 2)],
                            [(0, 3), (-0.1, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)],
                            [(3, 0), (3, -0.1)], ]

                  }

    Condation1 = {'BaseLines': [[(0.5, 140), (6, 200)],
                                [(6, 200), (50, 2000)],
                                [(6, 200), (6, 8)],
                                [(6, 8), (6, 1)],
                                [(6, 8), (200, 400)], ],
                  'xLabel': r'Yb+Ta (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 3), (0.5, 1), (1.5, 2.4), (2, 1)],
                  'Frame': [[(-1, 0), (-1, 3)],
                            [(-1, 0), (3, 0)],],

                  'BaseY': [[(-1, 1), (-1.1, 1)],
                            [(-1, 2), (-1.1, 2)],
                            [(-1, 3), (-1.1, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(-1, 0), (-1, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)], ]
                  }

    Condation2 = {'BaseLines': [[(1, 2000), (50, 10)],
                                [(40, 1), (50, 10)],
                                [(50, 10), (1000, 100)],
                                [(25, 25), (1000, 400)], ],
                  'xLabel': r'Y (PPM)',
                  'yLabel': r'Nb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 1.5), (0.5, 2), (2, 2), (2, 1)],
                  'Frame': [[(-0.5, 0), (-0.5, 3)],
                            [(-0.5, 0), (3, 0)],],

                  'BaseY': [[(-0.5, 1), (-0.6, 1)],
                            [(-0.5, 2), (-0.6, 2)],
                            [(-0.5, 3), (-0.6, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)],]

                  }

    Condation3 = {'BaseLines': [[(0.55, 20), (3, 2)],
                                [(0.1, 0.35), (3, 2)],
                                [(3, 2), (5, 1)],
                                [(5, 0.05), (5, 1)],
                                [(5, 1), (100, 7)],
                                [(3, 2), (100, 20)], ],
                  'xLabel': r'Yb (PPM)',
                  'yLabel': r'Ta (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(-0.5, 0.1), (-0.5, -1), (0.7, 1), (2, 0.5)],
                  'Frame': [[(-1, -1.5), (-1, 2)],
                            [(-1, -1.5), (2, -1.5)],],

                  'BaseY': [[(-1, 0), (-1.1, 0)],
                            [(-1, 1), (-1.1, 1)],
                            [(-1, 2), (-1.1, 2)],],

                  'BaseX': [[(-1, -1.5), (-1, -1.6)],
                            [(0, -1.5), (0, -1.6)],
                            [(1, -1.5), (1, -1.6)],
                            [(2, -1.5), (2, -1.6)], ]
                  }

    condation = [Condation0, Condation1, Condation2, Condation3]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(
            'Pearce diagram (after Julian A. Pearce et al., 1984).\n syn-COLG: syn-collision granites\n VAG: volcanic arc granites\n WPG: within plate granites\n ORG: ocean ridge granites ')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Pearce')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        self.axes.axis('off')

        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Pearce)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Pearce)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Pearce)  # int

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.Pearce)  # int

        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 3)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.Pearce)  # int

        self.standard_label = QLabel('Type')

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, self.slider_label, self.slider, self.detail_cb, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Pearce(self):

        self.WholeData = []

        raw = self._df

        a = int(self.standard.value())

        self.axes.clear()
        self.axes.axis('off')

        self.axes.set_xlabel(self.condation[a]['xLabel'])
        self.axes.set_ylabel(self.condation[a]['yLabel'])


        s=[]
        for i in self.condation[a]['Frame']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            s.append((i[1][0]/2,i[1][1]/2))


        self.axes.annotate(self.condation[a]['xLabel'], s[1], xycoords='data', xytext=(-2, -50),
                           textcoords='offset points',
                           fontsize=9, color='grey', alpha=0.8)
        self.axes.annotate(self.condation[a]['yLabel'], s[0], xycoords='data', xytext=(-50, -2),
                           textcoords='offset points',rotation=90,
                           fontsize=9, color='grey', alpha=0.8)



        for i in self.condation[a]['BaseX']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            if (type(i[0][0])== int):
                self.axes.annotate(str(int(np.power(10, np.float32(i[0][0])))), i[1], xycoords='data', xytext=(-2,-10),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)

        for i in self.condation[a]['BaseY']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            if (type(i[0][1]) == int):
                self.axes.annotate(str(int(np.power(10, np.float32(i[0][1])))), i[1], xycoords='data', xytext=(-15,-10),
                               textcoords='offset points',
                               fontsize=9, color='grey', alpha=0.8)


        BaseLines = self.condation[a]['BaseLines']

        for i in BaseLines:
            self.DrawLogLine(l=i)
        PointLabels = []

        self.Tags = []

        for i in range(len(self.condation[a]['Labels'])):
            self.Tags.append(Tag(Label=self.condation[a]['Labels'][i], Location=self.condation[a]['Locations'][i]))

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0

            if (a == 0):
                x, y = (raw.at[i, 'Y'] + raw.at[i, 'Nb']), raw.at[i, 'Rb']
            elif (a == 1):
                x, y = (raw.at[i, 'Yb'] + raw.at[i, 'Ta']), raw.at[i, 'Rb']
            elif (a == 2):
                x, y = raw.at[i, 'Y'], raw.at[i, 'Nb']
            elif (a == 3):
                x, y = raw.at[i, 'Yb'], raw.at[i, 'Ta']

            self.axes.scatter(math.log(x, 10), math.log(y, 10), marker=raw.at[i, 'Marker'],
                              s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                              label=TmpLabel, edgecolors='black')

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7)

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        if (self.detail_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

        self.canvas.draw()


class Harker(AppForm):
    Lines = []
    Tags = []
    description = 'Harker diagram'
    usefulelements = ['SiO2',
                      'TiO2',
                      'Al2O3',
                      'TFe2O3',
                      'Fe2O3',
                      'FeO',
                      'TFe',
                      'MnO',
                      'MgO',
                      'CaO',
                      'Na2O',
                      'K2O',
                      'P2O5',
                      'Loi',
                      'DI',
                      'Mg#',
                      'Li',
                      'Be',
                      'Sc',
                      'V',
                      'Cr',
                      'Co',
                      'Ni',
                      'Cu',
                      'Zn',
                      'Ga',
                      'Ge',
                      'Rb',
                      'Sr',
                      'Y',
                      'Zr',
                      'Nb',
                      'Cs',
                      'Ba',
                      'La',
                      'Ce',
                      'Pr',
                      'Nd',
                      'Sm',
                      'Eu',
                      'Gd',
                      'Tb',
                      'Dy',
                      'Ho',
                      'Er',
                      'Tm',
                      'Yb',
                      'Lu',
                      'III',
                      'Ta',
                      'Pb',
                      'Th',
                      'U']
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Harker diagram')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Harker')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Harker)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Harker)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Harker)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Harker)  # int

        self.x_element_label = QLabel('X')

        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Harker)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(0)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Harker)  # int

        self.y_element_label = QLabel('Y')

        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Harker)  # int

        #
        # Layout with box sizers
        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, self.slider_label, self.slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Harker(self):

        self.WholeData = []

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        self.axes.clear()

        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])

        PointLabels = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0
            xuse, yuse = 0, 0

            x, y = raw.at[i, self.items[a]], raw.at[i, self.items[b]]

            try:
                xuse = x
                yuse = y

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)

                    self.axes.set_xlabel('$log10$ ' + self.items[a])

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.axes.set_ylabel('$log10$ ' + self.items[b])

                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel, edgecolors='black')
            except(ValueError):
                pass

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        self.canvas.draw()


class ZirconTiTemp(AppForm):
    reference = 'Ferry J M, Watson E B. New thermodynamic models and revised calibrations for the Ti-in-zircon and Zr-[J]. Contributions to Mineralogy & Petrology, 2007, 154(4):429-437.'
    Calced = ['Temperature']

    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Zircon Ti Temperature Calculator')

        self._df = df
        self.raw = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, ]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def ZirconTiTemp(self):

        MaxTemps = []
        MinTemps = []
        MidTemps = []

        for i in range(len(self.raw)):
            Ti = self.raw.at[i, 'Ti']

            try:
                ASiO2 = self.raw.at[i, 'ASiO2']
            except(KeyError):
                ASiO2 = 1

            try:
                ATiO2 = self.raw.at[i, 'ATiO2']
            except(KeyError):
                ATiO2 = 1

            TiTemp1 = (4800 + 86) / ((5.711 + 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp2 = (4800 - 86) / ((5.711 + 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp3 = (4800 + 86) / ((5.711 - 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp4 = (4800 - 86) / ((5.711 - 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTempBig, TiTempSmall = max([TiTemp1, TiTemp2, TiTemp3, TiTemp4]), min(
                ([TiTemp1, TiTemp2, TiTemp3, TiTemp4]))

            MaxTemps.append(TiTempBig)
            MinTemps.append(TiTempSmall)
            MidTemps.append((TiTempSmall + TiTempBig) / 2)

        tmpdata = {'Temp Max': MaxTemps, 'Temp Min': MinTemps, 'Temp Mid': MidTemps, }

        tmpdftoadd = pd.DataFrame(tmpdata)

        self.newdf = pd.concat([tmpdftoadd, self.raw], axis=1)
        self.model = PandasModel(self.newdf)
        self.tableView.setModel(self.model)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.newdf.to_excel(DataFileOutput, encoding='utf-8')


class RutileZrTemp(AppForm):
    reference = 'Ferry J M, Watson E B. New thermodynamic models and revised calibrations for the Ti-in-zircon and Zr-[J]. Contributions to Mineralogy & Petrology, 2007, 154(4):429-437.'
    Calced = ['Temperature']

    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Rutile Zr Temperature Calculator')

        self._df = df
        self.raw = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, ]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def RutileZrTemp(self):

        MaxTemps = []
        MinTemps = []
        MidTemps = []

        for i in range(len(self.raw)):
            Zr = self.raw.at[i, 'Zr']

            try:
                ASiO2 = self.raw.at[i, 'ASiO2']
            except(KeyError):
                ASiO2 = 1

            ZrTemp1 = (4530 + 111) / ((7.42 + 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp2 = (4530 - 111) / ((7.42 + 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp3 = (4530 + 111) / ((7.42 - 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp4 = (4530 - 111) / ((7.42 - 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTempBig, ZrTempSmall = max([ZrTemp1, ZrTemp2, ZrTemp3, ZrTemp4]), min(
                ([ZrTemp1, ZrTemp2, ZrTemp3, ZrTemp4]))

            MaxTemps.append(ZrTempBig)
            MinTemps.append(ZrTempSmall)
            MidTemps.append((ZrTempSmall + ZrTempBig) / 2)

        tmpdata = {'Temp Max': MaxTemps, 'Temp Min': MinTemps, 'Temp Mid': MidTemps, }

        tmpdftoadd = pd.DataFrame(tmpdata)

        self.newdf = pd.concat([tmpdftoadd, self.raw], axis=1)
        self.model = PandasModel(self.newdf)
        self.tableView.setModel(self.model)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.newdf.to_excel(DataFileOutput, encoding='utf-8')


class Cluster(AppForm):
    Lines = []
    Tags = []
    description = 'Cluster diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Cluster Data')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Cluster')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveDataFile)

        # self.save_button.clicked.connect(self.saveImgFile)


        self.draw_button = QPushButton('&Show')
        self.draw_button.clicked.connect(self.Show)

        self.legend_cb = QCheckBox('&Horizontal')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Cluster)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Cluster)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def Cluster(self):

        if (self.legend_cb.isChecked()):
            self.legend_cb.setText('&Horizontal')
        else:
            self.legend_cb.setText('&Vertical')

        self.WholeData = []

        self.axes.clear()

        dataframe = self._df

        ItemsAvalibale = self._df.columns.values.tolist()

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Label', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        self._df = dataframe

        self.model = PandasModel(self._df)
        self.tableView.setModel(self.model)

        PointLabels = []


        # self.canvas.draw()

    def Show(self):
        dataframe = self._df
        corr = 1 - dataframe.corr()

        try:
            corr_condensed = hc.distance.squareform(corr)  # convert to condensed

            z = hc.linkage(corr_condensed, method='average')

            dendrogram = hc.dendrogram(abs(z), labels=corr.columns)

            plt.title('Cluster Diagram')
            plt.show()

        except(ValueError):
            reply = QMessageBox.warning(self, 'Value Error',
                                        'Check Your Data and make sure it contains only numerical values.')
            pass


class XY(AppForm):
    Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
               u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']

    NameChosen = 'OIB'
    Standards = {
        'OIB': {'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                'K': 12000, 'La': 37, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200, 'Gd': 7.62,
                'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3},
        'EMORB': {'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                  'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155, 'P': 620,
                  'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                  'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                  'Yb': 2.37, 'Lu': 0.354},
        'C1': {'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
               'Ta': 0.014, 'K': 545, 'La': 0.237, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
               'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
               'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
               'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
               'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
               'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
               'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.737, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
               'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
        'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                  'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                  'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                  'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                  'Yb': 3.05, 'Lu': 0.455}, }

    Lines = []
    Tags = []

    xlabel = 'x'
    ylabel = 'y'

    description = 'X-Y diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    width_plot = 100.0
    height_plot = 100.0

    width_load = width_plot
    height_load = height_plot

    polygon = []
    polyline = []
    line = []

    strgons = []
    strlines = []
    strpolylines = []

    extent = 0

    Left = 0
    Right = 0
    Up = 0
    Down = 0

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('X-Y diagram')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

        self.polygon = 0
        self.polyline = 0

        self.flag = 0

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Reset)

        self.load_button = QPushButton('&Load')
        self.load_button.clicked.connect(self.Load)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Magic)  # int

        self.Normalize_cb = QCheckBox('&Normalize')
        self.Normalize_cb.setChecked(False)
        self.Normalize_cb.stateChanged.connect(self.Magic)  # int

        self.norm_slider_label = QLabel('Standard:' + self.NameChosen)
        self.norm_slider = QSlider(Qt.Horizontal)
        self.norm_slider.setRange(0, 4)
        self.norm_slider.setValue(0)
        self.norm_slider.setTracking(True)
        self.norm_slider.setTickPosition(QSlider.TicksBothSides)
        self.norm_slider.valueChanged.connect(self.Magic)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Magic)  # int

        self.x_element_label = QLabel('X')

        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(0)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Magic)  # int

        self.y_element_label = QLabel('Y')

        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Magic)  # int

        self.width_size_seter_label = QLabel('Width')
        self.width_size_seter = QLineEdit(self)

        self.width_size_seter.textChanged[str].connect(self.WChanged)

        self.height_size_seter_label = QLabel('height')
        self.height_size_seter = QLineEdit(self)

        self.height_size_seter.textChanged[str].connect(self.HChanged)

        self.Left_size_seter_label = QLabel('Left')
        self.Left_size_seter = QLineEdit(self)

        self.Left_size_seter.textChanged[str].connect(self.LeftChanged)

        self.Right_size_seter_label = QLabel('Right')
        self.Right_size_seter = QLineEdit(self)

        self.Right_size_seter.textChanged[str].connect(self.RightChanged)

        self.Up_size_seter_label = QLabel('Up')
        self.Up_size_seter = QLineEdit(self)

        self.Up_size_seter.textChanged[str].connect(self.UpChanged)

        self.Down_size_seter_label = QLabel('Down')
        self.Down_size_seter = QLineEdit(self)

        self.Down_size_seter.textChanged[str].connect(self.DownChanged)

        #
        # Layout with box sizers
        #
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.hbox6 = QHBoxLayout()
        self.hbox7 = QHBoxLayout()

        for w in [self.Normalize_cb, self.norm_slider_label, self.norm_slider]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.save_button, self.draw_button, self.load_button,
                  self.legend_cb, self.slider_label, self.slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        for w in [self.width_size_seter_label, self.width_size_seter]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)

        for w in [self.height_size_seter_label, self.height_size_seter]:
            self.hbox5.addWidget(w)
            self.hbox5.setAlignment(w, Qt.AlignVCenter)

        for w in [self.Left_size_seter, self.Left_size_seter_label, self.Right_size_seter, self.Right_size_seter_label]:
            self.hbox6.addWidget(w)
            self.hbox6.setAlignment(w, Qt.AlignVCenter)

        for w in [self.Down_size_seter, self.Down_size_seter_label, self.Up_size_seter, self.Up_size_seter_label]:
            self.hbox7.addWidget(w)
            self.hbox7.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.vbox.addLayout(self.hbox5)
        self.vbox.addLayout(self.hbox6)
        self.vbox.addLayout(self.hbox7)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def Load(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         '选取文件',
                                                         '~/',
                                                         'PNG Files (*.png);;JPG Files (*.jpg);;SVG Files (*.svg)')  # 设置文件扩展名过滤,注意用双分号间隔

        print(fileName, '\t', filetype)

        if ('svg' in fileName):
            doc = minidom.parse(fileName)  # parseString also exists
            polygon_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polygon')]
            polyline_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polyline')]

            svg_width = [path.getAttribute('width') for path in doc.getElementsByTagName('svg')]
            svg_height = [path.getAttribute('height') for path in doc.getElementsByTagName('svg')]

            # print(svg_width)
            # print(svg_height)

            digit = '01234567890.-'
            width = svg_width[0].replace('px', '').replace('pt', '')
            height = svg_height[0].replace('px', '').replace('pt', '')

            self.width_load = float(width)
            self.height_load = float(height)

            soup = BeautifulSoup(open(fileName), 'lxml')

            tmpgon = soup.find_all('polygon')
            tmppolyline = soup.find_all('polyline')
            tmptext = soup.find_all('text')
            tmpline = soup.find_all('line')

            tmppath = soup.find_all('path')

            self.strgons = []
            for i in tmpgon:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polygon.attrs
                self.strgons.append(k['points'].split())

            self.strpolylines = []
            for i in tmppolyline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polyline.attrs
                self.strpolylines.append(k['points'].split())

            self.strlines = []
            for i in tmpline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.line.attrs
                a = str(k['x1']) + ',' + str(k['y1']) + ' ' + str(k['x2']) + ',' + str(k['y2'])
                self.strlines.append(a.split())

            self.strpath = []
            for i in tmppath:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.path.attrs
                self.strpath.append(k['d'].split())

            # print(self.strpath)



            self.polygon = []
            for i in self.strgons:
                m = self.Read(i)
                m.append(m[0])
                self.polygon.append(m)

            self.polyline = []
            for i in self.strpolylines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                self.polyline.append(m)

            self.line = []
            for i in self.strlines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                self.line.append(m)


        elif ('png' in fileName or 'jpg' in fileName):

            self.img = mpimg.imread(fileName)
            self.flag = 1

        self.Magic()

    def Reset(self):
        self.flag = 0
        self.Magic()

    def WChanged(self, text):
        w = 'width ' + text
        self.width_size_seter_label.setText(w)
        self.width_size_seter_label.adjustSize()

        try:
            self.width_plot = float(text)
        except:
            pass

        self.x_scale = self.width_plot / self.width_load

        self.polygon = []
        for i in self.strgons:
            m = self.Read(i)
            m.append(m[0])
            self.polygon.append(m)

        self.polyline = []
        for i in self.strpolylines:
            m = self.Read(i)
            # print('i: ',i,'\n m:',m)
            self.polyline.append(m)

        self.line = []
        for i in self.strlines:
            m = self.Read(i)
            # print('i: ',i,'\n m:',m)
            self.line.append(m)

        self.Magic()

    def HChanged(self, text):
        h = 'height ' + text
        self.height_size_seter_label.setText(h)
        self.height_size_seter_label.adjustSize()

        try:
            self.height_plot = float(text)
        except:
            pass

        self.y_scale = self.height_plot / self.height_load

        self.polygon = []
        for i in self.strgons:
            m = self.Read(i)
            m.append(m[0])
            self.polygon.append(m)

        self.polyline = []
        for i in self.strpolylines:
            m = self.Read(i)
            # print('i: ',i,'\n m:',m)
            self.polyline.append(m)

        self.line = []
        for i in self.strlines:
            m = self.Read(i)
            # print('i: ',i,'\n m:',m)
            self.line.append(m)

        self.Magic()

    # text_location= [path.getAttribute('transform') for path in doc.getElementsByTagName('text')]
    '''
    tmppolygon_points=[]
    for i in polygon_points:
        tmppolygon_points.append(i.split())

    polygon=[]
    for i in tmppolygon_points:
        for l in range(len(i)):
            a=float((i[l].split(','))[0])
            b=float((i[l].split(','))[1])

            polygon.append([a,b])
    '''

    def LeftChanged(self, text):
        w = 'Left ' + text
        self.Left_size_seter_label.setText(w)
        self.Left_size_seter_label.adjustSize()

        try:
            self.Left = float(text)
        except:
            pass

        self.Magic()

    def RightChanged(self, text):
        w = 'Right ' + text
        self.Right_size_seter_label.setText(w)
        self.Right_size_seter_label.adjustSize()

        try:
            self.Right = float(text)
        except:
            pass

        self.Magic()

    def UpChanged(self, text):
        w = 'Up ' + text
        self.Up_size_seter_label.setText(w)
        self.Up_size_seter_label.adjustSize()

        try:
            self.Up = float(text)
        except:
            pass

        self.Magic()

    def DownChanged(self, text):
        w = 'Down ' + text
        self.Down_size_seter_label.setText(w)
        self.Down_size_seter_label.adjustSize()

        try:
            self.Down = float(text)
        except:
            pass

        self.Magic()

    def Magic(self):

        self.WholeData = []

        self.x_scale = self.width_plot / self.width_load

        self.y_scale = self.height_plot / self.height_load

        # print(self.x_scale,' and ',self.x_scale)

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        self.axes.clear()

        if (self.Left != self.Right) and (self.Down != self.Up) and abs(self.Left) + abs(self.Right) + abs(
                self.Down) + abs(self.Up) != 0:
            self.extent = [self.Left, self.Right, self.Down, self.Up]
        elif (self.Left == self.Right and abs(self.Left) + abs(self.Right) != 0):
            reply = QMessageBox.warning(self, 'Warning', 'You set same value to Left and Right limits.')
            self.extent = 0

        elif (self.Down == self.Up and abs(self.Down) + abs(self.Up) != 0):
            reply = QMessageBox.warning(self, 'Warning', 'You set same value to Up and Down limits.')
            self.extent = 0
        else:
            self.extent = 0

        standardnamechosen = self.StandardsName[int(self.norm_slider.value())]
        standardchosen = self.Standards[standardnamechosen]

        self.norm_slider_label.setText(standardnamechosen)

        if self.flag != 0:
            if self.extent != 0:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto', extent=self.extent)
            else:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto')

        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])

        PointLabels = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0
            xuse, yuse = 0, 0

            x, y = raw.at[i, self.items[a]], raw.at[i, self.items[b]]

            try:
                xuse = x
                yuse = y

                self.xlabel = self.items[a]
                self.ylabel = self.items[b]

                if (self.Normalize_cb.isChecked()):

                    self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen

                    self.axes.set_xlabel(self.xlabel)
                    self.x_element_label.setText(self.xlabel)

                    self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen

                    self.axes.set_ylabel(self.ylabel)
                    self.y_element_label.setText(self.ylabel)

                    if self.items[a] in self.Element:
                        xuse = xuse / standardchosen[self.items[a]]

                    if self.items[b] in self.Element:
                        yuse = yuse / standardchosen[self.items[b]]

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)
                    self.xlabel = '$log10$ ' + self.xlabel

                    self.axes.set_xlabel(self.xlabel)

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.ylabel = '$log10$ ' + self.ylabel

                    self.axes.set_ylabel(self.ylabel)

                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel, edgecolors='black')
            except(ValueError):
                pass

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a,prop=fontprop)

        if self.polygon != 0 and self.polyline != 0 and self.line != 0:

            # print('gon: ',self.polygon,' \n line:',self.polyline)

            for i in self.polygon:
                self.DrawLine(i)

            for i in self.polyline:
                self.DrawLine(i)

            for i in self.line:
                self.DrawLine(i)



                # self.DrawLine(self.polygon)
                # self.DrawLine(self.polyline)

        self.canvas.draw()


class XYZ(AppForm):
    Lines = []
    Tags = []
    description = 'X-Y-Z diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    polygon = []
    polyline = []
    line = []
    flag = 0

    strgons = []
    strlines = []
    strpolylines = []

    width_plot = 100.0
    height_plot = 50 * math.sqrt(3)

    width_load = width_plot
    height_load = height_plot

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Triangular diagram')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

        self.polygon = 0
        self.polyline = 0

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')

        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Reset)

        self.load_button = QPushButton('&Load')
        self.load_button.clicked.connect(self.Load)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Magic)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Magic)  # int

        self.x_element_label = QLabel('X')

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(0)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Magic)  # int

        self.y_element_label = QLabel('Y')

        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, len(self.items) - 1)
        self.z_element.setValue(0)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.Magic)  # int

        self.z_element_label = QLabel('Z')

        #
        # Layout with box sizers
        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.load_button,
                  self.legend_cb, self.slider_label, self.slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        for w in [self.z_element_label, self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def Load(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         '选取文件',
                                                         '~/',
                                                         'PNG Files (*.png);;JPG Files (*.jpg);;SVG Files (*.svg)')  # 设置文件扩展名过滤,注意用双分号间隔

        print(fileName, '\t', filetype)

        if ('svg' in fileName):
            doc = minidom.parse(fileName)  # parseString also exists
            polygon_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polygon')]
            polyline_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polyline')]

            svg_width = [path.getAttribute('width') for path in doc.getElementsByTagName('svg')]
            svg_height = [path.getAttribute('height') for path in doc.getElementsByTagName('svg')]

            # print(svg_width)
            # print(svg_height)

            digit = '01234567890.-'
            width = svg_width[0].replace('px', '').replace('pt', '')
            height = svg_height[0].replace('px', '').replace('pt', '')

            '''
            width=''
            for letter in svg_width[0]:
                if letter in digit:
                    width = width + letter

            #print(width)



            height=''
            for letter in svg_height[0]:
                if letter in digit:
                    height = height + letter

            #print(height)
            '''

            self.width_load = float(width)
            self.height_load = float(height)

            self.x_scale = 100.0 / float(width)
            self.y_scale = 50.0 * math.sqrt(3) / float(height)

            # print('x_scale' , self.x_scale , ' y_scale' , self.y_scale)

            soup = BeautifulSoup(open(fileName), 'lxml')

            tmpgon = soup.find_all('polygon')
            tmpline = soup.find_all('polyline')
            tmptext = soup.find_all('text')

            strgons = []
            for i in tmpgon:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polygon.attrs
                strgons.append(k['points'].split())
            gons = []
            for i in strgons:
                m = self.Read(i)
                m.append(m[0])
                gons.append(m)

            strlines = []
            for i in tmpline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polyline.attrs
                strlines.append(k['points'].split())
            lines = []
            for i in strlines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                lines.append(m)

            self.polygon = gons
            self.polyline = lines

            # print(self.polygon,'\n',self.polyline)


        elif ('png' in fileName or 'jpg' in fileName):

            self.img = mpimg.imread(fileName)
            self.flag = 1

        self.Magic()

    def Reset(self):
        self.flag = 0
        self.Magic()

    def Magic(self):

        self.WholeData = []

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        c = int(self.z_element.value())

        self.axes.clear()
        self.axes.axis('off')

        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        x = [0, 100]
        y = [0, 50 * np.sqrt(3)]

        extent = [min(x), max(x), min(y), max(y)]

        if self.flag != 0:
            self.axes.imshow(self.img, interpolation='nearest', aspect='auto', extent=extent)

        # self.x_element_label.setText(self.items[a])
        # self.y_element_label.setText(self.items[b])
        # self.z_element_label.setText(self.items[c])

        self.axes.annotate(self.items[a], (2, 15))
        self.axes.annotate(self.items[b], (97, 15))
        self.axes.annotate(self.items[c], (40, 85))

        PointLabels = []
        TPoints = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y, z = 0, 0, 0
            xuse, yuse, zuse = 0, 0, 0

            x, y, z = raw.at[i, self.items[a]], raw.at[i, self.items[b]], raw.at[i, self.items[c]]

            # print(a,x,'\n',b,y,'\n',c,z,'\n')

            try:
                xuse = float(x)
                yuse = float(y)
                zuse = float(z)

                TPoints.append(TriPoint((xuse, yuse, zuse), Size=raw.at[i, 'Size'], Color=raw.at[i, 'Color'],
                                        Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel))


            except:
                pass

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        if self.polygon != 0 and self.polyline != 0:

            # print('gon: ',self.polygon,' \n line:',self.polyline)

            for i in self.polygon:
                self.DrawLine(i)

            for i in self.polyline:
                self.DrawLine(i)



                # self.DrawLine(self.polygon)
                # self.DrawLine(self.polyline)

        self.canvas.draw()


class Magic(AppForm):
    Lines = []
    Tags = []
    description = 'Magic diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Magic diagram')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

        self.polygon = 0
        self.polyline = 0

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Magic)

        self.load_button = QPushButton('&Load')
        self.load_button.clicked.connect(self.Load)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Magic)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Magic)  # int

        self.x_element_label = QLabel('X')

        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(0)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Magic)  # int

        self.y_element_label = QLabel('Y')

        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Magic)  # int

        #
        # Layout with box sizers
        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.load_button,
                  self.legend_cb, self.slider_label, self.slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def Load(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         '选取文件',
                                                         '~/',
                                                         'SVG Files (*.svg)')  # 设置文件扩展名过滤,注意用双分号间隔

        # #print(fileName)

        doc = minidom.parse(fileName)  # parseString also exists
        polygon_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polygon')]
        polyline_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polyline')]

        svg_width = [path.getAttribute('width') for path in doc.getElementsByTagName('svg')]
        svg_height = [path.getAttribute('height') for path in doc.getElementsByTagName('svg')]

        # print(svg_width)
        # print(svg_height)

        digit = '01234567890.-'
        width = svg_width[0].replace('px', '').replace('pt', '')
        height = svg_height[0].replace('px', '').replace('pt', '')

        '''
        width=''
        for letter in svg_width[0]:
            if letter in digit:
                width = width + letter

        #print(width)



        height=''
        for letter in svg_height[0]:
            if letter in digit:
                height = height + letter

        #print(height)
        '''

        self.width_load = float(width)
        self.height_load = float(height)

        self.x_scale = 100.0 / float(width)
        self.y_scale = 50.0 * math.sqrt(3) / float(height)

        # print('x_scale' , self.x_scale , ' y_scale' , self.y_scale)

        soup = BeautifulSoup(open(fileName), 'lxml')

        tmpgon = soup.find_all('polygon')
        tmpline = soup.find_all('polyline')
        tmptext = soup.find_all('text')

        strgons = []
        for i in tmpgon:
            a = (str(i)).replace('\n', '').replace('\t', '')
            m = BeautifulSoup(a, 'lxml')
            k = m.polygon.attrs
            strgons.append(k['points'].split())
        gons = []
        for i in strgons:
            m = self.Read(i)
            m.append(m[0])
            gons.append(m)

        strlines = []
        for i in tmpline:
            a = (str(i)).replace('\n', '').replace('\t', '')
            m = BeautifulSoup(a, 'lxml')
            k = m.polyline.attrs
            strlines.append(k['points'].split())
        lines = []
        for i in strlines:
            m = self.Read(i)
            # print('i: ',i,'\n m:',m)
            lines.append(m)

        self.polygon = gons
        self.polyline = lines

        # print(self.polygon,'\n',self.polyline)


        self.Magic()

    # text_location= [path.getAttribute('transform') for path in doc.getElementsByTagName('text')]
    '''
    tmppolygon_points=[]
    for i in polygon_points:
        tmppolygon_points.append(i.split())

    polygon=[]
    for i in tmppolygon_points:
        for l in range(len(i)):
            a=float((i[l].split(','))[0])
            b=float((i[l].split(','))[1])

            polygon.append([a,b])
    '''

    def Magic(self):

        self.WholeData = []

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        self.axes.clear()

        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])

        PointLabels = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0
            xuse, yuse = 0, 0

            x, y = raw.at[i, self.items[a]], raw.at[i, self.items[b]]

            try:
                xuse = x
                yuse = y

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)

                    self.axes.set_xlabel('$log10$ ' + self.items[a])

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.axes.set_ylabel('$log10$ ' + self.items[b])

                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel, edgecolors='black')
            except(ValueError):
                pass

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        if self.polygon != 0 and self.polyline != 0:

            # print('gon: ',self.polygon,' \n line:',self.polyline)

            for i in self.polygon:
                self.DrawLine(i)

            for i in self.polyline:
                self.DrawLine(i)



                # self.DrawLine(self.polygon)
                # self.DrawLine(self.polyline)

        self.canvas.draw()
