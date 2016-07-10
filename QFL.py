# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:33:43 2016

@author: cycleuser
@email: cycleuser@cycleuser.org

Copyright 2016 cycleuser

This file is part of GeoPython.

GeoPython is a set of free softwares for geology related daily work: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
GeoPython is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with GeoPython. If not, see http://www.gnu.org/licenses/.

This file is a module of QFL-plot for volcanic rocks.
All data used in this module are from  Dickinson 1979、1985


"""

#!/usr/bin/env python

# coding=utf-8

lang = "python"

import matplotlib.pyplot as plt
import math
import numpy as np


Width=1

Color='k'

def DrawLines(X=[0,1],Y=[0,1],LineWidth=1,LineColor='k',LineStyle="-",):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,)
    
    
    
def DrawTheLines(LineWidth=1,LineColor='k'):
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
    
    



def PlotPoints(X,Y,Size,Color,Alph):
    SpotSize = [5,25,175,200]
    SpotColor=['b','g','r','c','m','y','k','w']
    SpotAlpha=[0.25,0.5,0.75,1]
    plt.scatter(X,Y, s=SpotSize[Size],color =SpotColor[Color],alpha=SpotAlpha[Alph])

def PlotData(QflRaw,Width=1,Color='k'):
    DrawTheLines(Width,Color)
    Points = len(QflRaw)     
    for i in range(Points):        
        x=QflRaw.at[i,'Q']/2+(100-QflRaw.at[i,'Q'])*QflRaw.at[i,'L']/(QflRaw.at[i,'L']+QflRaw.at[i,'F'])
        y=(QflRaw.at[i,'Q'])/2*math.sqrt(3)
        PlotPoints(x,y,QflRaw.at[i,'Size'],QflRaw.at[i,'Color'],QflRaw.at[i,'Alpha'])  
    plt.savefig("Result-QFL-Plot.png",dpi=600)
    plt.savefig("Result-QFL-Plot.jpg",dpi=600)
    plt.savefig("Result-QFL-Plot.svg",dpi=600)
    plt.show()



def PlotBaseData(QflRaw,Width=1,Color='k'):
    DrawTheLines(Width,Color)
    Points = len(QflRaw)     
    for i in range(Points):        
        x=QflRaw.at[i,'Q']/2+(100-QflRaw.at[i,'Q'])*QflRaw.at[i,'F']/(QflRaw.at[i,'F']+QflRaw.at[i,'L'])
        y=(QflRaw.at[i,'Q'])/2*math.sqrt(3)
        PlotPoints(x,y,QflRaw.at[i,'Size'],QflRaw.at[i,'Color'],QflRaw.at[i,'Alpha'])  
    plt.savefig("Result-QFL-Plot.png",dpi=600)
    plt.savefig("Result-QFL-Plot.jpg",dpi=600)
    plt.savefig("Result-QFL-Plot.svg",dpi=600)
    plt.show()


if __name__ == '__main__':

    Width=1

    Color="Blue"


    DrawTheLines(Width,Color)
    plt.savefig("Default-QFL-Plot.png",dpi=600)
    plt.savefig("Default-QFL-Plot.jpg",dpi=600)
    plt.savefig("Default-QFL-Plot.svg",dpi=600)
    plt.show()









