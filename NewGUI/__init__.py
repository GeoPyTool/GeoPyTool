#!/usr/bin/python3
# coding:utf-8
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'interface.ui'#
# Created by: PyQt5 UI code generator 5.8.1#
# WARNING! All changes made in this file will be lost!

import os

LocationOfMySelf=os.path.dirname(__file__)

print(LocationOfMySelf)

import CustomClass

version = CustomClass.version

date = CustomClass.date

sign = """
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-10-15
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd,pyqt5,BeautifulSoup4
    Any issues or improvements please contact cycleuser@cycleuser.org
    or Open An Issue at GitHub:https://github.com/chinageology/GeoPython/issues     
    Website For Chinese Users：https://zhuanlan.zhihu.com/p/28908475
"""

t = 'You are using GeoPython ' + version + ', released on' + date + '\n' + sign

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
from CustomClass import ZirconTiTemp
from CustomClass import RutileZrTemp

from CustomClass import Cluster

from CustomClass import Magic

from CustomClass import XY
from CustomClass import XYZ

import webbrowser

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
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5.QtWidgets import (QWidget, QMessageBox, qApp, QShortcut, QLabel, QMainWindow, QMenu, QHBoxLayout,
                             QVBoxLayout,
                             QApplication, QPushButton, QSlider,
                             QFileDialog, QAction)


_translate = QtCore.QCoreApplication.translate


