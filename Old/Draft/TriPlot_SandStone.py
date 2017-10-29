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



    name = "SandStone.xlsx"

    def __init__(self, name="SandStone.xlsx",Label=[u'Q', u'F', u'L:']):
        super().__init__()

        self.raw = ''

        self.Label = Label
        self.name=name
        

       
    def draw(self):
        """
        use the values to set up the general frame and lines, fill particular zone with given colors
        """
        A=[(75,25,0),(50,50,0),(25,75,0),(25,0,75),(18.75,6.25,75),(12.5,12.5,75),(6.25,18.75,75),(0,25,75),(10,0,90),(5,5,90),(0,10,90)]
        

        Unit.TriLine(Points=[A[0],A[4]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        
        
        Unit.TriLine(Points=[A[1],A[9]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        
        Unit.TriLine(Points=[A[2],A[6]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        
        Unit.TriLine(Points=[A[3],A[7]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        
        Unit.TriLine(Points=[A[8],A[10]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        plt.xticks([])
        plt.yticks([])
        
        

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
            Unit.TriPoint((raw.at[i, 'F'], raw.at[i, 'L'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

        self.SavePic(name= self.name)

if __name__ == '__main__':
    TriPlot().read()