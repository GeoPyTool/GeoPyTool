#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this Simple, we determine the event sender
object.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import geopython as gp


class Simple(QMainWindow):
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



        self.statusBar()

        self.setGeometry(600, 600, 300, 300)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

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
        gp.Harker().read()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Simple()
    sys.exit(app.exec_())