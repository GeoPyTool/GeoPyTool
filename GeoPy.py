# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:37:33 2016

@author: cycleuser
@email: cycleuser@cycleuser.org

Copyright 2016 cycleuser

GeoPython is a set of free softwares for geology related daily work: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
GeoPython is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with GeoPython. If not, see http://www.gnu.org/licenses/.


"""
#!/usr/bin/env python

# coding=utf-8

lang = "python"



#You need to install numpy and matplotlib to use this module
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

#import sys
#sys.path.append("./TAS.py")
#sys.path.append("./QAPF.py")
#sys.path.append("./QFL.py")
#sys.path.append("./QmFt.py")
#sys.path.append("./Drawer.py")




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

def DrawTasFrame(LineWidth=1,LineColor='k'):    
#This DrawTasFrameLines function is used to draw the lines in the Frame of TAS figure
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



def DrawQFLline(LineWidth=1,LineColor='k',LineStyle="--"):
    XSpecialLon=[[51.5,15],
                 [27.5,87.5]
                ]
    YSpecialLon=[[48.5*math.sqrt(3),0],
                 [27.5*math.sqrt(3),12.5*math.sqrt(3)]          
                ]
    for i in range(len(XSpecialLon)):
        DrawLines(XSpecialLon[i],YSpecialLon[i],LineWidth,LineColor,LineStyle="-",)     
    
    
    
    LineMid=CrossPoint(13/2,13/2*math.sqrt(3),100-37/2,37/2*math.sqrt(3),55/2,55/2*math.sqrt(3),100-25/2,25/2*math.sqrt(3))    
    LineLeft=CrossPoint(15,0,51.5,48.5*math.sqrt(3),13/2,13/2*math.sqrt(3),100-37/2,37/2*math.sqrt(3))    
    
    
    XMid=[[LineMid[0],LineLeft[0]],
          [LineMid[0],100-37/2],
          [50,87.5],
         ]
    YMid=[[LineMid[1],LineLeft[1]]  ,
          [LineMid[1],37/2*math.sqrt(3)] ,
          [0,12.5*math.sqrt(3)]          
         ]
    for i in range(len(XMid)):
        DrawLines(XMid[i],YMid[i],LineWidth,LineColor,LineStyle="--")       

    
def DrawTriangle(LineWidth=1,LineColor='k',Label=[u'Q',u'F',u'L'],Position=[(48,50*math.sqrt(3)+2),(-6,-1),(104,-1)]):
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


    DrawLines(XBorder,YBorder,LineWidth,LineColor)
    Sign(Label,Position)


def Sign(What=[u'Q',u'F',u'L'],Where=[(48,50*math.sqrt(3)+2), (-6,-1), (104,-1)]):
    #Label are the names of different kinds of rocks
    Label=What

#LabelPosition are the positions of those Labels
    LabelPosition =Where

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i],xy=(LabelPosition[i]), xycoords='data',xytext=(0,0), textcoords='offset points', fontsize=16,)
    


    

if __name__ == '__main__':
    Width=1
    Color="Blue"
    x=[41,45,48.4,49.4,52,52.5,53,57,57.6,63,69]
    y=[3,5,5.9,7,7.3,8,9.3,9.4,11.5,11.7,14]
    plt.scatter(1,2,marker='o')
    DrawLines(x,y,Width,Color)
    DrawTriangle()
    DrawQFLline()
