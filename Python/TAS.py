# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:37:33 2016

@author: cycleuser
@email: cycleuser@cycleuser.org

Copyright 2016 cycleuser

This file is part of GeoPython.

GeoPython is a set of free softwares for geology related daily work: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
GeoPython is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with GeoPython. If not, see http://www.gnu.org/licenses/.

This file is a module of TAS-plot for volcanic rocks.
All data used in this module are from the book 
"Igneous Rocks_ a Classification and Glossary of Terms"
 by  R.W. Le Maitre & International Union of Geological Sciences 2002

Texts below is cited from this book as an introduction of TAS-plot:
"The TAS (Total Alkali – Silica) classification should be used only if:
(1) the rock is considered to be volcanic
(2) a mineral mode cannot be determined, owing either to the presence of glass or to the fine-grained nature of the rock
(3) a chemical analysis of the rock is available."



"""
#!/usr/bin/env python

# coding=utf-8

lang = "python"



#You need to install numpy and matplotlib to use this module
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
#sys is needed to add the TAS.py file in the path to import
#import sys
#sys.path.append("~/GeoPython/Drawer.py")
#import Drawer

'''
Drawer.DrawTasFrameLines(LineWidth=1,LineColor='k')


XHigh=[41,41,45,48.4,52.5]
YHigh=[3,7,9.4,11.5,14]

XMid=[61,57.6,53,49.4,45,45]
YMid=[(2.4*3.4/4.6+11.7),11.7,9.3,7.3,5,3]

XMid=[45,45,49.4,53,57.6,61]
YMid=[3,5,7.3,9.3,11.7,(2.4*3.4/4.6+11.7)]


XLow=[45,52,57,63,69]
YLow=[5,5,5.9,7,8]


XRightSpine=[50,52.5,57.6,63]
YRightSpine=[(2.5*2.3/5.1+14),14,11.7,7]


XMidSpine=[48.4,53,57]
YMidSpine=[11.5,9.3,5.9]


XLeftSpine=[45,49.4,52]
YLeftSpine=[9.4,7.3,5]


Drawer.DrawLines(XHigh,YHigh,LineWidth=0.5,LineColor='r')
Drawer.DrawLines(XMid,YMid,LineWidth=0.5,LineColor='r')
Drawer.DrawLines(XLow,YLow,LineWidth=0.5,LineColor='r')
Drawer.DrawLines(XRightSpine,YRightSpine,LineWidth=0.5,LineColor='r')
Drawer.DrawLines(XMidSpine,YMidSpine,LineWidth=0.5,LineColor='r')
Drawer.DrawLines(XLeftSpine,YLeftSpine,LineWidth=0.5,LineColor='r')



plt.show()
'''






def DrawTheLines(LineWidth=1,LineColor='k'):
    
#This DrawTheLines function is used to draw the lines in the figure
    plt.figure(figsize=(8,6), dpi=80)
    plt.xlim(35,79)
    plt.xticks(np.linspace(37,77,11,endpoint=True))
    plt.ylim(0,16)
    plt.yticks(np.linspace(1,15,8,endpoint=True))
    plt.xlabel(r'$SiO_2 wt\%$',fontsize=16)
    plt.ylabel(r'$Na_2O + K_2O wt\%$',fontsize=16)


#ax is used to set the axies
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))


    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',35))

#x and y are the values of the locations of points
    x=[41,45,48.4,49.4,52,52.5,53,57,57.6,63,69]
    y=[3,5,5.9,7,7.3,8,9.3,9.4,11.5,11.7,14]

#    LineLow =[(x[0],y[0]),(x[1],y[0]),(x[1],y[1]),(x[4],y[1]),(x[7],y[2]),(x[9],y[3]),(x[10],y[5])]
    XLow=[x[0],x[1],x[1],x[4],x[7],x[9],x[10]]
    YLow=[y[0],y[0],y[1],y[1],y[2],y[3],y[5]]


#    LineMid =[(x[3],y[4]),(x[6],y[6]),(x[8],y[9])]

    XMid =[x[1],x[3],x[6],x[8]]
    YMid =[y[1],y[4],y[6],y[9]]

#    LineHigh=[(x[0],y[3]),(x[1],y[7]),(x[2],y[8]),(x[5],y[10])]

    XHigh=[x[0],x[0],x[1],x[2],x[5]]
    YHigh=[y[0],y[3],y[7],y[8],y[10]]

#    YBase=[y[0],y[0],y[1],y[1],y[2],y[3],y[5]]

    for i in range(6):
        plt.plot([XLow[i],XLow[i]],[0.5,YLow[i]],label='DownBase',color=LineColor, linewidth=LineWidth, linestyle="-",)

    plt.plot([XLow[6],XLow[6]],[13,YLow[6]],label='UpBase',color=LineColor, linewidth=LineWidth, linestyle="-",)
    plt.plot([76.5,XLow[6]],[0.5,YLow[6]],label='RightBase',color=LineColor, linewidth=LineWidth, linestyle="-",)
    plt.plot(XLow,YLow,label='LineLow',color=LineColor, linewidth=LineWidth, linestyle="-",)
    plt.plot(XMid,YMid,label='LineMid',color=LineColor, linewidth=LineWidth, linestyle="-",)
    plt.plot([XHigh[0],XHigh[1],XHigh[2]],[YHigh[0],YHigh[1],YHigh[2]],label='LinweHigh',color=LineColor, linewidth=LineWidth, linestyle='--',)
    plt.plot([XHigh[2],XHigh[3],XHigh[4]],[YHigh[2],YHigh[3],YHigh[4]],label='LinweHigh',color=LineColor, linewidth=LineWidth, linestyle="-",)

    for i in range(3):
        plt.plot([XMid[i+1],XLow[i+3]],[YMid[i+1],YLow[i+3]],label='MidToLow',color=LineColor, linewidth=LineWidth, linestyle="-",)

    for i in range(3):
        plt.plot([XMid[i+1],XHigh[i+2]],[YMid[i+1],YHigh[i+2]],label='MidToHigh',color=LineColor, linewidth=LineWidth, linestyle="-",)

    plt.plot([XHigh[4],50],[YHigh[4],(2.5*2.3/5.1+14)],label='Higher',color=LineColor, linewidth=LineWidth, linestyle="-",)
    plt.plot([XMid[3],61],[YMid[3],(2.4*3.4/4.6+11.7)],label='Higher',color=LineColor, linewidth=LineWidth, linestyle="-",)



#Labels are the names of different kinds of rocks
    Labels=[u'F',u'Pc',u'U1',u'B',u'S1',u'U2',u'O1',u'S2',u'U3',u'O2',u'S3',u'Ph',u'O2',u'T',u'R']

#Items are the positions of those Labels
    Items =[(39,10),(43,1.5),(44,6),(48.5,2.5),(49,6),(49,9.5),(54,3),(53,7),(53,12),(60,4),(57,8.5),(57,14),(67,5),(65,10),(75,9)]

    for i in range(len(Items)):
        plt.annotate(Labels[i],xy=(Items[i]), xycoords='data',xytext=(-6, -3), textcoords='offset points', fontsize=12,)


    
'''
b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white
'''

def PlotPoints(X,Y,Size,Color,Alph,Marker ='d'):
    plt.scatter(X,Y, marker= Marker,s=Size,color =Color,alpha=Alph)    


def PlotData(TasRaw,Width=1,Color='k'):
    
    DrawTheLines(Width,Color)
    Points = len(TasRaw)    
    for i in range(Points):
        PlotPoints((TasRaw.at[i,'SiO2']),(TasRaw.at[i,'Na2O']+TasRaw.at[i,'K2O']),TasRaw.at[i,'Size'],TasRaw.at[i,'Color'],TasRaw.at[i,'Alpha'],TasRaw.at[i,'Marker'])
    plt.savefig("TAS-Plot.png",dpi=600)
    plt.savefig("TAS-Plot.svg",dpi=600)
    plt.show()



if __name__ == '__main__':
    #You need to put you data in a xlsx file in the same form as the example file
    TasRawData = pd.read_excel("TAS.xlsx")
 

    #You only need to input the data from the file
    PlotData(TasRawData)


   








