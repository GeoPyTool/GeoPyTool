#GeoPython, a set of free softwares for geology related daily work
#####author: cycleuser
#####email: cycleuser@cycleuser.org

##Introduction
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



##Dependence
This module is written with Python3.4 and based on numpy, matplotlib and pandas. That means you need to install them.

You can install these packages with PIP:
```Python
pip install numpy
pip install matplotlib
pip install pandas
```

##Usage
In order to use this module, sys is needed to ad the TAS.py file in the path to import:
```Python
import sys
sys.path.append("~/GeoPython/TAS.py")
import TAS
```

Remember that you need to import the module first and then you can use the functions in it.

You need to put you data in a xlsx file in the same form as the example file "TAS.xlsx"
```Python
TasRawData = pd.read_excel("TAS.xlsx")
```


Then you only need to input the data from the file, and everything will be done.
```Python
TAS.PlotData(TasRawData)
```

If the data file is in the right form and nothing goes wrong, you will have three files:
* a svg(Scalable Vector Graphics) file which can be modified directly in Adobe Illustrator or Corel Draw,
* a png (Portable Network Graphics) and a more commonly used jpg.

You can also set the width and color of lines like this:
```
TAS.PlotData(TasRawData,0.5,'b')
```

They are optional. And the letters for different colors are shown below:

b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white


And the items on the map stand for these different kinds of rocks.

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






