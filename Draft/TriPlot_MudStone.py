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
        '20',
              ]
    Locations = [(10,10,80),
                (40,10,50),
                (10,40,50),
                (50,10,40),
                (30,30,30),
                (10,50,40),
                (80,10,10),
                (60,30,10),
                (40,50,10),  
                (10,80,10), 
                
                (20,0,80),
        (40,0,60),
        (60,0,40),
        (80,0,20),
        
        (20,80,0),
        (40,60,0),
        (60,40,0),
        (80,20,0),
        
        (0,20,80),
        (0,40,60),
        (0,60,40),
        (0,80,20),
                ]
    Offset = [(0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0),
                
                (-18,0),
                (-18,0),
                (-18,0),
                (-18,0),
                
                (0,-18),
                (0,-18),
                (0,-18),
                (0,-18),
                
                (0,0),
                (0,0),
                (0,0),
                (0,0),]

    name = "MudStone.xlsx"

    def __init__(self, name="MudStone.xlsx",Label=[u'Z', u'X', u'Y']):
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
        #20间隔点坐标： 
        Gap20=[(20,0,80),
        (40,0,60),
        (60,0,40),
        (80,0,20),
        
        (20,80,0),
        (40,60,0),
        (60,40,0),
        (80,20,0),
        
        
        (0,80,20),
        (0,60,40),
        (0,40,60),
        (0,20,80)]
        
        #二等分点坐标：
        Gap50=[(50,0,50),
        (40,20,40),
        
        (0,50,50),
        (20,40,40),
        
        (50,50,0),
        (40,40,20),]
        
        #四等分点坐标：
        Gap25=[(25,0,75),
        (0,25,75),
        
        (75,0,25),
        (75,25,0),
        
        (25,75,0),
        (0,75,25),]
        
        #中心三角坐标：
        Middle=[(20,20,60),
        (60,20,20),
        (20,60,20),]
        
        
        #中心三角垂直链接四等分线坐标：
        Other=[(12.5,12.5,75),
        (75,12.5,12.5),
        (12.5,75,12.5),]



        #中心三角绘制
        Unit.TriLine(Points=[Middle[0],Middle[1],Middle[2],Middle[0]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        
        
        #二等分和四等分线条绘制
        for i in range(len(Gap50)):
                    
            if i%2 ==0:
                Unit.TriLine(Points=[Gap50[i],Gap50[i+1]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
                Unit.TriLine(Points=[Gap25[i],Gap25[i+1]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        
        
        #中心外延线条绘制
        for i in range(len(Middle)):
            Unit.TriLine(Points=[Middle[i],Other[i]], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
            
        #20网格线条绘制   
        for i in range(len(Gap20)):
            if i<= len(Gap20)-5:
                Unit.TriLine(Points=[Gap20[i],Gap20[i+4]], Sort='', Width=0.5, Color='grey', Style="-", Alpha=0.5,
                Label='').show()
            else:
                Unit.TriLine(Points=[Gap20[i],Gap20[-1-i]], Sort='', Width=0.5, Color='grey', Style="-", Alpha=0.5,
                Label='').show()
                
                
        plt.xticks([])
        plt.yticks([])
        
        
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
            Unit.TriPoint((raw.at[i, 'X'], raw.at[i, 'Y'], raw.at[i, 'Z']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

        self.SavePic(name= self.name)

if __name__ == '__main__':
    TriPlot().read()