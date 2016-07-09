Title: GeoPython,a project of using Python for geology related daily work
Date: 2016-7-7 6:20
Category: Python


#[GeoPython, a project of using Python for geology related daily work](https://github.com/cycleuser/GeoPython)
>#[GeoPython，一个将 Python 用于地质学的日常工作的计划](https://github.com/cycleuser/GeoPython)


https://github.com/cycleuser/GeoPython


#####author: cycleuser
#####email: cycleuser@cycleuser.org
#####Copyright 2016 cycleuser


|MileStone|Date|Function|
|--|--|--|
|Beginning Date|2016-07-07 6:20|TAS|
|Adding QAPF|2016-07-09 08:32|QAPF|


##Introduction



GeoPython is a project of using Python for geology related daily work. It is a set of free softwares: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>GeoPython 是一个将 Python 用于地质学的日常工作的计划。这是一套自由软件：你可以重新分发或者做出修改，但必须基于由自由软件基金会发布的GNU通用公共许可证第三版的许可,或其后的版本。



TAS.py and QAPF.py are all Python modules of plotting data of volcanic rocks.
All data used in this module are from the book：
"Igneous Rocks_ a Classification and Glossary of Terms"
 by  R.W. Le Maitre & International Union of Geological Sciences 2002
>TAS.py 和 QAPF.py 都是用于火山岩数据投图的 Python 模块。
>其中所有用到的数据引用自下面这本书：
>《火成岩—分类和术语表》
>R.W. Le Maitre & International Union of Geological Sciences 2002


Texts below is cited from this book as an introduction:
>下面这部分文本引用自该书原文，用作简要说明：

```language
The TAS (Total Alkali – Silica) classification should be used only if:
>TAS（ 全碱-硅）分类法只适用于以下条件：

(1) the rock is considered to be volcanic
>必须得是火山岩；

(2) a mineral mode cannot be determined, owing either to the presence of glass or to the fine-grained nature of the rock
>由于存在玻璃质，或者矿物晶体粒度太小，导致矿物模式不好确定；
(3) a chemical analysis of the rock is available.

>有全岩化学成分数据。

QAPF modal classification of volcanic rocks (based on Streckeisen, 1978, Fig. 1).
>QAPF 火山岩模式分类基于 Streckeisen，1978年的文献。

(1) The corners of the double triangle are Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.
>双三角图解中的 Q 代表石英，A 代表碱性长石，P 代表斜长石，F 代表似长石。

(2) This diagram must not be used for rocks in which the mafic mineral content, M, is greater than 90%.
>切忌将该图解用到镁铁质矿物超过90%的情况，这种情况绝对不能用这个图！


```


##Dependence
>##依赖关系

This module is written with Python3.4 and based on numpy, matplotlib and pandas. That means you need to install them.
>本模块是在Python 3.4下写的，基于 numpy， matplotlib 以及 pandas。所以这几个包你都得安装。

You can install these packages with PIP:
>用PIP就可以安装了：

```Python
pip install numpy
pip install matplotlib
pip install pandas
```

##Usage
>##用法

In order to use these modules, sys is needed to add the files in the path to import:
>要使用这些模块，首先要导入 sys 来把下面这些文件加入到路径中来导入：


```Python
import sys
sys.path.append("./TAS.py")
sys.path.append("./QAPF.py")

import TAS
import QAPF
```

Remember that you need to import the module first and then you can use the functions in it.
>一定记得，只有先导入了模块，才能使用里面的功能。

You need to put you data in a xlsx file in the same form as the example files.
>导入完毕后，根据我提供的样板文件，把你的数据输入进去。

Then you only need to input the data from the file, and everything will be done.
>然后你就在程序中如下所示这样读取一下，然后用对应模块的PlotData函数帮你搞定一切了。（注意大小写！）

```Python

TasRawData = pd.read_excel("TAS.xlsx")
QapfRawData= pd.read_excel("QAPF.xlsx")


TAS.PlotData(TasRawData)
QAPF.PlotData(QapfRawData)
```

If the data file is in the right form and nothing goes wrong, you will have three files:
>如果你的数据文件没有什么问题，你就能得到三个文件：

* a svg(Scalable Vector Graphics) file which can be modified directly in Adobe Illustrator or Corel Draw,
>* 一个碉堡的 svg（一种矢量图）文件，直接就能用Adobe Illustrator 或者 Corel Draw来打开编辑。


* a png (Portable Network Graphics) and a more commonly used jpg.
>* 然后就是一个png图像和一个常用的jpg了。

You can also set the width and color of lines like this:
>你可以用两个可选变量来设定投图的线宽和线色：

```Python
TAS.PlotData(TasRawData,0.5,'b')
QAPF.PlotData(QapfRawData,0.3,'r')
```

They are optional. And the letters for different colors are shown below:
>这两个不填写也不要紧，有默认值。下面列出的是字幕对应的颜色类型：

```language
b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white
```
Same sequence of colors is used in the data file TAS.xlsx.
>在表格里面设置颜色的时候也用了同样的颜色排序。

And the items on the map stand for these different kinds of rocks.
>图表中的每一个缩写代表的岩石类型如下所示：

```language
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
```

![](https://raw.githubusercontent.com/cycleuser/GeoPython/master/Result-TAS-Plot.png)

![](https://raw.githubusercontent.com/cycleuser/GeoPython/master/Result-QAPF-Plot.jpg)