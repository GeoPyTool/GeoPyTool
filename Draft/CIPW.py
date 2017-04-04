
lang = "python"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import sys
import csv
from chempy import Substance

"""
the Class for CIPW calculation

"""


def ToCsv(name='FileName.csv', DataToWrite=[
    ["First", "Second", "Third"], ]):
    #Write DataResult to CSV file
    with open(name, 'w', newline='') as fp:
        a = csv.writer(fp)
        a.writerows(DataToWrite)
           
def Mass(name= 'O'):
    #Mole Mass Calculated by chempy
    return Substance.from_formula(name).mass


def GenList(mylist):    
    for x in mylist:        
        globals()[x] = []

addon= 'Name Author DataType Label Marker Color Size Alpha Style Width TOTAL total LOI loi'

Minerals=["Quartz",
            "Zircon",
            "K2SiO3",
            "Anorthite",
            "Na2SiO3",
            "Acmite",
            "Diopside",
            "Sphene",
            "Hypersthene",
            "Albite",
            "Orthoclase",
            "Wollastonite",
            "Olivine",
            "Perovskite",
            "Nepheline",
            "Leucite",
            "Larnite",
            "Kalsilite",
            "Apatite",
            "Halite",
            "Fluorite",
            "Anhydrite",
            "Thenardite",
            "Pyrite",
            "Magnesiochromite",
            "Chromite",
            "Ilmenite",
            "Calcite",
            "Na2CO3",
            "Corundum",
            "Rutile",
            "Magnetite",
            "Hematite",]

DataWeight={}
DataVolume={}
DataBase={}

DataBase.update({"Quartz":[60.0843,2.65]}) 
DataBase.update({"Zircon":[183.3031,4.56]}) 
DataBase.update({"K2SiO3":[154.2803,2.5]}) 
DataBase.update({"Anorthite":[278.2093,2.76]}) 
DataBase.update({"Na2SiO3":[122.0632,2.4]}) 
DataBase.update({"Acmite":[462.0083,3.6]}) 
DataBase.update({"Diopside":[229.0691997,3.354922069]}) 
DataBase.update({"Sphene":[196.0625,3.5]}) 
DataBase.update({"Hypersthene":[112.9054997,3.507622212]}) 
DataBase.update({"Albite":[524.446,2.62]}) 
DataBase.update({"Orthoclase":[556.6631,2.56]}) 
DataBase.update({"Wollastonite":[116.1637,2.86]}) 
DataBase.update({"Olivine":[165.7266995,3.68429065]}) 
DataBase.update({"Perovskite":[135.9782,4]}) 
DataBase.update({"Nepheline":[284.1088,2.56]}) 
DataBase.update({"Leucite":[436.4945,2.49]}) 
DataBase.update({"Larnite":[172.2431,3.27]}) 
DataBase.update({"Kalsilite":[316.3259,2.6]}) 
DataBase.update({"Apatite":[493.3138,3.2]}) 
DataBase.update({"Halite":[66.44245,2.17]}) 
DataBase.update({"Fluorite":[94.0762,3.18]}) 
DataBase.update({"Anhydrite":[136.1376,2.96]}) 
DataBase.update({"Thenardite":[142.0371,2.68]}) 
DataBase.update({"Pyrite":[135.9664,4.99]}) 
DataBase.update({"Magnesiochromite":[192.2946,4.43]}) 
DataBase.update({"Chromite":[223.8366,5.09]}) 
DataBase.update({"Ilmenite":[151.7452,4.75]}) 
DataBase.update({"Calcite":[100.0892,2.71]}) 
DataBase.update({"Na2CO3":[105.9887,2.53]}) 
DataBase.update({"Corundum":[101.9613,3.98]}) 
DataBase.update({"Rutile":[79.8988,4.2]}) 
DataBase.update({"Magnetite":[231.5386,5.2]}) 
DataBase.update({"Hematite":[159.6922,5.25]}) 

name = "Data.xlsx"


if ("csv" in name):
    raw = pd.read_csv(name)
elif ("xlsx" in name):
    raw = pd.read_excel(name)
    
b=raw.columns
WeightCorrectionFactor=[]
BaseMass={}
Elements=[]
DataMole=[]
DataCalculating ={}
DataResult={}

for i in b:
    if i in addon.split() :
        pass
    else:
        """
        Get the list of Elements
        """
        if i in ['Sr','Ba','Ni']:
            k=i+"O"        
        elif i =='Cr':
            k=i+"2O3"
        elif i =='Zr':
            k=i+"O2"
        else:
            k=i
            
        try:
            m=Mass(k)
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
        """
        Get the Mole Mass of each Element
        """
        
        Elements.append(i)
        BaseMass.update({i:m})

   
