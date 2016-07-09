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

This file is a module of TAS-plot for volcanic rocks.
All data used in this module are from the book 
"Igneous Rocks_ a Classification and Glossary of Terms"
 by  R.W. Le Maitre & International Union of Geological Sciences 2002
Texts below is cited from this book as an introduction of TAS-plot:
"The TAS (Total Alkali – Silica) classification should be used only if:
(1) the rock is considered to be volcanic
(2) a mineral mode cannot be determined, owing either to the presence of glass or to the fine-grained nature of the rock
(3) a chemical analysis of the rock is available."



"""
#!/usr/bin/env python

# coding=utf-8

lang = "python"



#You need to install numpy and matplotlib to use this module
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def DrawTasFrameLines(LineWidth=1,LineColor='k'):    
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


def DrawLines(X=[0,1],Y=[0,1],LineWidth=1,LineColor='k',LineStyle="-",):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,)
    


if __name__ == '__main__':
    Width=1
    Color="Blue"
    x=[41,45,48.4,49.4,52,52.5,53,57,57.6,63,69]
    y=[3,5,5.9,7,7.3,8,9.3,9.4,11.5,11.7,14]
    DrawTheLines(x,y,Width,Color)

