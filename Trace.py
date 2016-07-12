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

This file is a module of Trace Element plot.



"""
#!/usr/bin/env python

# coding=utf-8

lang = "python"



#You need to install numpy and matplotlib to use this module

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math




class Point:
     x=0.0
     y=0.0
     Color = 'black'
     Size = 1
     Alpha = 0.5
     Marker='o'
     
     def __init__(self,X=0,Y=0,Color = 'black', Size = 1,Alpha = 0.5,Marker='o'):
           self.x=X
           self. y=Y
           self.Color=Color
           self.Size=Size
           self.Alpha=Alpha
           self.Marker=Marker

     def __del__(self):
         pass
    


class Line:   
    # Head= Point(0,0)
     Points=[]
     #Mid= []
     #End= Point(0,0)
     Length=0
     x=[]
     y=[]
     Color = 'black'
     Size = 1
     Alpha = 0.5
     Style='_'
     
     def __init__(self, Head= Point(),End= Point (),Mid=[],Color = 'black', Width = 1,Alpha = 0.5,Style='_'):
      #     self.Head.x= A.x
       #    self.Head.y= A.y
        #   self.Mid=C
             #  self.End.x= B.x
          # self.End.y= B.y
           
           self.Points.append(Head)
           
           for k in Mid:
               self.Points.append(k)
           
           self.Points.append(End)           
           
           self.Color=Color
           self.Width=Width
           self.Alpha=Alpha
           self.Style=Style
                         
           for index, i in enumerate(self.Points):
               self.x.append(i.x)
               self.y.append(i.y)
               
               if(index!=0):
                   self.Length+= Distance(self.Points[index-1],self.Points[index])
            
          
          #self.Length=math.sqrt(math.pow(self.Head.x-self.End.x, 2)+math.pow(self.Head.y-self.End.y, 2))

     def __del__(self):
         pass
 
     def AddPoint(self,NewPoint= Point(0,0)):       
         self.Length+= Distance(self.Points[-1],NewPoint)
         self.Points.append(NewPoint)  
         self.x.append(NewPoint.x)
         self.y.append(NewPoint.y)
        
#     def Draw(self):         
#         return (self.Head,self.End, self.Width,self.Color,self.Style)


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



def Distance(A= Point(3,4),B= Point(3,5)): 
    return(math.sqrt((A.x-B.x)**2+(A.y-B.y)**2))
    
def LineFormula(A= Point(3,4),B= Point(3,5)): 
    #Find formula of a line with Two given Points ky = m*x +n   
    k=1
    m=0
    n=0
   

    if(A.x==B.x):
        k=0
        m=1
        n=-A.x
    elif(A.y==B.y):        
        k=1
        m=0
        n=A.y  
    else: #(A.x!=B.x or A.y!=B.y):
        m=(B.y-A.y)/(B.x-A.x)
        n=A.y-m*A.x                   
    
    return(k,m,n)
        
def Cross(A= Point(3,4),B= Point(3,5),C= Point(4,4.5),D= Point(2,3.5)):
    #Find the cross point of two lines
    a = B.y-A.y 
    b = B.x*A.y-A.x*B.y 
    c = B.x-A.x
    d = D.y-C.y 
    e = D.x*C.y-C.x*D.y 
    f = D.x-C.x 
    
    if ((a*f-c*d)==0):    
        return("No Cross!")
    elif(a==0):
        y=A.y
        tmp= LineFormula(C,D)
        x= (tmp[0]*y)-tmp[2]/tmp[1]
        Answer= Point (x,y)
        return(Answer)    
    else:# ((a*f-c*d) !=0):
        y = float(a*e-b*d)/(a*f-c*d) 
        x = float(y*c-b)/a        
        Answer= Point (x,y)
        return(Answer)




def DrawPoint(a=Point(0,0)):
    plt.scatter(a.x,a.y,marker=a.Marker,c=a.Color,s=a.Size,alpha=a.Alpha)

def DrawLine(X=[0,1],Y=[0,1],LineColor='k',LineWidth=1,LineStyle="-",LineAlpha=0.3):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,alpha= LineAlpha)


def DrawLines(X=[0,1],Y=[0,1],LineColor='k',LineWidth=1,LineStyle="-",LineAlpha=0.3):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,alpha= LineAlpha)
    
def PlotPoints(X,Y,Size,Color,Alph,Marker):
    SpotSize = [5,25,175,200]
    SpotColor=['b','g','r','c','m','y','k','w']
    SpotAlpha=[0.25,0.5,0.75,1]
    plt.scatter(X,Y, marker= Marker,s=SpotSize[Size],color =SpotColor[Color],alpha=SpotAlpha[Alph])    






def Sign(What=[u'La',u'Ce',u'Pr',u'Nd',
               u'Sm',u'Eu',u'Gd',u'Tb',
               u'Dy',u'Ho',u'Er',u'Tm',
               u'Yb',u'Lu',u'Y'],
         Where=[(1,0.5),(2,0.5),(3,0.5),(4,0.5),
                (5,0.5),(6,0.5),(7,0.5),(8,0.5),
                (9,0.5),(10,0.5),(11,0.5),(12,0.5),
                (13,0.5),(14,0.5),(15,0.5)]):
    #Label are the names of different kinds of rocks
    Label=What

#LabelPosition are the positions of those Labels
    LabelPosition =Where

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i],xy=(LabelPosition[i]), xycoords='data',xytext=(-4,-24), textcoords='offset points', fontsize=12,)
    


def DrawREEFrame(LineWidth=1,LineColor='k'):
    
#This DrawTheLines function is used to draw the lines in the figure
    plt.figure(figsize=(8,6), dpi=80)
    plt.xlim(0,16)
    #plt.xticks(np.linspace(1,15,15,endpoint=True))
    
    
    plt.xticks(np.linspace(1,15,15,endpoint=True),
       [u'La',u'Ce',u'Pr',u'Nd',
               u'Sm',u'Eu',u'Gd',u'Tb',
               u'Dy',u'Ho',u'Er',u'Tm',
               u'Yb',u'Lu',u'Y'])
    plt.ylim(-0.1,5)
    
    
    plt.yticks(np.linspace(0,3,4,endpoint=True),
               [u'1',u'10',u'100',u'1000']
               )
    plt.xlabel(r'$REE-Standardlized-Pattern$',fontsize=16)
    #plt.ylabel(r'$Na_2O + K_2O wt\%$',fontsize=16)


#ax is used to set the axies
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))


    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))



    
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



#WholeData=[]

X=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

def PlotData(REERaw,Width=1,Color='b',Style="-",k=0):
    DrawREEFrame(LineWidth=1,LineColor='k')
    REEBase= pd.read_excel("REEBase.xlsx")
    for i in range(len(REERaw)):
        
        A=Point(1, math.log((REERaw.at[i,'La'])/REEBase.at[k,'La']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        B=Point(2, math.log((REERaw.at[i,'Ce'])/REEBase.at[k,'Ce']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        C=Point(3, math.log((REERaw.at[i,'Pr'])/REEBase.at[k,'Pr']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        D=Point(4, math.log((REERaw.at[i,'Nd'])/REEBase.at[k,'Nd']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        E=Point(5, math.log((REERaw.at[i,'Sm'])/REEBase.at[k,'Sm']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        F=Point(6, math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        G=Point(7, math.log((REERaw.at[i,'Gd'])/REEBase.at[k,'Gd']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        H=Point(8, math.log((REERaw.at[i,'Tb'])/REEBase.at[k,'Tb']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        I=Point(9, math.log((REERaw.at[i,'Dy'])/REEBase.at[k,'Dy']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        J=Point(10, math.log((REERaw.at[i,'Ho'])/REEBase.at[k,'Ho']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        K=Point(11, math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        L=Point(12, math.log((REERaw.at[i,'Tm'])/REEBase.at[k,'Tm']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        M=Point(13, math.log((REERaw.at[i,'Yb'])/REEBase.at[k,'Yb']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
        N=Point(14, math.log((REERaw.at[i,'Lu'])/REEBase.at[k,'Lu']),Color=REERaw.at[i,'Color'],Size=REERaw.at[i,'Size'],Alpha=REERaw.at[i,'Alpha'],Marker=REERaw.at[i,'Marker'])
       # O=(Point(15, math.log((REERaw.at[i,'Y'])/REEBase.at[k,'Y'])))         
        
        DrawPoint(A)
        DrawPoint(B)
        DrawPoint(C)
        DrawPoint(D)
        DrawPoint(E)
        DrawPoint(F)
        DrawPoint(G)
        DrawPoint(H)
        DrawPoint(I)
        DrawPoint(J)
        DrawPoint(K)
        DrawPoint(L)
        DrawPoint(M)
        DrawPoint(N)
        #DrawPoint(O)
        
        NewTmp=[]
        NewTmp.append(math.log((REERaw.at[i,'La'])/REEBase.at[k,'La']))
        NewTmp.append(math.log((REERaw.at[i,'Ce'])/REEBase.at[k,'Ce']))
        NewTmp.append(math.log((REERaw.at[i,'Pr'])/REEBase.at[k,'Pr']))
        NewTmp.append(math.log((REERaw.at[i,'Nd'])/REEBase.at[k,'Nd']))
        NewTmp.append(math.log((REERaw.at[i,'Sm'])/REEBase.at[k,'Sm']))
        NewTmp.append(math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu']))
        NewTmp.append(math.log((REERaw.at[i,'Gd'])/REEBase.at[k,'Gd']))
        NewTmp.append(math.log((REERaw.at[i,'Tb'])/REEBase.at[k,'Tb']))
        NewTmp.append(math.log((REERaw.at[i,'Dy'])/REEBase.at[k,'Dy']))
        NewTmp.append(math.log((REERaw.at[i,'Ho'])/REEBase.at[k,'Ho']))
        NewTmp.append(math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu']))
        NewTmp.append(math.log((REERaw.at[i,'Tm'])/REEBase.at[k,'Tm']))
        NewTmp.append(math.log((REERaw.at[i,'Yb'])/REEBase.at[k,'Yb']))
        NewTmp.append(math.log((REERaw.at[i,'Lu'])/REEBase.at[k,'Lu']))
       # NewTmp.append(math.log((REERaw.at[i,'Y'])/REEBase.at[k,'Y']))


        DrawLines(X,NewTmp,LineColor= REERaw.at[i,'Color'], LineWidth = REERaw.at[i,'Width'],LineStyle=REERaw.at[i,'Style'],LineAlpha=REERaw.at[i,'Alpha'])

    plt.savefig("Result-REE-Plot.png",dpi=600)
    plt.savefig("Resultt-REE-Plot.svg",dpi=600)
    plt.show()

'''
        Tmp=Line(A,B)        
        
        Tmp.AddPoint(Point(3, math.log((REERaw.at[i,'Pr'])/REEBase.at[k,'Pr'])))
        Tmp.AddPoint(Point(4, math.log((REERaw.at[i,'Nd'])/REEBase.at[k,'Nd'])))
        Tmp.AddPoint(Point(5, math.log((REERaw.at[i,'Sm'])/REEBase.at[k,'Sm'])))
        Tmp.AddPoint(Point(6, math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu'])))
        Tmp.AddPoint(Point(7, math.log((REERaw.at[i,'Gd'])/REEBase.at[k,'Gd'])))
        Tmp.AddPoint(Point(8, math.log((REERaw.at[i,'Tb'])/REEBase.at[k,'Tb'])))
        Tmp.AddPoint(Point(9, math.log((REERaw.at[i,'Dy'])/REEBase.at[k,'Dy'])))
        Tmp.AddPoint(Point(10, math.log((REERaw.at[i,'Ho'])/REEBase.at[k,'Ho'])))
        Tmp.AddPoint(Point(11, math.log((REERaw.at[i,'Eu'])/REEBase.at[k,'Eu'])))
        Tmp.AddPoint(Point(12, math.log((REERaw.at[i,'Tm'])/REEBase.at[k,'Tm'])))
        Tmp.AddPoint(Point(13, math.log((REERaw.at[i,'Yb'])/REEBase.at[k,'Yb'])))
        Tmp.AddPoint(Point(14, math.log((REERaw.at[i,'Lu'])/REEBase.at[k,'Lu'])))
        Tmp.AddPoint(Point(15, math.log((REERaw.at[i,'Y'])/REEBase.at[k,'Y'])))
        
        WholeData.append(Tmp)
'''


    



if __name__ == '__main__':
    REERawData= pd.read_excel("REE.xlsx")
    PlotData(REERawData)







