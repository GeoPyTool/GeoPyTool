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

Texts below is cited from this book as an introduction of QAPF-plot:
"QAPF modal classification of volcanic rocks (based on Streckeisen, 1978, Fig. 1). 
The corners of the double triangle are Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid. 
This diagram must not be used for rocks in which the mafic mineral content, M, is greater than 90%."


"""

#You need to install numpy and matplotlib to use this module
#pandas is used to read data from xlsx file
import pandas as pd


#sys is needed to add the files in the path to import
import sys
sys.path.append("./TAS.py")
sys.path.append("./QAPF.py")
sys.path.append("./QFL.py")
sys.path.append("./QmFt.py")
sys.path.append("./REE.py")

sys.path.append("./Drawer.py")

#import the module first and then you can use the functions in it
import TAS
import QAPF
import QFL
import QmFLt
import REE

import Drawer



#You need to put you data in a xlsx file in the same form as the example file
TasRawData = pd.read_excel("TAS.xlsx")
QapfRawData= pd.read_excel("QAPF.xlsx")
QflRawData= pd.read_excel("QFL.xlsx")
REERawData= pd.read_excel("REE.xlsx")
REEBaseData= pd.read_excel("REEBase.xlsx")

#You only need to input the data from the file
TAS.PlotData(TasRawData)
QAPF.PlotData(QapfRawData)
QFL.PlotData(QflRawData)
QmFLt.PlotData(QflRawData)
REE.PlotData(REERawData)

#Then if the data file is in the right form and nothing goes wrong, you will have three files:
#a svg(Scalable Vector Graphics) file which can be modified directly in Adobe Illustrator or Corel Draw,
#a png (Portable Network Graphics) and a more commonly used jpg.

#You can also set the width and color of lines like this:
#TAS.PlotData(TasRawData,0.5,'b')
#They are optional. And the letters for different colors are shown below:
#b: blue
#g: green
#r: red
#c: cyan
#m: magenta
#y: yellow
#k: black
#w: white



'''
F=Foidite
PC=Picro-Basalt
S1=Trachy-Basalt
S2=Basaltic Trachy-Andesite
S3=Tranchyandesite
U1=Tephrite(if ol < 10%) OR Basanite(if ol > 10%)
U2=Phonotephrite
U3=Tephriphonolite
Ph=Phonolite
T=Trachyte(if q < 20%) OR Trachydacite(if q >20%)
B=Basalt
O1=Basaltic Andesite
O2=Andesite
O3=Dacite
R=Rhyolite
'''






