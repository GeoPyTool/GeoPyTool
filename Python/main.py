#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-03-13
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd

# usage:
    1) opern a ipython console
    2) import geopython as gp
    3) TasSample= gp.Tas("tas.xlsx")
    4) TasSample.read()

# Geology related classes available:
    1) Tas
    2) Ree
    3) Trace & Trace2 (with different sequence of trace elements)
    4) Qfl & Qmflt & Qapf
    5) Polar (projection of wulf net & schmidt net)

# know issues:
    1) Only work on Python 3.x

# Other
    Any issues or improvements please contact cycleuser@cycleuser.org
    or leave a message to my blog: http://blog.cycleuser.org
"""


import sys
from PyQt5.QtWidgets import QLabel,QMainWindow, QPushButton, QApplication,QWidget, QPushButton, QLineEdit,QInputDialog, QApplication
import geopython as gp


class Simple(QMainWindow):


    x = 'SiO2'

    y = [ 'Al2O3','MgO', 'FeO', 'CaO', 'Na2O', 'TiO2', 'K2O', 'P2O5']

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):



        Tas = QPushButton("Tas", self)
        Tas.move(30, 50)
        Tas.clicked.connect(self.Tas)

        Ree = QPushButton("Ree", self)
        Ree.move(150, 50)
        Ree.clicked.connect(self.Ree)

        Trace = QPushButton("Trace", self)
        Trace.move(30, 80)
        Trace.clicked.connect(self.Trace)

        Qfl = QPushButton("Qfl", self)
        Qfl.move(150, 80)
        Qfl.clicked.connect(self.Qfl)

        Qmflt = QPushButton("Qmflt", self)
        Qmflt.move(30, 110)
        Qmflt.clicked.connect(self.Qmflt)

        QapfP = QPushButton("QapfP", self)
        QapfP.move(150, 110)
        QapfP.clicked.connect(self.QapfP)

        QapfV = QPushButton("QapfV", self)
        QapfV.move(30, 140)
        QapfV.clicked.connect(self.QapfV)

        Polar = QPushButton("Polar", self)
        Polar.move(150, 140)
        Polar.clicked.connect(self.Polar)

        Pearce = QPushButton("Pearce", self)
        Pearce.move(30, 170)
        Pearce.clicked.connect(self.Pearce)

        Harker = QPushButton("Harker", self)
        Harker.move(150, 170)
        Harker.clicked.connect(self.Harker)



        self.lbl_X = QLabel(self)
        set_X = QLineEdit(self)

        set_X.move(30, 230)
        self.lbl_X.move(150, 230)

        set_X.textChanged[str].connect(self.XChanged)



        self.lbl_Y = QLabel(self)
        set_Y = QLineEdit(self)

        set_Y.move(30, 290)
        self.lbl_Y.move(150, 290)

        set_Y.textChanged[str].connect(self.YChanged)



        self.statusBar()
        self.setGeometry(600, 600, 300, 500)
        self.setWindowTitle('GeoPython-GUI-Reluctantly')
        self.show()


    def XChanged(self, text):
        self.x=''
        self.x = str(text)
        self.lbl_X.setText(text)
        self.lbl_X.adjustSize()

    def YChanged(self, text):
        self.y = []
        self.y = str(text).split()
        self.lbl_Y.setText(text)
        self.lbl_Y.adjustSize()



    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter Your X:')

        if ok:
            self.SetX.setText(str(text))

    def Tas(self):
        gp.Tas().read()

    def Ree(self):
        gp.Ree().read()

    def Trace(self):
        gp.Trace().read()
        gp.Trace2().read()

    def Qfl(self):
        gp.Qfl().read()

    def Qmflt(self):
        gp.Qmflt().read()

    def QapfP(self):
        gp.QapfP().read()

    def QapfV(self):
        gp.QapfV().read()

    def Polar(self):
        gp.Polar().read()

    def Pearce(self):
        gp.Pearce().read()

    def Harker(self):
        print(self.x,"\t",self.y)
        gp.Harker(x=self.x,y=self.y).read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Simple()
    sys.exit(app.exec_())