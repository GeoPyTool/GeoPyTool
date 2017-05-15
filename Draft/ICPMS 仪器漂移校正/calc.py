import pandas as pd
import numpy as np
import math
import codecs



def Whole(position):
    

    df = pd.read_excel("datafile.xlsx")
    df.head()
    t = np.array([])
    allt  = np.array([])
    dt = np.array([])
    matt = np.array([])
    
    
    
    Lable='Unnamed: '+str(position)
    Name= str(df.columns[(position-1)])
    
    EleMent = np.array([])
    dEleMent = np.array([])
    tempValue=0
    
    def Ft(TestData,T,k):
        RealData = np.array([])  
        
        for j in range(len(k)):
            temp=T[0]+T[1]*(math.pow(k[j],1))+T[2]*(math.pow(k[j],2))+T[3]*(math.pow(k[j],3))+T[4]*(math.pow(k[j],4))
            RealData=np.append(RealData,TestData[j]*TestData[0]/temp)
        
        return RealData
    
    
    for i in range(21):
        t  = np.append(t,df.at[i,'采集日期时间'])
        
        
        if(df.at[i,'注释']=="QC"):
            dt = np.append(dt,(float((t[i]-t[0]).total_seconds())))
            dEleMent = np.append(dEleMent,float(df.at[i,Lable]))
        allt = np.append(allt,(float((t[i]-t[0]).total_seconds()))) 
        
        if(df.at[i,Lable]=='<0.000'):
            tempValue=0
        else:
            tempValue=float(df.at[i,Lable])
        EleMent  = np.append(EleMent,tempValue)
    
    
    for i in range(len(dt)):
        matt=np.append(matt,([1,math.pow(dt[i],1),math.pow(dt[i],2),math.pow(dt[i],3),math.pow(dt[i],4)]))
    
    
    NewMatt=np.mat([[matt[0],matt[1],matt[2],matt[3],matt[4]],[matt[5],matt[6],matt[7],matt[8],matt[9]],[matt[10],matt[11],matt[12],matt[13],matt[14]],[matt[15],matt[16],matt[17],matt[18],matt[19]],[matt[20],matt[21],matt[22],matt[23],matt[24]]])
    
    NewMatEleMent=(np.mat(dEleMent)).T
    
    tmp=np.linalg.inv(NewMatt)
    
    SoledMat = np.dot(tmp,NewMatEleMent)
    
    Answer=Ft(EleMent,SoledMat,allt)
    
    

    
    flag=""
    counter=0
    

    

    Str1=str(Name)+"\t,Tested\t,"
    Str2="\t,Real\t,"
    
    returnStr=""
    
    
    for x in range(len(EleMent)-1):
        
        if(df.at[x,'注释']=="QC"):
            flag="QC"
        else:
            counter=counter+1
            flag="Sample"+str(counter)
            
        Str1=Str1+str(EleMent[x])+"\t,"
        Str2=Str2+str(Answer[x])+"\t,"
        
    
    returnStr=Str1+"\r\n"+Str2
    
    
    return(returnStr)
    
    
    

def HeadPart(position):
    df = pd.read_excel("datafile.xlsx")
    df.head()
    t = np.array([])
    allt  = np.array([])
    dt = np.array([])
    
    Lable='Unnamed: '+str(position)
    
    EleMent = np.array([])
    dEleMent = np.array([])
    tempValue=0 
    
    for i in range(21):
        t  = np.append(t,df.at[i,'采集日期时间'])
    
        if(df.at[i,'注释']=="QC"):
            dt = np.append(dt,(float((t[i]-t[0]).total_seconds())))
            dEleMent = np.append(dEleMent,float(df.at[i,Lable]))
        allt = np.append(allt,(float((t[i]-t[0]).total_seconds()))) 
        
        if(df.at[i,Lable]=='<0.000'):
            tempValue=0
        else:
            tempValue=float(df.at[i,Lable])
        EleMent  = np.append(EleMent,tempValue)
    
    StrTime="\t,Time\t,"
    StrType="\t,Type\t,"
    returnStr=""
    flag=""
    counter=0
    
    for x in range(len(EleMent)-1):
        
        if(df.at[x,'注释']=="QC"):
            flag="QC"
        else:
            counter=counter+1
            flag="Sample"+str(counter)   
        
        StrTime=StrTime+str(t[x])+"\t,"
        StrType=StrType+flag+"\t," 

    returnStr=StrTime+"\r\n"+StrType
 
    return(returnStr)



WholeStr=HeadPart(3)

for p in range(69):
    if(p>=1):
        WholeStr=WholeStr+"\r\n"+Whole(2*p+1)

WholeOut = codecs.open("WholeOut.csv", 'w','utf-8')
WholeOut.write(WholeStr)    
    
WholeOut.close()

df = pd.read_csv("WholeOut.csv", header=None, sep=',')
df=df.T
df.to_excel('output.xlsx', sheet_name='Result', index=False)
    