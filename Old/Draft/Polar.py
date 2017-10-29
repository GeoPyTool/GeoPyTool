#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 10:41:56 2017

@author: cycleuser
"""


lang = "python"

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
import math
import sys
import csv
from chempy import Substance


import geopython as gp

class Polar(gp.Frame):
    """
    Polar Stereographic projection for structural data
    :param name: the file used to plot
    :type name: a string
    """
    Label = [u'N', u'S', u'W', u'E']
    LabelPosition = []
    name = "Structure.xlsx"

    def __init__(self, name="Structure.xlsx", Label=[u'N', u'S', u'W', u'E']):
        super().__init__()

        self.raw = ''
        
                
        if ("csv" in self.name):
            self.raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            self.raw = pd.read_excel(self.name)

        self.Label = [u'N', u'S', u'W', u'E']
        self.LabelPosition = []
        self.name = "Structure.xlsx"

        self.Label = Label
        self.name = name

    def read(self):
        self.wulf()

        plt.figure(2)
        plt.subplot(111)
        self.schmidt()

    def eqar(self, A):
        return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))

    def eqan(self, A):
        return 90 * np.tan(np.pi * (90. - A) / (2. * 180.))

    def getangular(self, A, B, C):
        a = np.radians(A)
        b = np.radians(B)
        c = np.radians(C)
        result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
        result = np.rad2deg(result)
        return result

    def wulf(self, Width=1, Color='k'):
        """
        read the Excel, then draw the wulf net and Plot points, job done~
        """

        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        Data = []
        Labels = []

        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))

        list1 = [self.eqan(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, 90, 15)]
        plt.rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                         raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]


            Label=raw.at[i, "Label"]
            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""
                
            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size=50

            Setting=[Width,Color,Alpha,Marker,Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size=raw.at[i, "Size"]            
    
            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size=raw.at[i, "Size"]
                
                Setting=[Width,Color,Alpha,Marker,Size]
            r = np.arange(Dip - 90, Dip + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]
            Line = (self.eqan(self.getangular(Dip_Angle, Dip, r)))

            plt.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha, label=Label)

        plt.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name + "Wulff.png", dpi=300)
        plt.savefig(self.name + "Wulff.svg", dpi=300)
        plt.show()

    def schmidt(self, Width=1, Color='k'):
        """
        read the Excel, then draw the schmidt net and Plot points, job done~
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        Data = []
        Labels = []
        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))

        list1 = [self.eqar(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, 90, 15)]
        plt.rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append(
                [raw.at[i, "Name"], raw.at[i, "Dip"], raw.at[i, "Dip-Angle"], raw.at[i, "Color"],
                 raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Marker"], raw.at[i, "Label"]])
            Dip = raw.at[i, "Dip"]
            Dip_Angle = raw.at[i, "Dip-Angle"]

            Label = raw.at[i, "Label"]

            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ""
                
                
            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size=50

            Setting=[Width,Color,Alpha,Marker,Size]

            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Size=raw.at[i, "Size"]            
    
            if (Color not in Setting or Color != ""):
                Width = raw.at[i, "Width"]
                Color = raw.at[i, "Color"]
                Alpha = raw.at[i, "Alpha"]
                Marker = raw.at[i, "Marker"]
                Size=raw.at[i, "Size"]
                
                Setting=[Width,Color,Alpha,Marker,Size]


            plt.scatter(np.radians(90 - Dip), self.eqar(Dip_Angle), marker=Marker, s=Size, color=Color, alpha=Alpha,
                    label=Label, edgecolors='black')
        
        # plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        plt.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name + "Schmidt.png", dpi=300)
        plt.savefig(self.name + "Schmidt.svg", dpi=300)
        plt.show()

    
    
    
    def Trans(self,S=(0,100,110),D=(0,30,40)):
        a=[]
        b=[]
        
        for i in S:
            a.append(np.radians(90 - i))
        for i in D:
            b.append(self.eqar(i))
            
        return(a,b)
        
        
        
        

    def singlerose(self, Gap=10,Width=1,Name=['Dip'], Color=['red']):
        """
        draw the rose map of single sample with different items~
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))
        
        real_max=[]

        for k in range(len(Name)):
            
            
                
            Data = []
            S=[]
            R=[]
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])
    
            
            s= np.linspace(0,360,360/Gap+1)
            t= tuple(s.tolist())
            count=[]
            
            for i in range(len(t)):
                tmp_count=0
                for j in S:
                    if i < len(t)-1:
                        if t[i]<j<=t[i+1]:
                            tmp_count+=1
                count.append(tmp_count)
                
            count_max =max(count)
            real_max.append(count_max)
            
            

            
        maxuse=max(real_max)   
        
        
        
        for k in range(len(Name)):   
            Data = []
            S=[]
            R=[]
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])
    
            
            s= np.linspace(0,360,360/Gap+1)
            t= tuple(s.tolist())
            count=[]
            
            for i in range(len(t)):
                tmp_count=0
                for j in S:
                    if i < len(t)-1:
                        if t[i]<j<=t[i+1]:
                            tmp_count+=1
                count.append(tmp_count)
            s= np.linspace(0,360,360/Gap+1)
            t= tuple(s.tolist())
            
            R_factor = 90/maxuse
            
            for i in count:
                TMP=90- i *R_factor
                R.append(TMP)
                        
            m,n=Polar().Trans(t,R)
            plt.plot(m,n, color=Color[k], linewidth=1, alpha=0.6, marker='')
            plt.fill(m, n, Color=Color[k], Alpha=0.6, )
            
        list1 = [self.eqar(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, int(maxuse+1), int((maxuse+1)/7))]
        list2.reverse()
        plt.rgrids(list1, list2)
            
        
        plt.thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name + "Rose.png", dpi=300)
        plt.savefig(self.name + "Rose.svg", dpi=300)
        plt.show()
        
        
        


    def multirose(self, Gap=10,Width=1,Name='Dip'):
        """
        draw the rose map of multiple samples~
        """

        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)

        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))
        
        real_max=[]

        S=[]
        R=[]
        Color=[]
        Label=[]
        Whole={} 
        
        for i in range(len(self.raw)):
            S.append(self.raw.at[i, Name])
            
            if self.raw.at[i, 'Color'] not in Color and self.raw.at[i, 'Color']  !='':
                Color.append(self.raw.at[i, 'Color'])
            if self.raw.at[i, 'Label'] not in Label and self.raw.at[i, 'Label']  !='':
                Label.append(self.raw.at[i, 'Label'])

        Whole=({k: [] for k in Label})
        
        WholeCount=({k: [] for k in Label})
        
        
        for i in range(len(self.raw)):
            for k in Label:
                if self.raw.at[i, 'Label'] ==k:
                    Whole[k].append(self.raw.at[i, Name])
        

        t= tuple(np.linspace(0,360,360/Gap+1).tolist())
        real_max=0
        
        for j in range(len(Label)):
            
            for i in range(len(t)):
                tmp_count=0
                for u in Whole[Label[j]]:
                    if i < len(t)-1:
                        if t[i]<u<=t[i+1]:
                            tmp_count+=1
                real_max=max(real_max,tmp_count)
                WholeCount[Label[j]].append(tmp_count)
            
            
        maxuse=real_max
        R_factor = 90/maxuse
        
        for j in range(len(Label)):
            
            R=[]
            for i in WholeCount[Label[j]]:
                TMP=90- i *R_factor
                R.append(TMP)
            
            m,n=Polar().Trans(t,R)
            plt.plot(m, n, color=Color[j], linewidth=1, alpha=0.6, marker='',label=Label[j])
            plt.fill(m, n, Color=Color[j], Alpha=0.6)
                    
        

            
        list1 = [self.eqar(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, int(maxuse+1), int((maxuse+1)/7))]
        list2.reverse()
        plt.rgrids(list1, list2)
            
        
        plt.thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name + "MultiRose.png", dpi=300)
        plt.savefig(self.name + "MultiRose.svg", dpi=300)
        plt.show()

if __name__ == '__main__':
    p=Polar()
    p.multirose()
    p.singlerose(Name=['Dip','Strike'], Color=['red','green'])