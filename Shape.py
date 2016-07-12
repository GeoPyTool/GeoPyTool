# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 14:14:08 2016

@author: cycleuser
"""
import math
import scipy
import numpy as ny
import pandas as pd
import matplotlib as plt


#sys is needed to add the files in the path to import
import sys
sys.path.append("./TAS.py")
sys.path.append("./QAPF.py")
sys.path.append("./QFL.py")
sys.path.append("./QmFt.py")
sys.path.append("./Drawer.py")

#import the module first and then you can use the functions in it
import TAS
import QAPF
import QFL
import QmFLt

import Drawer


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
     
             
    
    
if __name__ == '__main__':
    Width=1
    Color="Blue"


 