Title: GeoPython,a project of using Python for geology related daily work
Date: 2016-12-18 16:20
Category: Python


# [GeoPython, a Python tool set for geology related daily work](https://github.com/chinageology/GeoPython)



##### author: cycleuser

##### email: cycleuser@cycleuser.org

##### Copyright 2017 cycleuser


|MileStone|Date|Function|
|--|--|--|
|Beginning Date|2016-07-07 6:20|TAS|
|Adding QAPF|2016-07-09 08:32|QAPF|
|Adding Wulff|2016-12-18 08:32|Wulf|
|Reconsitution|2017-03-15 15:30|Pearce and  Harker|
|Single Zircon Ce|2017-03-25 15:30|Ballard|
|Multiple Zircon Ce|2017-03-28 15:30|MultiBallard|
|Multiple Samples CIPW Norm|2017-04-3 12:30|MultiCIPW|
|NewGUI|2017-07-23 12:30|GUI Powered By PyQt5|

## Introduction

GeoPython is a project of using Python for geology related daily work. It is a set of free softwares: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.



## Installation


The standalone application file is temporarily only provided on Windows platform. Users of other Operating Systems please try to use GeoPython in Python. And this is also recommended because the latest version can be installed with pip easily.

### Install Python First

The first thing to do is to install Python, newer than 3.5, which can be download from [Python Website](https://www.python.org/downloads/) or  [Tsinghua Tuna](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/).

Anaconda3-4.0.0 and other newer versions of Anaconda3 are recommended.

### Install GeoPython with PIP

After installation of Python, you can use the following commands in your terminal to install GeoPython:

```Bash
pip install --upgrade git+git://github.com/python-quantities/python-quantities.git@master
pip install --upgrade geopython --no-cache-dir
```

If there comes no error message, everything should have been done successfully.

## Usage in Python interpreter



After the installation step above, GeoPython now becomes available in Python interpreter. The **IPython** interpreter is recommended because it is much friendly than the buildin interpreter of Python. **IPython** can be also installed with pip:
```Bash
pip install ipython
```

Then you can simply use **GeoPython** by type the following commands in your Python interpreter:
```Python
import sys
import geopython as gp
sys.exit(gp.begin())
```


OR


```Python
import sys
import geopython as gp
gp.main()
```


You would see the GUI of **GeoPython**, which is under development for now. So it is a good idea to update **GeoPython** with pip everytime before you use it:

```Bash
pip install --upgrade geopython
```

## New GUI！


Here is a new version of GUI, that is still under development.

The files of this New GUI can be found under the [NewGUI](/NewGUI) folder.

Only a few functions are available for now, at the moment I am typing here there is only TAS and not even a whole good TAS function.

We may all know that nice things always happen gradually. So please be patient and give me some time.

I must apologize for the slow development, that is partially caused by my bad physical situation from the tumor operation at the end of last year, and mainly because my bad choice of choosing Kivy in the past. Kivy is cute and funny, but not as reliable as PyQt at all. That means I must learn to use PyQt5 from beginning to use it as the framework of the GUI of GeoPython.




The New Zircon Ce function need Data template file named as [ZirconCe.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/ZirconCe.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewZirconCe.png)


The New  TAS, REE and Trace Elements functions share a same Data template files:
[Data.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Data.xlsx)


![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTAS.png)
![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTrace.png)


The New StereoNet Projection and the RoseMap function need Data template file named as [Structure.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Structure.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/Rose.png)



## Legacy Usage Under Windows

[Legacy Download](https://github.com/chinageology/GeoPython/blob/master/Download.md)

If you are using Windows 7, there might comes an`api-ms-win-crt`related error. You needto install KB2999226 and then install the `Visual C++ Redistributable 2015`.
Of course, a sweet guy like me just packed them up and share here: [32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)，[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW).

For Windows Users, donwload the Windows version zip file and extrat the whole file into a folder, then just put your data in the correspoinding Xlsx file and double click the correspoinding main.exe and click on the function you need.