class Ui_MainWindow(QtWidgets.QMainWindow):
    # raw=0
    raw = pd.DataFrame(index=[], columns=[])  # raw is initialized as a blank dataframe

    lang = True

    app = QtWidgets.QApplication(sys.argv)
    trans = QtCore.QTranslator()

    talk=''

    def __init__(self):


        super(Ui_MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(1000, 500)


        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", u"GeoPython"))
        self.talk=  _translate("MainWindow",'You are using GeoPython ') + version +'\n'+  _translate("MainWindow",'released on ') + date

        self.model = PandasModel(self.raw)

        self.main_widget = QWidget(self)

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.tableView = CustomQTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 980, 384))
        self.tableView.setObjectName("tableView")
        self.tableView.setSortingEnabled(True)

        self.pushButtonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpen.setGeometry(QtCore.QRect(20, 404, 110, 32))
        self.pushButtonOpen.setObjectName("pushButtonOpen")

        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(150, 404, 110, 32))
        self.pushButtonSave.setObjectName("pushButtonSave")

        self.pushButtonSort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSort.setGeometry(QtCore.QRect(280, 404, 110, 32))
        self.pushButtonSort.setObjectName("pushButtonSort")

        self.pushButtonQuit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQuit.setGeometry(QtCore.QRect(410, 404, 110, 32))
        self.pushButtonQuit.setObjectName("pushButtonQuit")

        self.pushButtonLang = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLang.setGeometry(QtCore.QRect(540, 404, 110, 32))
        self.pushButtonLang.setObjectName("pushButtonLang")

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuGeoChem = QtWidgets.QMenu(self.menubar)
        self.menuGeoChem.setObjectName("menuGeoChem")

        self.menuStructure = QtWidgets.QMenu(self.menubar)
        self.menuStructure.setObjectName("menuStructure")

        self.menuCalc = QtWidgets.QMenu(self.menubar)
        self.menuCalc.setObjectName("menuCalc")

        self.menuStat = QtWidgets.QMenu(self.menubar)
        self.menuStat.setObjectName("menuStat")

        self.menuMore = QtWidgets.QMenu(self.menubar)
        self.menuMore.setObjectName("menuMore")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(QIcon(LocationOfMySelf+'/open.png'), 'Open',self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut('Ctrl+O')

        self.actionSave = QtWidgets.QAction(QIcon(LocationOfMySelf+'/save.png'), 'Save',self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut('Ctrl+S')

        self.actionCnWeb = QtWidgets.QAction(QIcon(LocationOfMySelf+'/cn.png'), 'Chinese Forum',self)
        self.actionCnWeb.setObjectName("actionCnWeb")

        self.actionEnWeb = QtWidgets.QAction(QIcon(LocationOfMySelf+'/en.png'), 'English Forum',self)
        self.actionEnWeb.setObjectName("actionEnWeb")


        self.actionGoGithub = QtWidgets.QAction(QIcon(LocationOfMySelf+'/github.png'), 'GitHub',self)
        self.actionGoGithub.setObjectName("actionGoGithub")

        self.actionVersionCheck = QtWidgets.QAction(QIcon(LocationOfMySelf+'/version.png'), 'Version',self)
        self.actionVersionCheck.setObjectName("actionVersionCheck")

        self.actionTAS = QtWidgets.QAction(self)
        self.actionTAS.setObjectName("actionTAS")

        self.actionTrace = QtWidgets.QAction(self)
        self.actionTrace.setObjectName("actionTrace")

        self.actionRee = QtWidgets.QAction(self)
        self.actionRee.setObjectName("actionRee")

        self.actionPearce = QtWidgets.QAction(self)
        self.actionPearce.setObjectName("actionPearce")

        self.actionHarker = QtWidgets.QAction(self)
        self.actionHarker.setObjectName("actionHarker")

        self.actionStereo = QtWidgets.QAction(self)
        self.actionStereo.setObjectName("actionStereo")

        self.actionRose = QtWidgets.QAction(self)
        self.actionRose.setObjectName("actionRose")

        self.actionQFL = QtWidgets.QAction(self)
        self.actionQFL.setObjectName("actionQFL")

        self.actionQmFLt = QtWidgets.QAction(self)
        self.actionQmFLt.setObjectName("actionQmFLt")

        self.actionCIPW = QtWidgets.QAction(self)
        self.actionCIPW.setObjectName("actionCIPW")

        self.actionZirconCe = QtWidgets.QAction(self)
        self.actionZirconCe.setObjectName("actionZirconCe")

        self.actionZirconTiTemp = QtWidgets.QAction(self)
        self.actionZirconTiTemp.setObjectName("actionZirconTiTemp")

        self.actionRutileZrTemp = QtWidgets.QAction(self)
        self.actionRutileZrTemp.setObjectName("actionRutileZrTemp")

        self.actionCluster = QtWidgets.QAction(self)
        self.actionCluster.setObjectName("actionCluster")

        self.actionQAPF = QtWidgets.QAction(self)
        self.actionQAPF.setObjectName("actionQAPF")

        self.actionMudStone = QtWidgets.QAction(self)
        self.actionMudStone.setObjectName("actionMudStone")

        self.actionXY = QtWidgets.QAction(self)
        self.actionXY.setObjectName("actionXY")

        self.actionXYZ = QtWidgets.QAction(self)
        self.actionXYZ.setObjectName("actionXYZ")

        self.actionMagic = QtWidgets.QAction(self)
        self.actionMagic.setObjectName("actionMagic")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)

        self.menuGeoChem.addAction(self.actionTAS)
        self.menuGeoChem.addAction(self.actionTrace)
        self.menuGeoChem.addAction(self.actionRee)
        self.menuGeoChem.addAction(self.actionPearce)
        self.menuGeoChem.addAction(self.actionHarker)

        self.menuStructure.addAction(self.actionStereo)
        self.menuStructure.addAction(self.actionRose)
        self.menuStructure.addAction(self.actionQFL)
        self.menuStructure.addAction(self.actionQmFLt)

        self.menuCalc.addAction(self.actionCIPW)
        self.menuCalc.addAction(self.actionZirconCe)
        self.menuCalc.addAction(self.actionZirconTiTemp)
        self.menuCalc.addAction(self.actionRutileZrTemp)

        self.menuStat.addAction(self.actionCluster)

        self.menuMore.addAction(self.actionMudStone)
        self.menuMore.addAction(self.actionQAPF)

        self.menuMore.addAction(self.actionXY)
        self.menuMore.addAction(self.actionXYZ)
        self.menuMore.addAction(self.actionMagic)

        self.menuHelp.addAction(self.actionCnWeb)
        self.menuHelp.addAction(self.actionEnWeb)


        self.menuHelp.addAction(self.actionGoGithub)
        self.menuHelp.addAction(self.actionVersionCheck)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuGeoChem.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuStructure.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuCalc.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuStat.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuMore.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addSeparator()

        self.actionTAS.triggered.connect(self.TAS)
        self.actionTrace.triggered.connect(self.Trace)
        self.actionRee.triggered.connect(self.REE)
        self.actionPearce.triggered.connect(self.Pearce)
        self.actionHarker.triggered.connect(self.Harker)
        self.actionQAPF.triggered.connect(self.QAPF)

        self.actionStereo.triggered.connect(self.Stereo)
        self.actionRose.triggered.connect(self.Rose)
        self.actionQFL.triggered.connect(self.QFL)
        self.actionQmFLt.triggered.connect(self.QmFLt)

        self.actionCIPW.triggered.connect(self.CIPW)
        self.actionZirconCe.triggered.connect(self.Zircon)
        self.actionZirconTiTemp.triggered.connect(self.ZirconTiTemp)
        self.actionRutileZrTemp.triggered.connect(self.RutileZrTemp)
        self.actionCluster.triggered.connect(self.Cluster)

        self.actionOpen.triggered.connect(self.getDataFile)
        self.actionSave.triggered.connect(self.saveDataFile)

        self.actionCnWeb.triggered.connect(self.goCnBBS)
        self.actionEnWeb.triggered.connect(self.goEnBBS)
        self.actionGoGithub.triggered.connect(self.goGitHub)
        self.actionVersionCheck.triggered.connect(self.checkVersion)

        self.actionXY.triggered.connect(self.XY)
        self.actionXYZ.triggered.connect(self.XYZ)
        self.actionMagic.triggered.connect(self.Magic)
        self.actionMudStone.triggered.connect(self.Mud)

        self.pushButtonOpen.clicked.connect(self.getDataFile)
        self.pushButtonSave.clicked.connect(self.saveDataFile)
        self.pushButtonSort.clicked.connect(self.SetUpDataFile)
        self.pushButtonQuit.clicked.connect(qApp.quit)
        self.pushButtonLang.clicked.connect(self.switch)

        self.actionQuit = QtWidgets.QAction('Quit', self)
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(qApp.quit)


        self.pushButtonOpen.setText(_translate("MainWindow",u"Open"))



        self.pushButtonSave.setText(_translate("MainWindow",u"Save"))
        self.pushButtonSort.setText(_translate("MainWindow",u"Set"))
        self.pushButtonQuit.setText(_translate("MainWindow",u"Quit"))
        self.pushButtonLang.setText(_translate("MainWindow",u"English"))

        self.pushButtonOpen.setIcon(QtGui.QIcon(LocationOfMySelf+'/open.png'))
        self.pushButtonSave.setIcon(QtGui.QIcon(LocationOfMySelf+'/save.png'))
        self.pushButtonSort.setIcon(QtGui.QIcon(LocationOfMySelf+'/set.png'))
        self.pushButtonQuit.setIcon(QtGui.QIcon(LocationOfMySelf+'/quit.png'))

        self.menuFile.setTitle(_translate("MainWindow",u"Data File"))

        self.menuGeoChem.setTitle(_translate("MainWindow",u"Geochemistry"))

        self.menuStructure.setTitle(_translate("MainWindow",u"Structure"))

        self.menuCalc.setTitle(_translate("MainWindow",u"Calculation"))

        self.menuStat.setTitle(_translate("MainWindow",u"Statistics"))

        self.menuMore.setTitle(_translate("MainWindow",u"Others"))

        self.menuHelp.setTitle(_translate("MainWindow",u"Help"))

        self.actionOpen.setText(_translate("MainWindow",u"Open Data"))
        self.actionSave.setText(_translate("MainWindow",u"Save Data"))

        self.actionTAS.setText(_translate("MainWindow",u"TAS"))
        self.actionTrace.setText(_translate("MainWindow",u"Trace"))
        self.actionRee.setText(_translate("MainWindow",u"REE"))
        self.actionPearce.setText(_translate("MainWindow",u"Pearce"))
        self.actionHarker.setText(_translate("MainWindow",u"Harker"))

        self.actionQAPF.setText(_translate("MainWindow",u"QAPF"))

        self.actionStereo.setText(_translate("MainWindow",u"Stereo"))
        self.actionRose.setText(_translate("MainWindow",u"Rose"))
        self.actionQFL.setText(_translate("MainWindow",u"QFL"))
        self.actionQmFLt.setText(_translate("MainWindow",u"QmFLt"))

        self.actionCIPW.setText(_translate("MainWindow",u"CIPW"))

        self.actionZirconCe.setText(_translate("MainWindow",u"ZirconCe"))
        self.actionZirconTiTemp.setText(_translate("MainWindow",u"ZirconTiTemp"))
        self.actionRutileZrTemp.setText(_translate("MainWindow",u"RutileZrTemp"))
        self.actionCluster.setText(_translate("MainWindow",u"Cluster"))

        self.actionXY.setText(_translate("MainWindow",u"X-Y plot"))
        self.actionXYZ.setText(_translate("MainWindow",u"X-Y-Z plot"))

        self.actionMagic.setText(_translate("MainWindow",u"Magic"))

        self.actionMudStone.setText(_translate("MainWindow",u"Sand-Silt-Mud"))

        self.actionVersionCheck.setText(_translate("MainWindow",u"About"))
        self.actionCnWeb.setText(_translate("MainWindow",u"Chinese Forum"))
        self.actionEnWeb.setText(_translate("MainWindow",u"English Forum"))
        self.actionGoGithub.setText(_translate("MainWindow",u"Github"))


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.talk=  _translate("MainWindow",'You are using GeoPython ') + version +'\n'+ _translate("MainWindow",'released on ') + date + '\n'+ _translate("MainWindow",'Visit the latest download link and check for update?')

        self.pushButtonOpen.setText(_translate("MainWindow", u"Open"))
        self.pushButtonSave.setText(_translate("MainWindow", u"Save"))
        self.pushButtonSort.setText(_translate("MainWindow", u"Set"))
        self.pushButtonQuit.setText(_translate("MainWindow", u"Quit"))
        self.pushButtonLang.setText(_translate("MainWindow", u"English"))

        self.pushButtonOpen.setIcon(QtGui.QIcon(LocationOfMySelf+'/open.png'))
        self.pushButtonSave.setIcon(QtGui.QIcon(LocationOfMySelf+'/save.png'))
        self.pushButtonSort.setIcon(QtGui.QIcon(LocationOfMySelf+'/set.png'))
        self.pushButtonQuit.setIcon(QtGui.QIcon(LocationOfMySelf+'/quit.png'))

        self.menuFile.setTitle(_translate("MainWindow", u"Data File"))

        self.menuGeoChem.setTitle(_translate("MainWindow", u"Geochemistry"))

        self.menuStructure.setTitle(_translate("MainWindow", u"Structure"))

        self.menuCalc.setTitle(_translate("MainWindow", u"Calculation"))

        self.menuStat.setTitle(_translate("MainWindow", u"Statistics"))

        self.menuMore.setTitle(_translate("MainWindow", u"Others"))

        self.menuHelp.setTitle(_translate("MainWindow", u"Help"))

        self.actionOpen.setText(_translate("MainWindow", u"Open Data"))
        self.actionSave.setText(_translate("MainWindow", u"Save Data"))

        self.actionTAS.setText(_translate("MainWindow", u"TAS"))
        self.actionTrace.setText(_translate("MainWindow", u"Trace"))
        self.actionRee.setText(_translate("MainWindow", u"REE"))
        self.actionPearce.setText(_translate("MainWindow", u"Pearce"))
        self.actionHarker.setText(_translate("MainWindow", u"Harker"))

        self.actionQAPF.setText(_translate("MainWindow", u"QAPF"))

        self.actionStereo.setText(_translate("MainWindow", u"Stereo"))
        self.actionRose.setText(_translate("MainWindow", u"Rose"))
        self.actionQFL.setText(_translate("MainWindow", u"QFL"))
        self.actionQmFLt.setText(_translate("MainWindow", u"QmFLt"))

        self.actionCIPW.setText(_translate("MainWindow", u"CIPW"))

        self.actionZirconCe.setText(_translate("MainWindow", u"ZirconCe"))
        self.actionZirconTiTemp.setText(_translate("MainWindow", u"ZirconTiTemp"))
        self.actionRutileZrTemp.setText(_translate("MainWindow", u"RutileZrTemp"))
        self.actionCluster.setText(_translate("MainWindow", u"Cluster"))

        self.actionXY.setText(_translate("MainWindow", u"X-Y plot"))
        self.actionXYZ.setText(_translate("MainWindow", u"X-Y-Z plot"))

        self.actionMagic.setText(_translate("MainWindow", u"Magic"))

        self.actionMudStone.setText(_translate("MainWindow", u"Sand-Silt-Mud"))

        self.actionVersionCheck.setText(_translate("MainWindow", u"About"))
        self.actionCnWeb.setText(_translate("MainWindow", u"Chinese Forum"))
        self.actionEnWeb.setText(_translate("MainWindow", u"English Forum"))
        self.actionGoGithub.setText(_translate("MainWindow", u"Github"))

    def getfile(self):
        _translate = QtCore.QCoreApplication.translate
        fileName, filetype = QFileDialog.getOpenFileName(self,_translate("MainWindow", u"Choose Data File"),
                                                         "~/",
                                                         "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔

    def goGitHub(self):
        webbrowser.open('https://github.com/chinageology/GeoPython/blob/master/README.md')

    def goCnBBS(self):
        webbrowser.open('http://bbs.geopython.com/-f2.html')

    def goEnBBS(self):
        webbrowser.open('http://bbs.geopython.com/English-Forum-f3.html')


    def checkVersion(self):

        #reply = QMessageBox.information(self, 'Version', self.talk)

        buttonReply = QMessageBox.question(self, 'Version', self.talk, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            webbrowser.open('https://github.com/chinageology/GeoPython/blob/master/Download.md')
        else:
            print('No clicked.')


    def Update(self):
        webbrowser.open('https://github.com/chinageology/GeoPython/blob/master/Download.md')

    def to_English(self):

        self.trans.load(LocationOfMySelf+"/en")
        self.app.installTranslator(self.trans)
        self.retranslateUi()

    def to_Chinese(self):

        self.trans.load(LocationOfMySelf+"/cn")
        self.app.installTranslator(self.trans)
        self.retranslateUi()

    def switch(self):
        self.lang = not (self.lang)
        if self.lang:
            self.to_English()


        else:
            self.to_Chinese()


    def ErrorEvent(self):

        reply = QMessageBox.information(self, 'Warning', "Your Data mismatch this Plot.")



    def SetUpDataFile(self):

        flag = 0
        ItemsAvalibale = self.model._df.columns.values.tolist()

        ItemsToTest = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']

        LabelList = []
        MarkerList = []
        ColorList = []
        SizeList = []
        AlphaList = []
        StyleList = []
        WidthList = []

        for i in range(len(self.model._df)):
            LabelList.append('Group1')
            MarkerList.append('o')
            ColorList.append('red')
            SizeList.append(10)
            AlphaList.append(0.6)
            StyleList.append('-')
            WidthList.append(1)

        data = {'Label': LabelList,
                'Marker': MarkerList,
                'Color': ColorList,
                'Size': SizeList,
                'Alpha': AlphaList,
                'Style': StyleList,
                'Width': WidthList}

        for i in ItemsToTest:
            if i not in ItemsAvalibale:
                # print(i)
                flag = flag + 1
                tmpdftoadd = pd.DataFrame({i: data[i]})

                self.model._df = pd.concat([tmpdftoadd, self.model._df], axis=1)

        self.model = PandasModel(self.model._df)

        self.tableView.setModel(self.model)

        if flag == 0:
            reply = QMessageBox.information(self, 'Ready',
                                        "Everything fine and no need to set up.")

        else:
            reply = QMessageBox.information(self, 'Ready',
                                        "Items added, Modify in the Table to set up details.")


    def getDataFile(self):
        _translate = QtCore.QCoreApplication.translate
        DataFileInput, filetype = QFileDialog.getOpenFileName(self,_translate("MainWindow", u"Choose Data File"),
                                                              "~/",
                                                              "Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)")  # 设置文件扩展名过滤,注意用双分号间隔

        # #print(DataFileInput,filetype)

        if ("csv" in DataFileInput):
            self.raw = pd.read_csv(DataFileInput)
        elif ("xls" in DataFileInput):
            self.raw = pd.read_excel(DataFileInput)
        # #print(self.raw)

        self.model = PandasModel(self.raw)
        self.tableView.setModel(self.model)

    def saveDataFile(self):

        # if self.model._changed == True:
        # print("changed")
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,_translate("MainWindow", u"Save Data File"),
                                                          "C:/",
                                                          "Excel Files (*.xlsx);;CSV Files (*.csv)")  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ("csv" in DataFileOutput):
                self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ("xls" in DataFileOutput):
                self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def CIPW(self):
        self.cipwpop = CIPW(df=self.model._df)
        try:
            self.cipwpop.CIPW()
            self.cipwpop.show()
        except(KeyError):
            self.ErrorEvent()

    def ZirconTiTemp(self):
        self.ztpop = ZirconTiTemp(df=self.model._df)
        try:
            self.ztpop.ZirconTiTemp()
            self.ztpop.show()
        except(KeyError):
            self.ErrorEvent()

    def RutileZrTemp(self):
        self.rzpop = RutileZrTemp(df=self.model._df)
        try:
            self.rzpop.RutileZrTemp()
            self.rzpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Cluster(self):

        self.clusterpop = Cluster(df=self.model._df)
        self.clusterpop.Cluster()
        self.clusterpop.show()

        try:
            self.clusterpop.Cluster()
            self.clusterpop.show()
        except(KeyError):
            pass
            # self.ErrorEvent()

    def TAS(self):

        self.pop = TAS(df=self.model._df)
        try:
            self.pop.TAS()
            self.pop.show()
        except(KeyError):
            self.ErrorEvent()

    def REE(self):
        self.reepop = REE(df=self.model._df)
        try:
            self.reepop.REE()
            self.reepop.show()
        except(KeyError):
            self.ErrorEvent()

    def Trace(self):
        self.tracepop = Trace(df=self.model._df)
        try:
            self.tracepop.Trace()
            self.tracepop.show()
        except(KeyError):
            self.ErrorEvent()

    def Pearce(self):
        self.pearcepop = Pearce(df=self.model._df)
        try:
            self.pearcepop.Pearce()
            self.pearcepop.show()
        except(KeyError):
            self.ErrorEvent()

    def Harker(self):
        self.harkerpop = Harker(df=self.model._df)
        try:
            self.harkerpop.Harker()
            self.harkerpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Stereo(self):
        self.stereopop = Stereo(df=self.model._df)
        try:
            self.stereopop.Stereo()
            self.stereopop.show()
        except(KeyError):
            self.ErrorEvent()

    def Rose(self):
        self.rosepop = Rose(df=self.model._df)
        try:
            self.rosepop.Rose()
            self.rosepop.show()
        except(KeyError):
            self.ErrorEvent()

    def QFL(self):
        self.tripop = QFL(df=self.model._df)
        try:
            self.tripop.Tri()
            self.tripop.show()
        except(KeyError):
            self.ErrorEvent()

    def QmFLt(self):
        self.tripop = QmFLt(df=self.model._df)
        try:
            self.tripop.Tri()
            self.tripop.show()
        except(KeyError):
            self.ErrorEvent()

    def QAPF(self):
        self.qapfpop = QAPF(df=self.model._df)
        try:
            self.qapfpop.QAPF()
            self.qapfpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Mud(self):
        self.mudpop = MudStone(df=self.model._df)
        try:
            self.mudpop.Tri()
            self.mudpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Zircon(self):
        # print("Opening a new popup window...")
        self.zirconpop = Zircon(df=self.model._df)
        try:
            self.zirconpop.MultiBallard()
            self.zirconpop.show()
        except(KeyError):
            self.ErrorEvent()

    def XY(self):
        self.xypop = XY(df=self.model._df)
        try:
            self.xypop.Magic()
            self.xypop.show()
        except(KeyError):
            self.ErrorEvent()

    def XYZ(self):
        self.xyzpop = XYZ(df=self.model._df)
        try:
            self.xyzpop.Magic()
            self.xyzpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Magic(self):
        self.magicpop = Magic(df=self.model._df)
        try:
            self.magicpop.Magic()
            self.magicpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Tri(self):
        pass

    def Auto(self):
        pass


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    trans = QtCore.QTranslator()
    # trans.load("cn")  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = Ui_MainWindow()
    mainWin.retranslateUi()
    mainWin.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

'''




if __name__ == '__main__':
    print(sign)



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    trans = QtCore.QTranslator()
    # trans.load("cn")  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = Ui_MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
'''