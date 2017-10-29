# !/usr/bin/env python3#!/usr/bin/env python3
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
    3) TasSample= Tas("tas.xlsx")
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

lang = "python"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
import math
import sys
import csv

import Unit

class TriPlot(Unit.Tri,Unit.Tool):

    """
    inherit Tri and Tool, read xlsx or csv file and make QFL diagram
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []
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

    name = "QmPK.xlsx"

    def __init__(self, name="QmPK.xlsx",Label=[u'Qm', u'P', u'K:']):
        super().__init__()

        self.raw = ''

        self.Label = Label
        self.name=name
        for i in range(len(self.Labels)):
            self.Tags.append(Unit.Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1], self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def draw(self):
        """
        use the values to set up the general frame and lines, fill particular zone with given colors
        """

        Unit.TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        Unit.TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        Unit.TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()
        T0 = (85, 15, 0)
        T1 = (0, 3, 97)
        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T4 = self.TriCross(A=[T0,T1] , B=[T2,T3])

        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T5 = (45, 0, 55)
        T6 = (0, 75, 25)


        T7 = self.TriCross(A=[T2,T3] , B=[T5,T6])

        Unit.TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        Unit.TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='').show()

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        Unit.TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)


        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        for i in self.Tags:
            i.show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            Unit.TriPoint((raw.at[i, 'P'], raw.at[i, 'K'], raw.at[i, 'Qm']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

        self.SavePic(name= self.name)

if __name__ == '__main__':
    TriPlot().read()