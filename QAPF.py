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

This file is a module of QAPF-plot for volcanic rocks.
All data used in this module are from the book 
"Igneous Rocks_ a Classification and Glossary of Terms"
 by  R.W. Le Maitre & International Union of Geological Sciences 2002

Texts below is cited from this book as an introduction of QAPF-plot:
"QAPF modal classification of volcanic rocks (based on Streckeisen, 1978, Fig. 1). 
The corners of the double triangle are Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid. 
This diagram must not be used for rocks in which the mafic mineral content, M, is greater than 90%."

“To use the classification the modal amounts of Q, A, P, and F must be known and recalcu- lated so that their sum is 100%.
For example, a rock with Q = 10%, A = 30%, P = 20%, and M = 40% would give recalculated values of Q, A, and P as follows:
Q = 100 £ 10 / 60 = 16.7 A = 100 £ 30 / 60 = 50.0 P = 100 £ 20 / 60 = 33.3
Although at this stage the rock can be plotted directly into the triangular diagram, if all that is required is to name the rock it is easier to determine the plagioclase ratio where:
plagioclase ratio = 100 £ P / (A + P)
as the non-horizontal divisions in the QAPF diagram are lines of constant plagioclase ratio. The field into which the rock falls can then easily be determined by inspection.
In the above example rock the plagioclase ratio is 40 so that it can be seen by inspection that the rock falls into QAPF field 8* (Fig. 2.5) and should, therefore, be called a quartz monzonite (Fig. 2.4).
Similarly, a rock with A = 50%, P = 5%, F = 30%, and M = 15% would recalculate as fol- lows:
A = 100 £ 50 / 85 = 58.8 P = 100 £ 5 / 85 = 5.9
F = 100 £ 30 / 85 = 35.3 Plagioclase ratio = 9
”


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
    plt.figure(figsize=(8,8*math.sqrt(3)), dpi=80)
    plt.xlim(-10,110)
    plt.ylim(-100,100)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    
    XBorder=[0,50,100,50,0]
    YBorder=[0,50*math.sqrt(3),0,-50*math.sqrt(3),0]


    DrawLines(XBorder,YBorder,LineWidth=1,LineColor='k')
    
#x= 65-y*math.sqrt(3)*0.1
    
    XLat=[[45,55],
          [30,70],
          [10,90],
          [2.5,65-2.5*math.sqrt(3)*math.sqrt(3)*0.1],
          [0,65],
          [5,95],
          [30,70],
          [45,55]
          ]
    YLat=[[45*math.sqrt(3),45*math.sqrt(3)],
          [30*math.sqrt(3),30*math.sqrt(3)],
          [10*math.sqrt(3),10*math.sqrt(3)],
          [2.5*math.sqrt(3),2.5*math.sqrt(3)],
          [0,0],     
          [-5*math.sqrt(3),-5*math.sqrt(3)],
          [-30*math.sqrt(3),-30*math.sqrt(3)], 
          [-45*math.sqrt(3),-45*math.sqrt(3)]     
          ]

    for i in range(len(XLat)):
        DrawLines(XLat[i],YLat[i],LineWidth=1,LineColor='k') 
      
    XLon=[[34,10,34],
          [38,35,36.5],
          [56,65,63.5],
          [66,86],
          [50,50]
          ]
          
          
          
    YLon=[[30*math.sqrt(3),0,-30*math.sqrt(3)],
          [10*math.sqrt(3),0,-5*math.sqrt(3)],
          [30*math.sqrt(3),0,-5*math.sqrt(3)],         
          [-30*math.sqrt(3),-5*math.sqrt(3)],
          [0,-45*math.sqrt(3)]
          ]

    for i in range(len(XLon)):
        DrawLines(XLon[i],YLon[i],LineWidth=1,LineColor='k',LineStyle="-",) 

      
    XSpecialLon=[[44,38],
                 [66,82]                 
                ]
    YSpecialLon=[[30*math.sqrt(3),10*math.sqrt(3)],
                 [30*math.sqrt(3),10*math.sqrt(3)]
                ]
    for i in range(len(XSpecialLon)):
        DrawLines(XSpecialLon[i],YSpecialLon[i],LineWidth=1,LineColor='k',LineStyle="--",) 
    
#Label are the names of different kinds of rocks
    Label=[u'Q',
            u'A',
            u'F',
            u'P']

