import sys
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


class AppForm(QMainWindow):

    _df= pd.DataFrame()
    _changed= False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    def __init__(self, parent=None,df = pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('GeoPython Image')

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

        slider_label = QLabel('Font Size:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(8, 24)
        self.slider.setValue(10)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb,self.detail_cb,self.tag_cb,self.more_cb,
                  slider_label, self.slider]:
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
            self.MyCanvas.print_figure(ImgFileOutput, dpi= 300 )

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
                 Top=19, Y0=1,Y1=19, Y_Gap=19, FontSize= 12 ,xlabel=r'$SiO_2 wt\%$', ylabel=r'$Na_2O + K_2O wt\%$',width=12, height=12, dpi=300,xlim=(30,90),ylim=(0,20)):

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
                self.axes.legend(loc=1,fontsize= 9)

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
