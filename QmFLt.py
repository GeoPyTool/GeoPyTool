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

This file is a module of QmFLt-plot for sedimentary rocks.
All data used in this module are from  Dickinson 1979、1985


"""

#!/usr/bin/env python

# coding=utf-8

lang = "python"

import matplotlib.pyplot as plt
import math
import sys
sys.path.append("./Drawer.py")

#import the module first and then you can use the functions in it
import Drawer

Width=1

Color='k'

   
    

def DrawLines(X=[0,1],Y=[0,1],LineWidth=1,LineColor='k',LineStyle="-",):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,)
    
def CrossPoint(x0,y0,x1,y1,x2,y2,x3,y3): 
    a = y1-y0 
    b = x1*y0-x0*y1 
    c = x1-x0 
    d = y3-y2 
    e = x3*y2-x2*y3 
    f = x3-x2 
    y = float(a*e-b*d)/(a*f-c*d) 
    x = float(y*c-b)/a 
    print(x,y)
    return([x,y])   
    
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
    

    
    XSpecialLon=[[55.5,23],
                 [27.5,93.5],
                 [40,87]
                ]
    YSpecialLon=[[44.5*math.sqrt(3),0],
                 [27.5*math.sqrt(3),6.5*math.sqrt(3)],
                 [40*math.sqrt(3),0]
                ]
    for i in range(len(XSpecialLon)):
        DrawLines(XSpecialLon[i],YSpecialLon[i],LineWidth=1,LineColor='k',LineStyle="-",)     
    
    
    
    LineMid=CrossPoint(9,9*math.sqrt(3),84,16*math.sqrt(3),57/2,57/2*math.sqrt(3),100-13/2,13/2*math.sqrt(3))    
    LineLeft=CrossPoint(23,0,55.5,44.5*math.sqrt(3),9,9*math.sqrt(3),84,16*math.sqrt(3))    
    
    
    XMid=[[LineMid[0],LineLeft[0]],
          [LineMid[0],84],
          [47,91],
         ]
    YMid=[[LineMid[1],LineLeft[1]]  ,
          [LineMid[1],16*math.sqrt(3)] ,
          [0,9*math.sqrt(3)]          
         ]
    for i in range(len(XMid)):
        DrawLines(XMid[i],YMid[i],LineWidth=1,LineColor='k',LineStyle="--",)     

#Label are the names of different kinds of rocks
    Label=[u'Qm',
           u'F',
           u'Lt']

#LabelPosition are the positions of those Labels
    LabelPosition =[(48,50*math.sqrt(3)+2),
            (-6,-1),
            (104,-1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i],xy=(LabelPosition[i]), xycoords='data',xytext=(0,0), textcoords='offset points', fontsize=16,)
    
    






def PlotPoints(X,Y,Size,Color,Alph,Marker ='o'):
    plt.scatter(X,Y, marker= Marker,s=Size,color =Color,alpha=Alph)    

#PlotPoints(x,y,QflRaw.at[i,'Size'],QflRaw.at[i,'Color'],QflRaw.at[i,'Alpha'],QflRaw.at[i,'Marker'])  
   


def PlotData(QmFLtRaw,Width=1,Color='k'):
    DrawTheLines(Width,Color)
    Points = len(QmFLtRaw)     
    for i in range(Points):        
        q=QmFLtRaw.at[i,'Qm']
        f=QmFLtRaw.at[i,'F']
        l=QmFLtRaw.at[i,'Lt']
        
        Q=100*q/(q+f+l)
        F=100*f/(q+f+l) 
        L=100*l/(q+f+l) 
        
        
        x= Q/2+(100-Q)*L/(L+F)
        y= Q/2*math.sqrt(3)
        
        PlotPoints(x,y,QmFLtRaw.at[i,'Size'],QmFLtRaw.at[i,'Color'],QmFLtRaw.at[i,'Alpha'],QmFLtRaw.at[i,'Marker'])  
    plt.savefig("Result-QmFLt-Plot.png",dpi=600)
    plt.savefig("Result-QmFLt-Plot.jpg",dpi=600)
    plt.savefig("Result-QmFLt-Plot.svg",dpi=600)
    plt.show()



def PlotBaseData(QmFLtRaw,Width=1,Color='k'):
    DrawTheLines(Width,Color)
    Points = len(QmFLtRaw)     
    for i in range(Points):       
        q=QmFLtRaw.at[i,'Qm']
        f=QmFLtRaw.at[i,'F']
        l=QmFLtRaw.at[i,'Lt']
        
        Q=100*q/(q+f+l)
        F=100*f/(q+f+l) 
        L=100*l/(q+f+l) 
        
        
        x= Q/2+(100-Q)*L/(L+F)
        y= Q/2*math.sqrt(3)
        
        
        PlotPoints(x,y,QmFLtRaw.at[i,'Size'],QmFLtRaw.at[i,'Color'],QmFLtRaw.at[i,'Alpha'])  
    plt.savefig("Result-QmFLt-Plot.png",dpi=600)
    plt.savefig("Result-QmFLt-Plot.jpg",dpi=600)
    plt.savefig("Result-QmFLt-Plot.svg",dpi=600)
    plt.show()


if __name__ == '__main__':

    Width=1

    Color="Blue"


    DrawTheLines(Width,Color)
    plt.savefig("Default-QmFLt-Plot.png",dpi=600)
    plt.savefig("Default-QmFLt-Plot.jpg",dpi=600)
    plt.savefig("Default-QmFLt-Plot.svg",dpi=600)
    plt.show()









