Title: GeoPython,a project of using Python for geology related daily work
Date: 2016-12-18 16:20
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
|Adding Wulff|2016-12-18 08:32|Wulf|

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

##Background Information 
>##背景知识

You can also set width, color and other features in the Xlsx files. And the introduction can be found [here](http://www.jianshu.com/p/67cbc84e57a6)
>你可以在数据文件中对应的位置设置线宽、颜色等各种属性。对这些属性的说明可以参考[这里](http://www.jianshu.com/p/67cbc84e57a6)

##Usage Under Windows
>##在Windows系统中用法

Just put your data in the correspoinding Xlsx file and double click the correspoinding EXE file.
>把你的数据按照示范放到模板文件中，然后双击对应名字的exe程序就行了。


##Usage with Python
>##在Python下的用法

In order to use these modules, you need to install geopython with pip:
>现在可以用pip来安装geopython了：


```Bash
pip install geopython
```

Then open you python , and enter to the location path of data files, which are the xlsx files that  you still need to download from [here](https://github.com/cycleuser/GeoPython/tree/master/Python). Then you can use geopython as the codes below:
>然后打开你的python，进入到数据目录，目前数据文件还要在[这里](https://github.com/cycleuser/GeoPython/tree/master/Python)下载。下载好样本文件，把自己的数据填入，然后用下面的命令就可以运行了：

```Bash
ipython
```

```Python
from geopython import geopython

geopython.tas("tas.xlsx")
geopython.qfl("qfl.xlsx")
geopython.qmflt("qfl.xlsx")
geopython.ree("ree.xlsx")
geopython.qapf("qapf.xlsx")
geopython.wulf("strike.xlsx")
geopython.schmidt("strike.xlsx")

```

Remember that you need to import the module first and then you can use the functions in it.
>一定记得，只有先导入了模块，才能使用里面的功能。

You need to put you data in a xlsx file in the same form as the example files.
>导入完毕后，根据我提供的样板文件，把你的数据输入进去。

If python told you that it cannot find a xlsx file, you must have entered to the wrong location, and you need to use the cd command to go to the path containing xlsx files that you downloaded and modiffed.
>如果python提醒你找不到excel的xlsx文件，很可能就是你进错目录了，那样你就需要找到你下载并修改的xlsx文件的位置，用cd命令进去，然后再进行上面的操作。


Then you only need to input the data from the file, and everything will be done.
>然后你就在程序中如下所示这样读取一下，然后用对应模块的函数帮你搞定一切了。（注意大小写！）


If the data file is in the right form and nothing goes wrong, you will have three files, which will be in the same location of these xlsx files:
>如果你的数据文件没有什么问题，你就能得到图像了，这些图像会存放在excel表格文件所在的同一目录下：

* a svg(Scalable Vector Graphics) file which can be modified directly in Adobe Illustrator or Corel Draw,
>* 一个碉堡的 svg（一种矢量图）文件，直接就能用Adobe Illustrator 或者 Corel Draw来打开编辑。


* a png (Portable Network Graphics) .
>* 然后就是一个png图像了。





![](https://github.com/cycleuser/GeoPython/blob/master/TAS-Plot.png?raw=true)


![](https://raw.githubusercontent.com/cycleuser/GeoPython/master/QFL-Plot.png)

![](https://raw.githubusercontent.com/cycleuser/GeoPython/master/REE-Plot.png)

![](https://github.com/cycleuser/GeoPython/blob/master/Wulff.png?raw=true)