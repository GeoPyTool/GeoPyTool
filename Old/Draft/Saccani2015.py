#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 00:19:04 2017

@author: cycleuser
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


class Saccani():
    
    name= 'Saccani.xlsx'
    xLabel='Nb N(PPM)'
    yLabel='Th N (PPM)'
    
    Width =9
    Height=9
    Dpi=80
    FontSize=12
    
    Left,Right=-2,2 
    Base,Top=-2,3
    
    X0,Y0=-2,-2
    X1,Y1=2,3
    
    Xtext,Ytext=[u'0.01', u'0.1', u'1', u'10', u'100'],[u'0.01', u'0.1',u'1', u'10', u'100', u'1000']
    
    X_Gap,Y_Gap=6,5
    Lines = [Unit.LogLine([(0.01,20),(2.2,8.0)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      Unit.LogLine([(0.306,0.708),(100,1000)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      Unit.LogLine([(0.01,0.1),(0.306,0.708),(0.5,0.01)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),]

    def __init__(self):
        pass
    
    def show(self):
        """
        show the frame and lines on canvas
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        plt.xlim(self.Left, self.Right)
        plt.ylim(self.Base, self.Top)
        plt.xticks(np.linspace(self.X0, self.X1, self.X_Gap, endpoint=True), self.Xtext)
        plt.yticks(np.linspace(self.Y0, self.Y1, self.Y_Gap, endpoint=True), self.Ytext)
        plt.xlabel(self.xLabel, fontsize=self.FontSize)
        plt.ylabel(self.yLabel, fontsize=self.FontSize)
        for i in self.Lines:
            i.show()
            
            
    def read(self):
        self.show()
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~


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
                #TmpLabel = raw.at[i, 'Label']
            #Unit.TriPoint((raw.at[i, 'X'], raw.at[i, 'Y'], raw.at[i, 'Z']), Size=raw.at[i, 'Size'],
                     #Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     #Label=TmpLabel).show()

        self.SavePic(name= self.name)
        """
if __name__ == '__main__':
    Saccani().read()