for i in range(len(raw)):
    TmpWhole=0
    TmpMole={}
    for j in Elements:
        """
        Get the Whole Mole of the dataset
        """
        if j in ['Sr','Ba','Ni']:
            
            T_TMP=raw.at[i,j]
            TMP = T_TMP/ ( Mass(j)/Mass(j+'O') *10000 )
            
        elif j =='Cr':
            T_TMP=raw.at[i,j]
            TMP = T_TMP/((2*Mass("Cr"))/Mass("Cr2O3")*10000)
            
        elif j =='Zr':
            T_TMP=raw.at[i,j]
            TMP = T_TMP/((2*Mass("Zr"))/Mass("ZrO2")*10000)
            
        else:
            TMP=raw.at[i,j]
            
        V= TMP
        TmpWhole+=V
    
    
    WeightCorrectionFactor.append(100/TmpWhole)


    for j in Elements:
        """
        Get the Mole percentage of each element
        """
        if j in ['Sr','Ba','Ni']:
            
            T_TMP=raw.at[i,j]
            TMP = T_TMP/ ( Mass(j)/Mass(j+'O') *10000 )
            
        elif j =='Cr':
            T_TMP=raw.at[i,j]
            TMP = T_TMP/((2*Mass("Cr"))/Mass("Cr2O3")*10000)

            
        elif j =='Zr':
            T_TMP=raw.at[i,j]
            TMP = T_TMP/((Mass("Zr"))/Mass("ZrO2")*10000)

            
        else:
            TMP=raw.at[i,j]

            
        M= TMP/BaseMass[j] * WeightCorrectionFactor[i]
        # M= TMP/NewMass(j) * WeightCorrectionFactor[i]
        
        TmpMole.update({j:M})
    DataMole.append(TmpMole)            
   
DataCalculating= {k: [] for k in Elements}   

   

"""for i in len(raw):
    k=raw.at[i,'Label']
    DataResult.update({ k: {} } )
"""

