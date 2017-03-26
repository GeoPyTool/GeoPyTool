# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:55:03 2016

@author: cycleuser
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
import pandas as pd
import geopython as gp



name= "Ballard.xlsx"
raw = pd.read_excel("Ballard.xlsx")

a = raw.index.values.tolist()
b = raw.columns.values.tolist()

m=raw.at[a[2],b[1]]

Elements=[]
Elements3=[]
UnUsedElements3=[]
Elements4=[]
E3=[]
UnUsedE3=[]
E4=[]

Sample=[]
Rock=[]

x3=[]
y3=[]

UnUsedx3=[]
UnUsedy3=[]

x4=[]
y4=[]

Ce3=[]
Ce4=[]

RockCe=R=raw.at['Rock','Ce']  

names=['Nd','Sm','Gd','Tb','Dy','Ho','Er','Yb','Lu']

for i in b:
    if i != 'Label' and i != 'Eu(II)'and i != 'Ce'and i != 'Ce(+4)':
        Elements.append(i)

        Ri=raw.at['Ri',i]
        Ro=raw.at['Ro',i]
        X=(Ri/3+Ro/6)*(Ri-Ro)*(Ri-Ro)
                
        S=raw.at['Sample',i]
        R=raw.at['Rock',i]        
        
        Sample.append(S)
        Rock.append(R)
        Y=np.log(S/R)              
        
        if raw.at['valence',i]==3 and raw.at['use',i]=='yes':
            Elements3.append(i)
            E3.append([i,S,R])
            x3.append(X)
            y3.append(Y)
            
        elif raw.at['valence',i]==3 and raw.at['use',i]=='no':
            UnUsedElements3.append(i)
            UnUsedE3.append([i,S,R])
            UnUsedx3.append(X)
            UnUsedy3.append(Y)
            
        elif raw.at['valence',i]==4 and raw.at['use',i]=='yes':

            Elements4.append(i)
            E3.append([i,S,R])            
            x4.append(X)
            y4.append(Y)
            
            
    elif i == 'Ce':
        Ri=raw.at['Ri',i]
        Ro=raw.at['Ro',i]
        X=(Ri/3+Ro/6)*(Ri-Ro)*(Ri-Ro)
                
        S=raw.at['Sample',i]
        R=raw.at['Rock',i]        
        
        Sample.append(S)
        Rock.append(R)
        Y=np.log(S/R)   
        Ce3=[X,Y]
        
        
        
    elif i == 'Ce(+4)':
        Ri=raw.at['Ri',i]
        Ro=raw.at['Ro',i]
        X=(Ri/3+Ro/6)*(Ri-Ro)*(Ri-Ro)
                
        S=raw.at['Sample',i]
        R=raw.at['Rock',i]        
        
        Sample.append(S)
        Rock.append(R)
        Y=np.log(S/R)   
        Ce4=[X,Y]
                    
z3 = np.polyfit(x3,y3, 1)
p3 = np.poly1d(z3)


r23 = r2_score(y3, p3(x3))

Xline3= np.linspace(min(x3),max(UnUsedx3),30)   
Yline3= p3(Xline3)          


Ce3test=str( np.power(np.e, p3(Ce3[0])+np.log(RockCe) )) 
DCe3test=str( np.power(np.e, p3(Ce3[0]) )) 

xlabel3="ZirconData is "+str(Ce3[1])+"\n Testdata is"+str( p3(Ce3[0]) )+"\n  R2 is "+str(r23)+"\n  est'd Ce(III) (ppm)="+Ce3test+"\n  est'd DCe(III)(Zir/Met) (ppm)="+DCe3test

plt.xlabel(xlabel3,fontsize=12)

   
plt.ylabel(r'Ln D $Zircon/Rock%$',fontsize=12) 
plt.plot(Xline3,Yline3,'r-')  

gp.Point(Ce3[0],p3(Ce3[0]),Label='',Color='red').show()   
plt.annotate("Ce3 Calculated", xy = (Ce3[0],p3(Ce3[0])), xytext = (10, -25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))  
   

gp.Point(Ce3[0],Ce3[1],Label='',Color='red').show()
plt.annotate("Ce3 Zircon", xy = (Ce3[0],Ce3[1]), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))     



gp.Line(Points=[(Ce3[0],Ce3[1]),(Ce3[0], p3(Ce3[0]))],Style='--',Color='red',Alpha=0.5).show() 

for i in range(len(x3)):           
    gp.Point(x3[i],y3[i],Label='',Color='red').show()
    plt.annotate(Elements3[i], xy = (x3[i],y3[i]), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

for i in range(len(UnUsedx3)):           
    gp.Point(UnUsedx3[i],UnUsedy3[i],Label='',Color='red').show()
    plt.annotate(UnUsedElements3[i], xy = (UnUsedx3[i],UnUsedy3[i]), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))



plt.figure(2)

plt.ylabel(r'Ln D $Zircon/Rock%$',fontsize=12)
plt.subplot(111)


z4 = np.polyfit(x4, y4, 1)
p4 = np.poly1d(z4)           

r24 = r2_score(y4, p4(x4))

Xline4= np.linspace(min(x4),max(x4),30)   
Yline4= p4(Xline4)

plt.plot(Xline4,Yline4,'b-')  
Ce4test=str(p4(Ce4[0]))  


xlabel4="ZirconData is "+str(Ce4[1])+"\n  Testdata is"+Ce4test+"\n  "




Ce4test=str( np.power(np.e, p4(Ce4[0])+np.log(RockCe) )) 
DCe4test=str( np.power(np.e, p4(Ce4[0]) )) 

xlabel4="ZirconData is "+str(Ce4[1])+"\n Testdata is"+str( p4(Ce4[0]) )+"\n  R2 is "+str(r24)+"\n  est'd Ce(IV) (ppm)="+Ce4test+"\n  est'd DCe(IV)(Zir/Met) (ppm)="+DCe4test


plt.xlabel(xlabel4,fontsize=12)  

gp.Point(Ce4[0],p4(Ce4[0]),Label='',Color='red').show()   
plt.annotate("Ce4 Calculated", xy = (Ce4[0],p4(Ce4[0])), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')) 

gp.Point(Ce4[0],Ce4[1],Label='',Color='red').show()
plt.annotate("Ce4 Zircon", xy = (Ce4[0],Ce4[1]), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))  


gp.Line(Points=[(Ce4[0],Ce4[1]),(Ce4[0], p4(Ce4[0]))],Style='--',Color='blue',Alpha=0.5).show()    

for i in range(len(x4)):
    gp.Point(x4[i],y4[i],Label='',Color='blue').show()
    plt.annotate(Elements4[i], xy = (x4[i],y4[i]), xytext = (10, 25), textcoords = 'offset points', ha = 'right', va = 'bottom',
                    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3),
                    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
plt.savefig(self.name+"zircon-Ce.png", dpi=300, bbox_inches='tight')
plt.savefig(self.name+"zircon-Ce.svg", dpi=300, bbox_inches='tight')
plt.show()