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
    5) Wulf (projection of wulf net & schmidt net and Rose map)

# know issues:
    1) Only work on Python 3.x

# Other
    Any issues or improvements please contact cycleuser@cycleuser.org
    or leave a message to my blog: http://blog.cycleuser.org
"""


import sys
from PyQt5.QtWidgets import QLabel,QMainWindow, QPushButton, QApplication,QWidget, QPushButton, QLineEdit,QInputDialog, QApplication
import geopython as gp
import os


class Simple(QMainWindow):


    x = 'SiO2'

    y = [ 'Al2O3','MgO', 'FeO', 'CaO', 'Na2O', 'TiO2', 'K2O', 'P2O5']

    SR = 'Strike'

    MR = 'Strike'

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):



        Tas = QPushButton("Tas-1986", self)
        Tas.move(80, 30)
        Tas.clicked.connect(self.Tas)


        TasW = QPushButton("Tas Wilson", self)
        TasW.move(250, 30)
        TasW.clicked.connect(self.TasW)

        TasV = QPushButton("Tas Volcano", self)
        TasV.move(420, 30)
        TasV.clicked.connect(self.TasV)

        TasI = QPushButton("Tas Intrusion", self)
        TasI.move(590, 30)
        TasI.clicked.connect(self.TasI)





        Ree = QPushButton("Ree", self)
        Ree.move(80, 80)
        Ree.clicked.connect(self.Ree)



        Trace1 = QPushButton("Trace Cs->", self)
        Trace1.move(250, 80)
        Trace1.clicked.connect(self.Trace1)


        Trace2 = QPushButton("Trace Rb->", self)
        Trace2.move(420, 80)
        Trace2.clicked.connect(self.Trace2)



        CIPW= QPushButton("CIPW", self)
        CIPW.move(590, 80)
        CIPW.clicked.connect(self.CIPW)


        Ballard = QPushButton("Ballard", self)
        Ballard.move(590, 130)
        Ballard.clicked.connect(self.Ballard)


        MultiBallard = QPushButton("MultiBallard", self)
        MultiBallard.move(590, 180)
        MultiBallard.clicked.connect(self.MultiBallard)


        Qfl = QPushButton("Qfl", self)
        Qfl.move(250, 130)
        Qfl.clicked.connect(self.Qfl)

        Qmflt = QPushButton("Qmflt", self)
        Qmflt.move(80, 130)
        Qmflt.clicked.connect(self.Qmflt)

        QapfP = QPushButton("QapfP", self)
        QapfP.move(250, 180)
        QapfP.clicked.connect(self.QapfP)

        QapfV = QPushButton("QapfV", self)
        QapfV.move(80, 180)
        QapfV.clicked.connect(self.QapfV)



        Pearce = QPushButton("Pearce", self)
        Pearce.move(80, 360)
        Pearce.clicked.connect(self.Pearce)


        Harker = QPushButton("Harker", self)
        Harker.move(250, 360)
        Harker.clicked.connect(self.Harker)






        SingleRose= QPushButton("SingleRose", self)
        SingleRose.move(420, 360)
        SingleRose.clicked.connect(self.SingleRose)


        MultiRose= QPushButton("MultiRose", self)
        MultiRose.move(590, 360)
        MultiRose.clicked.connect(self.MultiRose)

        Wulf = QPushButton("Wulff", self)
        Wulf.move(420, 410)
        Wulf.clicked.connect(self.Wulf)


        Schmidt= QPushButton("Schmidt", self)
        Schmidt.move(590, 410)
        Schmidt.clicked.connect(self.Schmidt)






        self.lbl_hintX = QLabel(self)
        self.lbl_hintX.move(80, 250)
        self.lbl_hintX.setText("Input X for Harker:")
        self.lbl_hintX.adjustSize()


        self.lbl_hintY = QLabel(self)
        self.lbl_hintY.move(250, 250)
        self.lbl_hintY.setText("Input Y for Harker:")
        self.lbl_hintY.adjustSize()


        set_X = QLineEdit(self)
        set_X.move(80, 280)

        set_X.textChanged[str].connect(self.XChanged)

        set_Y = QLineEdit(self)
        set_Y.move(250, 280)

        set_Y.textChanged[str].connect(self.YChanged)



        self.lbl_X = QLabel(self)
        self.lbl_X.move(80, 330)
        self.lbl_Y = QLabel(self)
        self.lbl_Y.move(250, 330)


        self.lbl_SR = QLabel(self)
        self.lbl_SR.move(420, 330)
        self.lbl_MR = QLabel(self)
        self.lbl_MR.move(590, 330)


        self.lbl_hintSR = QLabel(self)
        self.lbl_hintSR.move(420, 250)
        self.lbl_hintSR.setText("Items for SingleRose:")
        self.lbl_hintSR.adjustSize()

        self.lbl_hintMR = QLabel(self)
        self.lbl_hintMR.move(590, 250)
        self.lbl_hintMR.setText("Item for MultiRose:")
        self.lbl_hintMR.adjustSize()

        set_SR = QLineEdit(self)
        set_SR.move(420, 280)

        set_SR.textChanged[str].connect(self.SRChanged)

        set_MR = QLineEdit(self)
        set_MR.move(590, 280)

        set_MR.textChanged[str].connect(self.MRChanged)

        self.lbl_SR = QLabel(self)
        self.lbl_SR.move(420, 330)
        self.lbl_MR = QLabel(self)
        self.lbl_MR.move(590, 330)

        self.statusBar()
        self.setGeometry(900, 600, 750, 500)
        self.setWindowTitle('GeoPython-GUI-Reluctantly')
        self.show()


    def XChanged(self, text):
        self.x=''
        self.x = str(text)
        self.lbl_X.setText("X:"+text)
        self.lbl_X.adjustSize()

    def YChanged(self, text):
        self.y = []
        self.y = str(text).split()
        self.lbl_Y.setText("Y:"+text)
        self.lbl_Y.adjustSize()



    def SRChanged(self, text):
        self.SR=''
        self.SR = str(text)
        self.lbl_SR.setText("SR:"+text)
        self.lbl_SR.adjustSize()

    def MRChanged(self, text):
        self.MR = []
        self.MR = str(text).split()
        self.lbl_MR.setText("MR:"+text)
        self.lbl_MR.adjustSize()


    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter Your X:')

        if ok:
            self.SetX.setText(str(text))

    def Tas(self):
        a=0
        a=gp.Tas_Old()
        a.read()
        a = 0

    def TasW(self):
        a=0
        a=gp.Tas()
        a.read()
        a = 0

    def TasV(self):
        a=0
        a=gp.TasV()
        a.read()
        a = 0

    def TasI(self):
        a = 0
        a=gp.TasI()
        a.read()
        a = 0


    def Ree(self):
        a = 0
        a = gp.Ree()
        a.read()
        a = 0

    def CIPW(self):
        a = 0
        a = gp.CIPW()
        a.read()
        a = 0

    def Trace1(self):
        a = 0
        a=gp.Trace()
        a.read()
        a = 0

    def Trace2(self):
        a=0
        a=gp.Trace2()
        a.read()
        a = 0

    def Qfl(self):
        a=0
        a=gp.Qfl()
        a.read()
        a=0

    def Qmflt(self):
        a=0
        a =gp.Qmflt()
        a.read()
        a=0

    def QapfP(self):
        a=0
        gp.QapfP().read()
        a=0

    def QapfV(self):
        a=0
        a =gp.QapfV()
        a.read()
        a=0

    def Wulf(self):
        a=0
        a =gp.Polar()
        a.wulf()
        a=0

    def Schmidt(self):
        a=0
        a =gp.Polar()
        a.schmidt()
        a=0


    def SingleRose(self):
        a=0
        a =gp.Polar()
        a.singlerose(Name=self.SR.split())
        a=0


    def MultiRose(self):
        a=0
        a =gp.Polar()
        a.multirose(Name=self.MR.split()[0])
        a=0


    def Pearce(self):
        a=0
        a =gp.Pearce()
        a.read()
        a=0

    def Harker(self):
        print(self.x,"\t",self.y)
        a=0
        a =gp.Harker(x=self.x,y=self.y)
        a.read()
        a=0

    def Ballard(self):
        a=0
        a = gp.Ballard()
        a.read()
        a=0

    def MultiBallard(self):
        b=0
        b=gp.MultiBallard()
        b.read()
        b=0

def Show():
    app = QApplication(sys.argv)
    ex = Simple()
    sys.exit(app.exec_())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Simple()
    sys.exit(app.exec_())
