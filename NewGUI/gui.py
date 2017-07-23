#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'interface.ui'#
# Created by: PyQt5 UI code generator 5.8.1#
# WARNING! All changes made in this file will be lost!

"""
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-07-23
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd,pyqt5
    Any issues or improvements please contact cycleuser@cycleuser.org
    or leave a message to my blog: http://blog.cycleuser.org
"""


from CustomClass import PandasModel
from CustomClass import PlotModel
from CustomClass import CustomQTableView

import sys
import random
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import numpy as np
from numpy import arange, sin, pi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel,QMainWindow, QMenu, QHBoxLayout, QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)





class Ui_MainWindow(QtWidgets.QWidget):

    #raw=0
    raw = pd.DataFrame(index=[], columns=[])  # raw is initialized as a blank dataframe

    def setupUi(self, MainWindow,):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.model = PandasModel(self.raw)

        self.main_widget = QWidget(self)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.tableView = CustomQTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 384, 384))
        self.tableView.setObjectName("tableView")
        self.tableView.setSortingEnabled(True)


        self.MyCanvas=PlotModel(self.centralwidget, width=5, height=4, dpi=100)
        self.MyCanvas.setGeometry(QtCore.QRect(404, 10, 384, 384))
        self.MyCanvas.setObjectName("MyCanvas")
        #self.MyConvas.compute_initial_figure()

        self.pushButtonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpen.setGeometry(QtCore.QRect(30, 404, 110, 32))
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(30, 444, 110, 32))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonXYplot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonXYplot.setGeometry(QtCore.QRect(150, 404, 110, 32))
        self.pushButtonXYplot.setObjectName("pushButtonXYplot")
        self.pushButtonTriplot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonTriplot.setGeometry(QtCore.QRect(150, 444, 110, 32))
        self.pushButtonTriplot.setObjectName("pushButtonTriplot")
        self.pushButtonStereoplot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStereoplot.setGeometry(QtCore.QRect(410, 404, 110, 32))
        self.pushButtonStereoplot.setObjectName("pushButtonStereoplot")
        self.pushButtonCIPW = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCIPW.setGeometry(QtCore.QRect(280, 444, 110, 32))
        self.pushButtonCIPW.setObjectName("pushButtonCIPW")
        self.pushButtonAuto = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAuto.setGeometry(QtCore.QRect(410, 444, 110, 32))
        self.pushButtonAuto.setObjectName("pushButtonAuto")
        self.pushButtonCe = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCe.setGeometry(QtCore.QRect(280, 404, 110, 32))
        self.pushButtonCe.setObjectName("pushButtonCe")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuPlot = QtWidgets.QMenu(self.menubar)
        self.menuPlot.setObjectName("menuPlot")
        self.menuCalc = QtWidgets.QMenu(self.menubar)
        self.menuCalc.setObjectName("menuCalc")
        self.menuDIY = QtWidgets.QMenu(self.menubar)
        self.menuDIY.setObjectName("menuDIY")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionInstruction = QtWidgets.QAction(MainWindow)
        self.actionInstruction.setObjectName("actionInstruction")
        self.actionWebsite = QtWidgets.QAction(MainWindow)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionX_Y = QtWidgets.QAction(MainWindow)
        self.actionX_Y.setObjectName("actionX_Y")
        self.actionTriangular = QtWidgets.QAction(MainWindow)
        self.actionTriangular.setObjectName("actionTriangular")
        self.actionStereo = QtWidgets.QAction(MainWindow)
        self.actionStereo.setObjectName("actionStereo")
        self.actionCIPW = QtWidgets.QAction(MainWindow)
        self.actionCIPW.setObjectName("actionCIPW")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuHelp.addAction(self.actionInstruction)
        self.menuHelp.addAction(self.actionWebsite)
        self.menuPlot.addAction(self.actionX_Y)
        self.menuPlot.addAction(self.actionTriangular)
        self.menuPlot.addAction(self.actionStereo)
        self.menuCalc.addAction(self.actionCIPW)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menubar.addAction(self.menuCalc.menuAction())
        self.menubar.addAction(self.menuDIY.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.pushButtonOpen.clicked.connect(self.getDataFile)
        self.actionOpen.triggered.connect(self.getDataFile)



        self.pushButtonSave.clicked.connect(self.saveDataFile)
        self.actionSave.triggered.connect(self.saveDataFile)

        self.pushButtonXYplot.clicked.connect(self.TASplot)


    def getfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                              "选取文件",
                                                              "~/",
                                                              "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔

    def getDataFile(self):
        DataFileInput, filetype = QFileDialog.getOpenFileName(self,
                                                              "选取文件",
                                                              "~/",
                                                              "Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)")  # 设置文件扩展名过滤,注意用双分号间隔

        print(DataFileInput,filetype)



        if ("csv" in DataFileInput):
            self.raw = pd.read_csv(DataFileInput)
        elif ("xls" in DataFileInput):
            self.raw = pd.read_excel(DataFileInput)
        print(self.raw)

        self.model = PandasModel(self.raw)
        self.tableView.setModel(self.model)





    def saveDataFile(self):


        if self.model._changed == True:
            print("changed")
            print(self.model._df)



        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "Excel Files (*.xlsx);;CSV Files (*.csv)")  # 数据文件保存输出

        if(DataFileOutput !=''):

            if ("csv" in DataFileOutput):self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ("xls" in DataFileOutput):self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def saveImgFile(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

    def TASplot(self):

        self.MyCanvas.TAS(self.model._df)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoPython"))
        self.pushButtonOpen.setText(_translate("MainWindow", "Open"))
        self.pushButtonSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonXYplot.setText(_translate("MainWindow", "X-Y plot"))
        self.pushButtonTriplot.setText(_translate("MainWindow", "Triangular plot"))
        self.pushButtonStereoplot.setText(_translate("MainWindow", "Stereo plot"))
        self.pushButtonCIPW.setText(_translate("MainWindow", "CIPW"))
        self.pushButtonAuto.setText(_translate("MainWindow", "Auto"))
        self.pushButtonCe.setText(_translate("MainWindow", "Zircon Ce"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot"))
        self.menuCalc.setTitle(_translate("MainWindow", "Calc"))
        self.menuDIY.setTitle(_translate("MainWindow", "DIY"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionInstruction.setText(_translate("MainWindow", "Instruction"))
        self.actionWebsite.setText(_translate("MainWindow", "Website"))
        self.actionX_Y.setText(_translate("MainWindow", "X-Y"))
        self.actionTriangular.setText(_translate("MainWindow", "Triangular"))
        self.actionStereo.setText(_translate("MainWindow", "Stereo"))
        self.actionCIPW.setText(_translate("MainWindow", "CIPW"))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