for i in range(len(DataMole)):
    k=raw.at[i,'Label']
    DataResult.update({ k: {} } )
    DataWeight.update({ k: {} } )

    DataVolume.update({ k: {} } )
    
    a=DataMole[i]
    for j in list(a):
        DataCalculating[j].append(a[j])
        
    DataCalculating['CaO'][i]+=DataCalculating['Sr'][i]
    DataCalculating['Sr'][i]=0
        
    DataCalculating['K2O'][i]+=2*DataCalculating['Ba'][i]
    DataCalculating['Ba'][i]=0
        
    
    if DataCalculating['CaO'][i]>=10/3*DataCalculating['P2O5'][i]:
        DataCalculating['CaO'][i]-=10/3*DataCalculating['P2O5'][i]
    else:
        DataCalculating['CaO'][i]=0
        
    DataCalculating['P2O5'][i]=DataCalculating['P2O5'][i]/1.5
    
    Apatite=DataCalculating['P2O5'][i]
    
    
    #IF(S19>=T15,S19-T15,0)
    
    if DataCalculating['F'][i]>=DataCalculating['P2O5'][i]:
        DataCalculating['F'][i]-=DataCalculating['P2O5'][i]
    else:
        DataCalculating['F'][i]=0
        
    if DataCalculating['Na2O'][i]>=DataCalculating['Cl'][i]:
        DataCalculating['Na2O'][i]-=DataCalculating['Cl'][i]
    else:
        DataCalculating['Na2O'][i]=0
    
    Halite=DataCalculating['Cl'][i]
    
    #IF(U12>=(U19/2),U12-(U19/2),0)
    if DataCalculating['CaO'][i]>=0.5*DataCalculating['F'][i]:
        DataCalculating['CaO'][i]-=0.5*DataCalculating['F'][i]
    else:
        DataCalculating['CaO'][i]=0
    
    DataCalculating['F'][i]*=0.5
    
    Fluorite=DataCalculating['F'][i]

    #=IF(V17>0,IF(V13>=V17,"Thenardite",IF(V13>0,"Both","Anhydrite")),"None")
    AorT=0
    if DataCalculating['SO3'][i]<=0:
        AorT='None'
    else:
        if DataCalculating['Na2O'][i]>=DataCalculating['SO3'][i]:
            AorT='Thenardite'
        else:
            if DataCalculating['Na2O'][i]>0:
                AorT='Both'
            else:
                AorT='Anhydrite'
        
    #=IF(W26="Anhydrite",V17,IF(W26="Both",V12,0))
    #=IF(W26="Thenardite",V17,IF(W26="Both",V17-W17,0))
    
    if AorT =='Anhydrite':
        DataCalculating['Sr'][i]=0
    elif AorT =='Thenardite':        
        DataCalculating['Sr'][i]=DataCalculating['SO3'][i]
        DataCalculating['SO3'][i]=0 
    elif AorT =='Both':            
        DataCalculating['Sr'][i]=DataCalculating['SO3'][i]-DataCalculating['CaO'][i]            
        DataCalculating['SO3'][i]=DataCalculating['CaO'][i]
    else:
        DataCalculating['SO3'][i]=0
        DataCalculating['Sr'][i]=0
            
    DataCalculating['CaO'][i] -=DataCalculating['SO3'][i] 
    
    DataCalculating['Na2O'][i] -=DataCalculating['Sr'][i] 
    
    
    Anhydrite=DataCalculating['SO3'][i] 
    Thenardite=DataCalculating['Sr'][i] 
    
    Pyrite=0.5*DataCalculating['S'][i]
    
    
    #=IF(W9>=(W18*0.5),W9-(W18*0.5),0)
    
    if DataCalculating['FeO'][i]>=DataCalculating['S'][i]*0.5:
        DataCalculating['FeO'][i]-=DataCalculating['S'][i]*0.5
    else:
        DataCalculating['FeO'][i]=0
        
    #=IF(X24>0,IF(X9>=X24,"Chromite",IF(X9>0,"Both","Magnesiochromite")),"None")

    if DataCalculating['Cr'][i]>0:
        if DataCalculating['FeO'][i]>= DataCalculating['Cr'][i]:
            CorM='Chromite'
        elif DataCalculating['FeO'][i]>0:
            CorM='Both'
        else:
            CorM='Magnesiochromite'
    else:
        CorM='None'
        

        
        
    #=IF(Y26="Chromite",X24,IF(Y26="Both",X9,0))
    #=IF(Y26="Magnesiochromite",X24,IF(Y26="Both",X24-Y24,0))
    
    if CorM=='Chromite':
        DataCalculating['Cr'][i]=DataCalculating['Cr'][i]
        DataCalculating['Ni'][i]=0
        
    elif CorM=='Magnesiochromite':
        DataCalculating['Ni'][i]=DataCalculating['Cr'][i] 
        DataCalculating['Cr'][i]=0
        
    elif CorM=='Both':
        DataCalculating['Ni'][i]=DataCalculating['Cr'][i]-DataCalculating['FeO'][i]
        DataCalculating['Cr'][i]=DataCalculating['FeO'][i]
       
    else:
        DataCalculating['Cr'][i]=0
        DataCalculating['Ni'][i]=0
    


    DataCalculating['MgO'][i]-= DataCalculating['Ni'][i]
        
    Magnesiochromite=DataCalculating['Ni'][i]
    Chromite=DataCalculating['Cr'][i]
            
    #=IF(X9>=Y24,X9-Y24,0)
    
    if DataCalculating['FeO'][i]>= DataCalculating['Cr'][i]:
        DataCalculating['FeO'][i]-=DataCalculating['Cr'][i]
    else:
        DataCalculating['FeO'][i]=0
    
    
    
    
    #=IF(Y6>0,IF(Y9>=Y6,"Ilmenite",IF(Y9>0,"Both","Sphene")),"None")
    
    if DataCalculating['TiO2'][i]<0:
        IorS='None'
    else:
        if DataCalculating['FeO'][i]>= DataCalculating['TiO2'][i]:
            IorS='Ilmenite'
        else:
            if DataCalculating['FeO'][i]>0:
                IorS='Both'
            else:
                IorS='Sphene'
                
    #=IF(Z26="Ilmenite",Y6,IF(Z26="Both",Y9,0))
    #=IF(Z26="Sphene",Y6,IF(Z26="Both",Y6-Z6,0))

    if IorS== 'Ilmenite'    :
        DataCalculating['TiO2'][i]=DataCalculating['TiO2'][i]
        DataCalculating['MnO'][i]=0
        
    elif IorS=='Sphene':        
        DataCalculating['MnO'][i]=DataCalculating['TiO2'][i]
        DataCalculating['TiO2'][i]=0
        
    elif IorS=='Both':
        
        DataCalculating['MnO'][i]=DataCalculating['TiO2'][i]-DataCalculating['FeO'][i]
        DataCalculating['TiO2'][i]=DataCalculating['FeO'][i]
        
    else:
        DataCalculating['TiO2'][i]=0
        DataCalculating['MnO'][i]=0

            
    DataCalculating['FeO'][i]-=DataCalculating['TiO2'][i]
    
    Ilmenite=DataCalculating['TiO2'][i]
    
    #=IF(Z16>0,IF(Z12>=Z16,"Calcite",IF(Z12>0,"Both","Na2CO3")),"None")
    
    
    if  DataCalculating['CO2'][i]<=0:
        CorN='None'
    else:
        if DataCalculating['CaO'][i]>=DataCalculating['CO2'][i]:
            CorN='Calcite'
        else:
            if DataCalculating['CaO'][i]>0:
                CorN='Both'
            else:
                CorN='Na2CO3'
                
                
    
    
    
    #=IF(AA26="Calcite",Z16,IF(AA26="Both",Z12,0))
    
    
    #=IF(AA26="Na2CO3",Z16,IF(AA26="Both",Z16-AA16,0))
    
    if CorN=='None':
        DataCalculating['CO2'][i]=0
        DataCalculating['SO3'][i]=0
        
    elif CorN =='Calcite':        
        DataCalculating['CO2'][i]=DataCalculating['CO2'][i]
        DataCalculating['SO3'][i]=0
        
    elif CorN =='Na2CO3':
        DataCalculating['SO3'][i]=DataCalculating['SO3'][i]
        DataCalculating['CO2'][i]=0
    
    elif CorN =='Both':
        DataCalculating['SO3'][i]= DataCalculating['CO2'][i]-DataCalculating['CaO'][i]
        DataCalculating['CO2'][i]=DataCalculating['CaO'][i]
        
    
    DataCalculating['CaO'][i]-=DataCalculating['CO2'][i]
    
    
    Calcite=DataCalculating['CO2'][i]
    
    Na2CO3=DataCalculating['SO3'][i]
    
    #=IF(AA17>Z13,0,Z13-AA17)
    if DataCalculating['SO3'][i]>DataCalculating['Na2O'][i]:
        DataCalculating['Na2O'][i]=0
    else:
        DataCalculating['Na2O'][i]-=DataCalculating['SO3'][i]
    
    DataCalculating['SiO2'][i]-=DataCalculating['Zr'][i]
    Zircon=DataCalculating['Zr'][i]
    
    #=IF(AB14>0,IF(AB7>=AB14,"Orthoclase",IF(AB7>0,"Both","K2SiO3")),"None")
    
    if DataCalculating['K2O'][i]<=0:
        OorK='None'
    else:
        if DataCalculating['Al2O3'][i]>= DataCalculating['K2O'][i]:
            OorK='Orthoclase'
        else:
            if DataCalculating['Al2O3'][i]>0:
                OorK='Both'
            else:
                OorK ='K2SiO3' 
    
    
    
    #=IF(AC26="Orthoclase",AB14,IF(AC26="Both",AB7,0))
    #=IF(AC26="K2SiO3",AB14,IF(AC26="Both",AB14-AB7,0))
    
    if OorK== 'None':
        DataCalculating['K2O'][i]=0
        DataCalculating['P2O5'][i]=0
        

    elif OorK== 'Orthoclase':
        DataCalculating['K2O'][i]=DataCalculating['K2O'][i]
        DataCalculating['P2O5'][i]=0
    

    elif OorK== 'K2SiO3':
        DataCalculating['P2O5'][i]=DataCalculating['K2O'][i]
        DataCalculating['K2O'][i]=0
    
   

    elif OorK== 'Both':
        
        DataCalculating['P2O5'][i]=DataCalculating['K2O'][i]-DataCalculating['Al2O3'][i]
        DataCalculating['K2O'][i]=DataCalculating['Al2O3'][i]
        
    DataCalculating['Al2O3'][i]-=DataCalculating['K2O'][i]
    
    
    #=IF(AC13>0,IF(AC7>=AC13,"Albite",IF(AC7>0,"Both","Na2SiO3")),"None")
    
    if DataCalculating['Na2O'][i]<=0:
        AorN='None'
    else:
        if DataCalculating['Al2O3'][i]>=DataCalculating['Na2O'][i]:
            AorN='Albite'
        else:
            if DataCalculating['Al2O3'][i]>0:
                AorN='Both'
            else:
                AorN='Na2SiO3'
                
                
    #=IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)
    
    if DataCalculating['Al2O3'][i]>=DataCalculating['Na2O'][i] and DataCalculating['Al2O3'][i]>0:
        DataCalculating['Al2O3'][i]-=DataCalculating['Na2O'][i]
    else:
        DataCalculating['Al2O3'][i]=0
    
    
    #=IF(AD26="Albite",AC13,IF(AD26="Both",AC7,0))
    #=IF(AD26="Na2SiO3",AC13,IF(AD26="Both",AC13-AD13,0))

        
    if AorN =='Albite':
        DataCalculating['Cl'][i]=0
        
    elif AorN=='Both':
        DataCalculating['Cl'][i]=DataCalculating['Na2O'][i]-DataCalculating['Al2O3'][i]
        DataCalculating['Na2O'][i]=DataCalculating['Al2O3'][i]
            
    elif AorN =='Na2SiO3':        
        DataCalculating['Cl'][i]=DataCalculating['Na2O'][i]
        DataCalculating['Na2O'][i]=0
            
    elif AorN =='None':
        DataCalculating['Na2O'][i]=0
        DataCalculating['Cl'][i]=0
    
    
    #=IF(AD7>0,IF(AD12>0,"Anorthite","None"),"None")
    
    """
    Seem like should be =IF(AD7>0,IF(AD12>AD7,"Anorthite","Corundum"),"None")
    
    If Al2O3 is left after alloting orthoclase and albite, then:
    Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
    If Al2O3 exceeds CaO in the preceding calculation, then:
    Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
    Corundum = Al2O3, CaO =0, Al2O3 = 0
    
    
        if DataCalculating['Al2O3'][i]<=0:
            AorC='None'
        else:
            if DataCalculating['CaO'][i]>DataCalculating['Al2O3'][i]:
                AorC= 'Anorthite'
            else:
                Aorc='Corundum'
        
    """       
    
    if DataCalculating['Al2O3'][i]<=0:
        AorC='None'
    else:
        if DataCalculating['CaO'][i]>0:
            AorC= 'Anorthite'
        else:
            Aorc='None'
            
            
    #=IF(AE26="Anorthite",IF(AD12>AD7,0,AD7-AD12),AD7)
 
    #=IF(AE26="Anorthite",IF(AD7>AD12,0,AD12-AD7),AD12)
        
    #=IF(AE26="Anorthite",IF(AD7>AD12,AD12,AD7),0)
    
    if AorC== 'Anorthite':
        if DataCalculating['Al2O3'][i]>=DataCalculating['CaO'][i]:            
            DataCalculating['Sr'][i] = DataCalculating['CaO'][i]            
            DataCalculating['Al2O3'][i]-=DataCalculating['CaO'][i]
            DataCalculating['CaO'][i]=0
            
        else:            
            DataCalculating['Sr'][i]=DataCalculating['Al2O3'][i]            
            DataCalculating['CaO'][i]-=DataCalculating['Al2O3'][i]
            DataCalculating['Al2O3'][i]=0
            
    else:
        DataCalculating['Sr'][i]=0
        
    Corundum=DataCalculating['Al2O3'][i]
    Anorthite=DataCalculating['Sr'][i]
    
    #=IF(AE10>0,IF(AE12>=AE10,"Sphene",IF(AE12>0,"Both","Rutile")),"None")
    
    if DataCalculating['MnO'][i]<=0:
        SorR='None'
    else:
        if DataCalculating['CaO'][i]>=DataCalculating['MnO'][i]:
            SorR='Sphene'
        elif DataCalculating['CaO'][i]>0:
            SorR='Both'
        else:
            SorR='Rutile'
            
            
    #=IF(AF26="Sphene",AE10,IF(AF26="Both",AE12,0))
    
    #=IF(AF26="Rutile",AE10,IF(AF26="Both",AE10-AE12,0))
    
    if SorR=='Sphene':
        DataCalculating['MnO'][i]=DataCalculating['MnO'][i]
        DataCalculating['S'][i]=0
    
    elif SorR=='Rutile':
        DataCalculating['S'][i]=DataCalculating['MnO'][i]
        DataCalculating['MnO'][i]=0
        
        
    elif SorR=='Both':
        DataCalculating['S'][i]=DataCalculating['MnO'][i]-DataCalculating['CaO'][i]
        DataCalculating['MnO'][i]=DataCalculating['CaO'][i]
    
    elif SorR=='None':     
        DataCalculating['MnO'][i]=0
        DataCalculating['S'][i]=0
    
    DataCalculating['CaO'][i]-=DataCalculating['MnO'][i]
      
    
    
    Rutile=DataCalculating['S'][i]
    
    #=IF(AND(AF20>0),IF(AF8>=AF20,"Acmite",IF(AF8>0,"Both","Na2SiO3")),"None")
    
    if DataCalculating['Cl'][i]<=0:
        ACorN='None'
    else:
        if DataCalculating['Fe2O3'][i]>=DataCalculating['Cl'][i]:
            ACorN='Acmite'
        else:
            if DataCalculating['Fe2O3'][i]>0:
                ACorN='Both'
            else:
                ACorN='Na2SiO3'
                
                
    #=IF(AG26="Acmite",AF20,IF(AG26="Both",AF8,0))
    
    
    #=IF(AG26="Na2SiO3",AF20,IF(AG26="Both",AF20-AG19,0))
    
    if ACorN=='Acmite':
        DataCalculating['F'][i]=DataCalculating['Cl'][i]
        DataCalculating['Cl'][i]=0 
        
    elif ACorN =='Na2SiO3':
        DataCalculating['Cl'][i]=DataCalculating['Cl'][i]   
        DataCalculating['F'][i]=0 
        
    elif ACorN=='Both':
        DataCalculating['F'][i]=DataCalculating['Fe2O3'][i]
        DataCalculating['Cl'][i]=DataCalculating['Cl'][i]-DataCalculating['F'][i]        

    elif ACorN=='None':
        DataCalculating['F'][i]=0
        DataCalculating['Cl'][i]=0
    
    
    DataCalculating['Fe2O3'][i]-=DataCalculating['F'][i]
    
    Acmite=DataCalculating['F'][i]
    
    #=IF(AG8>0,IF(AG9>=AG8,"Magnetite",IF(AG9>0,"Both","Hematite")),"None")
    
    
    if DataCalculating['Fe2O3'][i]<=0:
        MorH='None'
    else:
        if DataCalculating['FeO'][i]>=DataCalculating['Fe2O3'][i]:
            MorH='Magnetite'
        else:
            if DataCalculating['FeO'][i]>0:
                MorH='Both'
            else:
                MorH='Hematite'
    
    
    
    #=IF(AH26="Magnetite",AG8,IF(AH26="Both",AG9,0))
    #=IF(AH26="Hematite",AG8,IF(AH26="Both",AG8-AG9,0))
    
    
    
    if MorH=='Magnetite':
        DataCalculating['Fe2O3'][i]=DataCalculating['Fe2O3'][i]
        DataCalculating['Ba'][i]=0
    
    elif MorH== 'Hematite':
        DataCalculating['Fe2O3'][i]=0
        DataCalculating['Ba'][i]=DataCalculating['FeO'][i]
    
    
    elif MorH=='Both':
        DataCalculating['Fe2O3'][i]=DataCalculating['FeO'][i]
        DataCalculating['Ba'][i]= DataCalculating['Fe2O3'][i]-DataCalculating['FeO'][i]
    
    
    elif MorH=='None':
        DataCalculating['Fe2O3'][i]=0
        DataCalculating['Ba'][i]==0
        
        
    DataCalculating['FeO'][i]-=DataCalculating['Fe2O3'][i]
    

    Magnetite=DataCalculating['Fe2O3'][i]
    Hematite=DataCalculating['Ba'][i]
    
    DataCalculating['FeO'][i]+=DataCalculating['MgO'][i]
    
    DataCalculating['MgO'][i]=0
    
    #=IF(AI12>0,IF(AI9>=AI12,"Diopside",IF(AI9>0,"Both","Wollastonite")),"None")
    
    
    if DataCalculating['CaO'][i]<=0:
        DorW='None'
    else:
        if DataCalculating['FeO'][i]>=DataCalculating['CaO'][i]:
            DorW='Diopside'
        else:
            if DataCalculating['FeO'][i]>0:
                DorW='Both'
            else:
                DorW='Wollastonite'    
    
    
    #=IF(AJ26="Diopside",AI12,IF(AJ26="Both",AI9,0))    
    
    #=IF(AJ26="Wollastonite",AI12,IF(AJ26="Both",AI12-AI9,0))
       
    
    
    if DorW =='Diopside':
        DataCalculating['CaO'][i]=DataCalculating['CaO'][i]
        DataCalculating['S'][i]=0
    
    elif DorW =='Wollastonite':
        DataCalculating['S'][i]=DataCalculating['CaO'][i]
        DataCalculating['CaO'][i]=0
    
    elif DorW =='Both':
        DataCalculating['S'][i]=DataCalculating['CaO'][i]-DataCalculating['FeO'][i]
        DataCalculating['CaO'][i]=DataCalculating['FeO'][i]
    
    elif DorW =='None':
        DataCalculating['CaO'][i]=0
        DataCalculating['S'][i]=0
    
    DataCalculating['FeO'][i]-=DataCalculating['CaO'][i]
    

    Diopside=DataCalculating['CaO'][i]
    
    Quartz=DataCalculating['SiO2'][i]
    
    Zircon= DataCalculating['Zr'][i]
    K2SiO3= DataCalculating['P2O5'][i]   
        
    Na2SiO3=DataCalculating['Cl'][i]
    
    Sphene= DataCalculating['MnO'][i]
    
    Hypersthene= DataCalculating['FeO'][i]
        
    Albite= DataCalculating['Na2O'][i]
    
    Orthoclase= DataCalculating['K2O'][i]
        
    Wollastonite = DataCalculating['S'][i]
        
    #=AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)
    
    Quartz-=(Zircon+
            K2SiO3+
            Anorthite*2+
            Na2SiO3+
            Acmite*4+
            Diopside*2+
            Sphene+
            Hypersthene+
            Albite*6+
            Orthoclase*6+
            Wollastonite)
        
    #=IF(AL5>0,AL5,0)   
    
    if Quartz>0:
        Quartz=Quartz
    else:Quartz=0


    #=IF(AL13>0,IF(AL5>=0,"Hypersthene",IF(AL13+(2*AL5)>0,"Both","Olivine")),"None")
    
    if Hypersthene<=0:
        HorO='None'
    else:
        if Quartz>=0:
            HorO='Hypersthene'
        else:
            if Hypersthene+2*Quartz>0:
                HorO='Both'
            else:
                HorO='Olivine'
                
    
    
   
    
    #=IF(AN26="Hypersthene",AL13,IF(AN26="Both",AL13+(2*AL5),0))
    #=IF(AN26="Olivine",AL13*0.5,IF(AN26="Both",ABS(AL5),0))
    Old_Hypersthene=Hypersthene
    if HorO=='Hypersthene':
        Hypersthene=Hypersthene
        Olivine=0
        
    elif HorO=='Both':
        Hypersthene=Hypersthene+Quartz*2
        Olivine=abs(Quartz)
        
    elif HorO=='Olivine':
        Olivine=Hypersthene/2
        Hypersthene=0
        
    elif HorO=='None':
        Hypersthene=0
        Olivine=0
    
    
    #=AL5+AL13-(AN13+AN17)
    Quartz+= Old_Hypersthene-(Hypersthene+Olivine)
    
    
    #=IF(AL12>0,IF(AN5>=0,"Sphene",IF(AL12+AN5>0,"Both","Perovskite")),"None")
    
    if Sphene<=0:
        SorP='None'
    else:
        if Quartz>=0:
            SorP='Sphene'
        else:
            if Sphene+Quartz>0:
                SorP='Both'
            else:
                SorP='Perovskite'
                
    
    #=IF(AO26="Sphene",AL12,IF(AO26="Both",AL12+AN5,0))
    #=IF(AO26="Perovskite",AL12,IF(AO26="Both",AL12-AO12,0))
    
    Old_Sphene=Sphene
    
    if SorP=='Sphene':
        Sphene=Sphene
        Perovskite=0
        
    elif SorP=='Perovskite' :        
        Perovskite=Sphene
        Sphene=0        
        
    elif SorP=='Both' :
        Sphene+=Quartz        
        Perovskite=Old_Sphene-Sphene    
    
    elif SorP=='None' :
        Sphene=0
        Perovskite=0
        
    Quartz+=Old_Sphene-Sphene  
    
    
    #=IF(AL14>0,IF(AO5>=0,"Albite",IF(AL14+(AO5/4)>0,"Both","Nepheline")),"None")
    
    
    if Albite<=0:
        AlorNe='None'
    else:
        if Quartz>=0:
            AlorNe='Albite'
        else:
            if Albite+(Quartz/4)>0:
                AlorNe='Both'
            else:
                AlorNe='Nepheline'
                
    #=AO5+(6*AL14)-(AP14*6)-(AP19*2)
    
    
    #=IF(AP26="Albite",AL14,IF(AP26="Both",AL14+(AO5/4),0))
    #=IF(AP26="Nepheline",AL14,IF(AP26="Both",AL14-AP14,0))
    
    
    Old_Albite=Albite
    
    if AlorNe=='Albite':
        Albite=Albite
        Nepheline=0
        
    elif AlorNe=='Nepheline':
        Nepheline=Albite
        Albite=0
    
    elif AlorNe=='Both':
        Albite+=Quartz/4
        Nepheline=Old_Albite-Albite
    
    elif AlorNe=='None':
        Nepheline=0
        Albite=0
    
    
    Quartz+=(6*Old_Albite)-(Albite*6)-(Nepheline*2)

    
    
    #=IF(AL15>0,IF(AP5>=0,"Orthoclase",IF(AL15+(AP5/2)>0,"Both","Leucite")),"None")
    
    if Orthoclase<=0:
        OorL='None'
    else:
        if Quartz>=0:
            OorL='Orthoclase'
        else:
            if Orthoclase+Quartz/2>0:
                OorL='Both'
            else:
                OorL='Leucite'
   
    #=IF(AQ26="Orthoclase",AL15,IF(AQ26="Both",AL15+(AP5/2),0))             
    #=IF(AQ26="Leucite",AL15,IF(AQ26="Both",AL15-AQ15,0))

    Old_Orthoclase=Orthoclase
    
    if OorL =='Orthoclase':
        Orthoclase=Orthoclase
        Leucite=0
    
    elif OorL =='Leucite':
        Leucite=Orthoclase
        Orthoclase=0
    
    elif OorL =='Both':
        Orthoclase+=Quartz/2
        Leucite=Old_Orthoclase-Orthoclase
        
    elif OorL =='None':
        Orthoclase=0
        Leucite=0
                
    
    #=AP5+(AL15*6)-(AQ15*6)-(AQ20*4)
    
    Quartz+=(Old_Orthoclase*6)-(Orthoclase*6)-(Leucite*4)
    
    
    
    #=IF(AL16>0,IF(AQ5>=0,"Wollastonite",IF(AL16+(AQ5*2)>0,"Both","Larnite")),"None")
    if Wollastonite<=0:
        WorB='None'
    else:
        if Quartz>=0:
            WorB='Wollastonite'
        else:
            if Wollastonite + Quartz/2 >0:
                WorB='Both'
            else:
                WorB='Larnite'
                
                
    #=IF(AR26="Wollastonite",AL16,IF(AR26="Both",AL16+(2*AQ5),0))
    #=IF(AR26="Larnite",AL16/2,IF(AR26="Both",(AL16-AR16)/2,0))
    
    Old_Wollastonite=Wollastonite
    if WorB=='Wollastonite':
        Wollastonite=Wollastonite
        Larnite=0
    
    elif WorB=='Larnite':
        Larnite=Wollastonite/2
        Wollastonite=0
    
    elif WorB=='Both':
        Wollastonite+=Quartz*2
        Larnite=(Old_Wollastonite-Wollastonite)/2
    
    elif WorB=='None':
        Wollastonite=0
        Larnite=0
    

    #=AQ5+AL16-AR16-AR21
    Quartz+=Old_Wollastonite-Wollastonite-Larnite
    
    #=IF(AL11>0,IF(AR5>=0,"Diopside",IF(AL11+AR5>0,"Both","LarniteOlivine")),"None")
    
    if Diopside<=0:
        DorL='None'
    else:
        if Quartz>=0:
            DorL='Diopside'
        else:
            if Diopside+Quartz>0:
                DorL='Both'
            else:
                DorL='LarniteOlivine'
    
    
    
    #=IF(AS26="Diopside",AL11,IF(AS26="Both",AL11+AR5,0))
    #=(IF(AS26="LarniteOlivine",AL11/2,IF(AS26="Both",(AL11-AS11)/2,0)))+AN17
    #=(IF(AS26="LarniteOlivine",AL11/2,IF(AS26="Both",(AL11-AS11)/2,0)))+AR21
    
    Old_Diopside=Diopside
    Old_Larnite=Larnite
    Old_Olivine=Olivine
    if DorL=='Diopside':
        Diopside=Diopside
      
    
    
    elif DorL=='LarniteOlivine':
        Larnite+=Diopside/2
        Olivine+=Diopside/2 
        Diopside=0
    
    elif DorL=='Both':
        Diopside+=Quartz
        Larnite+=Old_Diopside-Diopside
        Olivine+=Old_Diopside-Diopside
        
    
    
    elif DorL=='None':
        Diopside=0      
    
    #=AR5+(AL11*2)+AN17+AR21-AS21-(AS11*2)-AS17
    Quartz+=(Old_Diopside*2)+Old_Olivine+Old_Larnite-Larnite-(Diopside*2)-Olivine
    
    
    #=IF(AQ20>0,IF(AS5>=0,"Leucite",IF(AQ20+(AS5/2)>0,"Both","Kalsilite")),"None")
    
    if Leucite<=0:
        LorK='None'
    else:
        if Quartz>=0:
            LorK='Leucite'
        else:
            if Leucite+Quartz/2>0:
                LorK='Both'
            else:
                LorK='Kalsilite'
                
                
    
    #=IF(AT26="Leucite",AQ20,IF(AT26="Both",AQ20+(AS5/2),0))
    #=IF(AT26="Kalsilite",AQ20,IF(AT26="Both",AQ20-AT20,0))
    
    
    Old_Leucite=Leucite
    
    if LorK=='Leucite':
        Leucite=Leucite
        Kalsilite=0
        
    elif LorK=='Kalsilite':
        Kalsilite=Leucite
        Leucite=0
                
    elif LorK=='Both':
        Leucite+=Quartz/2
        Kalsilite=Old_Leucite-Leucite        
        
    elif LorK=='None':
        Leucite=0
        Kalsilite=0
    
    
    #=AS5+(AQ20*4)-(AT20*4)-(AT22*2)
    Quartz+=Old_Leucite*4-Leucite*4-Kalsilite*2

 
    for i in Minerals:        
        exec('DataResult[k].update({\"'+i+'\":'+i+'}) ')
        exec('DataWeight[k].update({\"'+i+'\":'+i+'*DataBase[\"'+i+'\"][0]}) ')        
        exec('DataVolume[k].update({\"'+i+'\":'+i+'*DataBase[\"'+i+'\"][0]/DataBase[\"'+i+'\"][1]}) ')

def WriteData(target='DataResult'):
    DataToWrite=[]
    TMP_DataToWrite=['Samples']
    for j in Minerals:
        TMP_DataToWrite.append(str(j))
    DataToWrite.append(TMP_DataToWrite)
    for i in range(len(DataMole)):
        TMP_DataToWrite=[]
        k=raw.at[i,'Label']
        TMP_DataToWrite=[k]
        for j in Minerals:
            command='TMP_DataToWrite.append(str('+target+'[k][j]))'
            exec(command)        
        DataToWrite.append(TMP_DataToWrite)    
    ToCsv(name= name[0:-5]+'_'+target[4:]+'_CIPW.csv', DataToWrite=DataToWrite)
    

WriteData(target='DataResult')
WriteData(target='DataWeight')
WriteData(target='DataVolume')