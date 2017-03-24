# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:55:03 2016

@author: cycleuser
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd



Raw = pd.read_excel("Data.xlsx")

ElementName=[]
ZirconAverage=[]
BulkAverage=[]

for i in range(len(Raw.Elements)):
    ElementName.append(Raw.Elements[i])
    ZirconAverage.append(Raw.ZirconAverage[i])
    BulkAverage.append(Raw.BulkAverage[i])

CEZ = Raw.ZirconAverage[2]
CEB = Raw.BulkAverage[2]



Element3Name="La    Ce	Pr	Nd	Sm	Eu	Gd	Tb	Dy	Ho	Er	Tm	Lu	"
Element3=Element3Name.split()




Element4Name="Th U Ce4 Hf"
Element4=Element4Name.split()


LnDi=[]

for i in range(len(ZirconAverage)):
    LnDi.append(math.log(float(ZirconAverage[i])/float(BulkAverage[i])))


Ri=[]
Ro=[]
RiData="1.16 	1.14 	1.13 	1.11 	1.08 	1.07 	1.05 	1.04 	1.03 	1.02 	1.00 	0.99 	0.98 	0.83 	1.00 	1.06 	0.97 "


TmpRi=RiData.split()
TmpRo=("0.84 "*len(TmpRi)).split()

for a in range(len(TmpRi)):
    Ri.append(float(TmpRi[a]))
    Ro.append(float(TmpRo[a]))
    

TmpX=[]
for i in range(len(Ri)):
    TmpX.append((Ri[i]/3+Ro[i]/6)*(Ri[i]-Ro[i])*(Ri[i]-Ro[i]))

X={}
Y={}

for i in range(len(ElementName)):
    X[ElementName[i]]=TmpX[i]
    Y[ElementName[i]]=LnDi[i]






XE3=[]
YE3=[]

XE4=[]
YE4=[]

CE3=[]
CE4=[]

LineXE3=[]
LineYE3=[]

LineXE4=[]
LineYE4=[]

for i in Element3:
    XE3.append(X[i])
    YE3.append(Y[i])
    
    if(i!='Ce'):
        LineXE3.append(X[i])
        LineYE3.append(Y[i])
    else:
        CE3=[X[i],Y[i]]

for i in Element4:
    XE4.append(X[i])
    YE4.append(Y[i])
    
    if(i!='Ce4'):
        LineXE4.append(X[i])
        LineYE4.append(Y[i])
    else:
        CE4=[X[i],Y[i]]
        
        
        
    
z3 = np.polyfit(LineXE3, LineYE3, 1)
p3 = np.poly1d(z3)
    
z4 = np.polyfit(LineXE4, LineYE4, 1)
p4 = np.poly1d(z4)

x3=np.linspace(min(XE3),max(XE3),30)  
y3=p3(x3)





plt.figure(1)
#plt.figure(figsize=(8,6), dpi=80)
plt.xlim(0,max(XE3)*5/4)
plt.ylim(-10,10)
plt.ylabel(r'$LnD Zircon / Rock %$',fontsize=16)


plt.plot(x3,y3,'r-')  


YforCE3=np.linspace(p3(CE3[0]),CE3[1],30) 
XforCE3=[]

for i in YforCE3:
    XforCE3.append(CE3[0])

plt.plot( XforCE3,YforCE3,'b-')  


PCE3=(CE3[1]-p3(CE3[0]))

PCE4=(CE4[1]-p4(CE4[0]))

a4=np.power(np.e,PCE3)
a3=np.power(np.e,PCE4)


Sight=r"D Ce4 ="+str(a4) +r"   D Ce3 ="+str(a3)

plt.xlabel(Sight,fontsize=16)

plt.subplots_adjust(bottom = 0.1)
plt.scatter(
    XE3,YE3, marker = '^', color='red',
    cmap = plt.get_cmap('Spectral'))
for  Element3, x, y in zip(Element3, XE3,YE3):
    plt.annotate(
        Element3, 
        xy = (x, y), xytext = (10, 25),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
#plt.scatter(XE3,YE3,label='Element3',color='r',marker='^', linewidth=1, linestyle="-",)

plt.figure(2)
#plt.figure(figsize=(8,6), dpi=80)
plt.xlim(0,max(XE4)*5/4)
plt.ylim(-10,10)
plt.ylabel(r'$LnD Zircon / Rock %$',fontsize=16)
plt.subplot(111)

x4=np.linspace(min(XE4),max(XE4),30)  
y4=p4(x4)


plt.plot(x4,y4,'g-') 

YforCE4=np.linspace(p4(CE4[0]),CE4[1],30) 
XforCE4=[]

for i in YforCE4:
    XforCE4.append(CE4[0])

plt.plot( XforCE4,YforCE4,'b-')  

PCE3=(CE3[1]-p3(CE3[0]))

PCE4=(CE4[1]-p4(CE4[0]))



q=0

q= (CEB-(CEZ/a3)) / (CEZ/a4-CEB)

Sight=r"Ce4/Ce3 ="+str(q)




plt.xlabel(Sight,fontsize=16)

plt.scatter(
    XE4,YE4, marker = 'o', color='green',
    cmap = plt.get_cmap('Spectral'))
for  Element4, x, y in zip(Element4, XE4,YE4):
    plt.annotate(
        Element4, 
        xy = (x, y), xytext = (10, 25),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
plt.show()
