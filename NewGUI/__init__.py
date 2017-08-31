#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'interface.ui'#
# Created by: PyQt5 UI code generator 5.8.1#
# WARNING! All changes made in this file will be lost!

"""
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-08-31
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd,pyqt5
    Any issues or improvements please contact cycleuser@cycleuser.org
    or leave a message to my blog: http://blog.cycleuser.org
"""


from CustomClass import PandasModel
from CustomClass import CustomQTableView

from CustomClass import PlotModel
from CustomClass import AppForm

from CustomClass import CIPW
from CustomClass import TAS
from CustomClass import Trace
from CustomClass import REE
from CustomClass import Pearce
from CustomClass import Harker

from CustomClass import Stereo
from CustomClass import Rose

from CustomClass import QFL
from CustomClass import QmFLt
from CustomClass import QAPF

from CustomClass import MudStone

from CustomClass import Zircon

from CustomClass import MyPopup

import re
import math
import sys
import csv
import random
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

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

        self.w = MyPopup()
        self.w.setGeometry(QtCore.QRect(100, 100, 532, 600))

        self.zirconpop=Zircon()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)

        self.model = PandasModel(self.raw)

        self.main_widget = QWidget(self)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.tableView = CustomQTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 780, 384))
        self.tableView.setObjectName("tableView")
        self.tableView.setSortingEnabled(True)

        self.pushButtonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpen.setGeometry(QtCore.QRect(20, 404, 110, 32))
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(20, 444, 110, 32))
        self.pushButtonSave.setObjectName("pushButtonSave")







        self.pushButtonCIPW = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCIPW.setGeometry(QtCore.QRect(150, 404, 110, 32))
        self.pushButtonCIPW.setObjectName("pushButtonCIPW")

        self.pushButtonTAS = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonTAS.setGeometry(QtCore.QRect(150, 444, 110, 32))
        self.pushButtonTAS.setObjectName("pushButtonTAS")

        self.pushButtonTrace = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonTrace.setGeometry(QtCore.QRect(150, 484, 110, 32))
        self.pushButtonTrace.setObjectName("pushButtonTrace")

        self.pushButtonREE = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonREE.setGeometry(QtCore.QRect(150, 524, 110, 32))
        self.pushButtonREE.setObjectName("pushButtonREE")

        self.pushButtonPearce = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPearce.setGeometry(QtCore.QRect(150, 564, 110, 32))
        self.pushButtonPearce.setObjectName("pushButtonPearce")


        self.pushButtonHarker = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonHarker.setGeometry(QtCore.QRect(150, 604, 110, 32))
        self.pushButtonHarker.setObjectName("pushButtonHarker")



        self.pushButtonStereo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStereo.setGeometry(QtCore.QRect(280, 404, 110, 32))
        self.pushButtonStereo.setObjectName("pushButtonStereo")

        self.pushButtonRose = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRose.setGeometry(QtCore.QRect(280, 444, 110, 32))
        self.pushButtonRose.setObjectName("pushButtonRose")


        self.pushButtonQFL= QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQFL.setGeometry(QtCore.QRect(410, 404, 110, 32))
        self.pushButtonQFL.setObjectName("pushButtonQFL")


        self.pushButtonQmFLt= QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQmFLt.setGeometry(QtCore.QRect(410, 444, 110, 32))
        self.pushButtonQmFLt.setObjectName("pushButtonQmFLt")


        self.pushButtonQAPF= QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQAPF.setGeometry(QtCore.QRect(410, 484, 110, 32))
        self.pushButtonQAPF.setObjectName("pushButtonQAPF")



        self.pushButtonMudStone = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonMudStone.setGeometry(QtCore.QRect(540, 404, 110, 32))
        self.pushButtonMudStone.setObjectName("pushButtonMudStone")







        self.pushButtonZircon = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonZircon.setGeometry(QtCore.QRect(670, 404, 110, 32))
        self.pushButtonZircon.setObjectName("pushButtonZircon")






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



        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuHelp.addAction(self.actionInstruction)
        self.menuHelp.addAction(self.actionWebsite)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.pushButtonOpen.clicked.connect(self.getDataFile)
        self.actionOpen.triggered.connect(self.getDataFile)

        self.pushButtonSave.clicked.connect(self.saveDataFile)
        self.actionSave.triggered.connect(self.saveDataFile)

        self.pushButtonCIPW.clicked.connect(self.CIPW)
        self.pushButtonTAS.clicked.connect(self.TAS)
        self.pushButtonTrace.clicked.connect(self.Trace)
        self.pushButtonREE.clicked.connect(self.REE)
        self.pushButtonPearce.clicked.connect(self.Pearce)
        self.pushButtonHarker.clicked.connect(self.Harker)


        self.pushButtonStereo.clicked.connect(self.Stereo)
        self.pushButtonRose.clicked.connect(self.Rose)


        self.pushButtonQFL.clicked.connect(self.QFL)
        self.pushButtonQmFLt.clicked.connect(self.QmFLt)
        self.pushButtonQAPF.clicked.connect(self.QAPF)


        self.pushButtonMudStone.clicked.connect(self.Mud)

        self.pushButtonZircon.clicked.connect(self.Zircon)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoPython"))
        self.pushButtonOpen.setText(_translate("MainWindow", "Open"))
        self.pushButtonSave.setText(_translate("MainWindow", "Save"))

        self.pushButtonCIPW.setText(_translate("MainWindow", "CIPW"))
        self.pushButtonTAS.setText(_translate("MainWindow", "TAS"))
        self.pushButtonTrace.setText(_translate("MainWindow", "Trace"))
        self.pushButtonREE.setText(_translate("MainWindow", "REE"))
        self.pushButtonPearce.setText(_translate("MainWindow", "Pearce"))
        self.pushButtonHarker.setText(_translate("MainWindow", "Harker"))

        self.pushButtonQFL.setText(_translate("MainWindow", "QFL"))
        self.pushButtonQmFLt.setText(_translate("MainWindow", "QmFLt"))
        self.pushButtonQAPF.setText(_translate("MainWindow", "QAPF"))

        self.pushButtonStereo.setText(_translate("MainWindow", "Stereo"))
        self.pushButtonRose.setText(_translate("MainWindow", "Rose"))

        self.pushButtonMudStone.setText(_translate("MainWindow", "Sand-Silt-Mud"))

        self.pushButtonZircon.setText(_translate("MainWindow", "Zircon Ce"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionInstruction.setText(_translate("MainWindow", "Instruction"))
        self.actionWebsite.setText(_translate("MainWindow", "Website"))


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

        #print(DataFileInput,filetype)



        if ("csv" in DataFileInput):
            self.raw = pd.read_csv(DataFileInput)
        elif ("xls" in DataFileInput):
            self.raw = pd.read_excel(DataFileInput)
        #print(self.raw)

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
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                    "C:/",
                                    "pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.w.MyCanvas.print_figure(ImgFileOutput, dpi= 300 )
            #self.statusBar().showMessage('Saved to %s' % ImgFileOutput, 2000)

    def CIPW(self):
        self.cipwpop = CIPW(df=self.model._df)
        self.cipwpop.CIPW()
        self.cipwpop.show()
    def TAS(self):

        self.pop = TAS(df=self.model._df)
        self.pop.TAS()
        self.pop.show()
    def REE(self):
        self.reepop = REE(df=self.model._df)
        self.reepop.REE()
        self.reepop.show()
    def Trace(self):
        self.tracepop = Trace(df=self.model._df)
        self.tracepop.Trace()
        self.tracepop.show()
    def Pearce(self):
        self.pearcepop = Pearce(df=self.model._df)
        self.pearcepop.Pearce()
        self.pearcepop.show()
    def Harker(self):
        self.harkerpop = Harker(df=self.model._df)
        self.harkerpop.Harker()
        self.harkerpop.show()


    def Stereo(self):
        self.stereopop = Stereo(df=self.model._df)
        self.stereopop.Stereo()
        self.stereopop.show()
    def Rose(self):
        self.rosepop = Rose(df=self.model._df)
        self.rosepop.Rose()
        self.rosepop.show()

    def QFL(self):
        self.tripop = QFL(df=self.model._df)
        self.tripop.Tri()
        self.tripop.show()
    def QmFLt(self):
        self.tripop = QmFLt(df=self.model._df)
        self.tripop.Tri()
        self.tripop.show()
    def QAPF(self):
        self.qapfpop = QAPF(df=self.model._df)
        self.qapfpop.QAPF()
        self.qapfpop.show()

    def Mud(self):
        self.mudpop = MudStone(df=self.model._df)
        self.mudpop.Tri()
        self.mudpop.show()
    def Zircon(self):
        print("Opening a new popup window...")
        #self.w = MyPopup(xlabel = r'$SiO_2 wt\%$', ylabel = r'$Na_2O + K_2O wt\%$', xlim = (30,90), ylim = (0, 20))
        #self.w.setGeometry(QtCore.QRect(100, 100, 532, 600))

        self.zirconpop = Zircon(df=self.model._df)
        self.zirconpop.MultiBallard()
        self.zirconpop.show()







    def Tri(self):
        pass


    def Auto(self):
        pass




def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

def begin():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())