#LabelPosition are the positions of those Labels
    LabelPosition =[(48,50*math.sqrt(3)+2),
            (-6,-1),
            (48.5,-5-50*math.sqrt(3)),
            (104,-1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i],xy=(LabelPosition[i]), xycoords='data',xytext=(0,0), textcoords='offset points', fontsize=16,)
    
    
    Scale=[u'90',u'90',
           u'60',u'60',
           u'20',u'0',u'35',u'65',u'90',u'20',
           u'5',
           u'10',u'50',u'90',u'10',
           u'60',u'60',
           u'90',u'90'] 
    '''
    ScalePosition=[(45,45*math.sqrt(3)),(55,45*math.sqrt(3)),
                   (30,30*math.sqrt(3)),(70,30*math.sqrt(3)),
                   (10,10*math.sqrt(3)),(18,10*math.sqrt(3)),(38,10*math.sqrt(3)),(62,10*math.sqrt(3)),(82,10*math.sqrt(3)),(90,10*math.sqrt(3)),
                   (65-2.5*math.sqrt(3)*math.sqrt(3)*0.1,2.5*math.sqrt(3)),
                   (14,-5*math.sqrt(3)),(50,-5*math.sqrt(3)),(86,-5*math.sqrt(3)),(95,-5*math.sqrt(3)),
                   (30,-30*math.sqrt(3)),(70,-30*math.sqrt(3)),
                   (45,-45*math.sqrt(3)),(55,-45*math.sqrt(3))] 
    
    '''
    
    
    ScalePosition=[(40,45*math.sqrt(3)),(57,45*math.sqrt(3)),
                   (25,30*math.sqrt(3)),(72,30*math.sqrt(3)),
                   (5,10*math.sqrt(3)-2),(21,10*math.sqrt(3)+2),(41,10*math.sqrt(3)+2),(62,10*math.sqrt(3)+2),(82,10*math.sqrt(3)+2),(92,10*math.sqrt(3)-2),
                   (65-2.5*math.sqrt(3)*math.sqrt(3)*0.1,2.5*math.sqrt(3)),
                   (14,-5*math.sqrt(3)+2),(50,-5*math.sqrt(3)+2),(86,-5*math.sqrt(3)+2),(95,-5*math.sqrt(3)-2),
                   (25,-30*math.sqrt(3)),(72,-30*math.sqrt(3)),
                   (40,-45*math.sqrt(3)),(57,-45*math.sqrt(3))] 
    
    
    
    
    
    for i in range(len(ScalePosition)):
        plt.annotate(Scale[i],xy=(ScalePosition[i]), xycoords='data',xytext=(0,0), textcoords='offset points', fontsize=12,)
        
    


    Name=[u'Alkali Feldspar Rhyolite',u'Rhyolite',u'Dacite'
            ,u'Quartz Alkali Feldspar Trachyte',u'Quartz Trachyte',u'Quartz Latite'
            ,u'Alkali Feldspar Trachyte',u'Trachyte',u'Latite'
            ,u'Foid-Bearing Alkali Feldspar Trachyte',u'Foid-Bearing Trachyte',u'Foid-Bearing Latite',u'Basalt Andesite'
            ,u'Phonolite',u'Tephritic Phonolite',u'Phonolitic Basanite(olivine>10%) OR Phonolitic Tephrite(olivine<10%)',u'Basanite(olivine>10%) OR Tephrite(olivine<10%)'
            ,u'Phonolitic Foidite',u'Tephritic Foidite'
            ,u'Foidite'
           ]     
           
    NamePosition=[u'Alkali Feldspar Rhyolite',u'Rhyolite',u'Dacite'
            ,u'Quartz Alkali Feldspar Trachyte',u'Quartz Trachyte',u'Quartz Latite'
            ,u'Alkali Feldspar Trachyte',u'Trachyte',u'Latite'
            ,u'Foid-Bearing Alkali Feldspar Trachyte',u'Foid-Bearing Trachyte',u'Foid-Bearing Latite',u'Basalt Andesite'
            ,u'Phonolite',u'Tephritic Phonolite',u'Phonolitic Basanite(olivine>10%) OR Phonolitic Tephrite(olivine<10%)',u'Basanite(olivine>10%) OR Tephrite(olivine<10%)'
            ,u'Phonolitic Foidite',u'Tephritic Foidite'
            ,u'Foidite'
           ]   
           
           
           
           
    



def PlotPoints(X,Y,Size,Color,Alph,Marker ='o'):
    plt.scatter(X,Y, marker= Marker,s=Size,color =Color,alpha=Alph)    

#PlotPoints(x,y,QflRaw.at[i,'Size'],QflRaw.at[i,'Color'],QflRaw.at[i,'Alpha'],QflRaw.at[i,'Marker'])  


def PlotData(QapfRaw,Width=1,Color='k'):
    
    DrawTheLines(Width,Color)
    
    Points = len(QapfRaw)    
    
    for i in range(Points):        
        
        
        q=QapfRaw.at[i,'Q']
        f=QapfRaw.at[i,'F']
        a=QapfRaw.at[i,'A']
        p=QapfRaw.at[i,'P']
        
        Q=100*q/(q+a+p)
        F=100*f/(f+a+p)

        
        if( Q>0):
            A=100*a/(q+a+p)
            P=100*p/(q+a+p)
            x=Q/2+(100-Q)*P/(A+P)
            y=(Q)/2*math.sqrt(3)
        if( F>0):
            A=100*a/(f+a+p)
            P=100*p/(f+a+p)
            x=F/2+(100-F)*P/(A+P)
            y=-(F)/2*math.sqrt(3)
        PlotPoints(x,y,QapfRaw.at[i,'Size'],QapfRaw.at[i,'Color'],QapfRaw.at[i,'Alpha'],QapfRaw.at[i,'Marker'])
        

    
    plt.savefig("Result-QAPF-Plot.png",dpi=600)
    plt.savefig("Result-QAPF-Plot.jpg",dpi=600)
    plt.savefig("Result-QAPF-Plot.svg",dpi=600)
    plt.show()



if __name__ == '__main__':

    Width=1

    Color="Blue"


    DrawTheLines(Width,Color)
    plt.savefig("Default-Qapf-Plot.png",dpi=600)
    plt.savefig("Default-Qapf-Plot.jpg",dpi=600)
    plt.savefig("Default-Qapf-Plot.svg",dpi=600)
    plt.show()









