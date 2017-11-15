import os 
import pandas as pd
import sys

def Del(name='test.txt',num=3):
    lines = open(name,'r',encoding='windows-1252').readlines()
    open('new'+name, 'w',encoding='utf-8').writelines(lines[num:-1])



a=os.listdir()



for i in a:
    
    if 'csv' in i and 'new' not in i:
        Del(name=i,num=3)
        
        


b=[]
for i in a:
    if 'csv' in i:
        b.append(pd.read_csv('new'+i))


result = pd.concat(b)

result.to_csv('result.csv', sep=',', encoding='utf-8')


