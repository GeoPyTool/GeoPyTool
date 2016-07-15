# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 13:38:54 2016

@author: cycleuser
@email: cycleuser@cycleuser.org

Copyright 2016 cycleuser

This file is part of GeoPython.

GeoPython is a set of free softwares for geology related daily work: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
GeoPython is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with GeoPython. If not, see http://www.gnu.org/licenses/.

This file is a module of drawing lines

"""


#!/usr/bin/env python

# coding=utf-8

lang = "python"


#You need to install numpy and matplotlib to use this module
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

def DrawLines(X=[0,1],Y=[0,1],LineWidth=1,LineColor='k',LineStyle="-",):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,)
    
    
    
def DrawTriangle(LineWidth=1,LineColor='k'):
    plt.figure(figsize=(8,4*math.sqrt(3)), dpi=80)
    plt.xlim(-10,110)
    plt.ylim(-10,100)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    
    XBorder=[0,50,100,0]
    YBorder=[0,50*math.sqrt(3),0,0]


    DrawLines(XBorder,YBorder,LineWidth=1,LineColor='k')
    

    
    XSpecialLon=[[51.5,15],
                 [27.5,87.5]
                ]
    YSpecialLon=[[48.5*math.sqrt(3),0],
                 [27.5*math.sqrt(3),12.5*math.sqrt(3)]          
                ]
    for i in range(len(XSpecialLon)):
        DrawLines(XSpecialLon[i],YSpecialLon[i],LineWidth=1,LineColor='k',LineStyle="-",)     
    
    
    
    LineMid=Drawer.CrossPoint(13/2,13/2*math.sqrt(3),100-37/2,37/2*math.sqrt(3),55/2,55/2*math.sqrt(3),100-25/2,25/2*math.sqrt(3))    
    LineLeft=Drawer.CrossPoint(15,0,51.5,48.5*math.sqrt(3),13/2,13/2*math.sqrt(3),100-37/2,37/2*math.sqrt(3))    
    
    
    XMid=[[LineMid[0],LineLeft[0]],
          [LineMid[0],100-37/2],
          [50,87.5],
         ]
    YMid=[[LineMid[1],LineLeft[1]]  ,
          [LineMid[1],37/2*math.sqrt(3)] ,
          [0,12.5*math.sqrt(3)]          
         ]
    for i in range(len(XMid)):
        DrawLines(XMid[i],YMid[i],LineWidth=1,LineColor='k',LineStyle="--",)     

#Label are the names of different kinds of rocks
    Label=[u'Q',
           u'F',
           u'L']

#LabelPosition are the positions of those Labels
    LabelPosition =[(48,50*math.sqrt(3)+2),
            (-6,-1),
            (104,-1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i],xy=(LabelPosition[i]), xycoords='data',xytext=(0,0), textcoords='offset points', fontsize=16,)
    
    



if __name__ == '__main__':
    Width=1
    Color="Blue"
    x=[41,45,48.4,49.4,52,52.5,53,57,57.6,63,69]
    y=[3,5,5.9,7,7.3,8,9.3,9.4,11.5,11.7,14]
    DrawTriangle()