Title: GeoPython, a one-stop cross-platform application for geology related daily work
Date: 2017-11-04 16:20:48
Category: Python

# GeoPython,a one-stop cross-platform application for geology related daily work

##### author: cycleuser
##### email: cycleuser@cycleuser.org
##### Copyright 2017 cycleuser
##### [Official BBS](http://bbs.geopython.com/)



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
|All Rebuild|2017-08-31 23:30|Harker Back|
|Temp Calc|2017-10-17 20:48:21|Zircon/Rutile|
|Load PNG/JPG/SVG|2017-10-23  17:38:21|Load Base Maps|
|Chinese/English Switch|2017-10-25 21:00:20|Language|
|More Languages|2017-10-30 23:00:20|User can choose own Language file|


## Introduction

GeoPython is an application based on Python and designed as a solution for geology related daily work. **It can run on alomost all mainstream operating systems**, such as Windows 7 SP1, Windows 8, Windows 10, macOS Sierra, macOS High Sierra, Ubuntu Linux, Debian Linux, Fedora Linux, and alomost all other widely used desktop platforms.

**GeoPython doesn't rely on any other software**, such as MS Excel or CorelDraw, it can directly transport your data into the plot as vector graphic files and the calculation results into data sheets such as Xlsx or CSV files.


It is a **free software**: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

GeoPython contains both traditional routines and newly developed methods, which are shown in the table below.

|Function|Brief description|Reference
|--|--|--|
|TAS plot|Volcanic or intrusive rocks classification with SiO2 and (Na2O+K2O)|Maitre et al., 1989, Middlemost, 1994|
|QAPF plot|Plutonic or volcanic rocks classification with Q (quartz), A (alkali feldspar), P (plagioclase) and F (feldspathoid)|Maitre et al., 2004|
|REE|Compare Rare Earth Elements with standard samples as Spider Diagram to analyze the distribution, tendency and anomalies|Boynton, 1984|
|Trace elements |Compare Trace Elements with standard samples as Spider Diagram to analyze the distribution, tendency and anomalies|Sun and McDonough, 1989|
|Rb-Y+Nb, Rb-Yb+Ta, Nb-Y, and Ta-Yb plots|Tectonic settings classification with Y-Nb, Yb-Ta, Rb- (Y + Nb) and Rb- (Yb + Ta) for granites|Pearce et al., 1984|
|Stereographic projection and rose diagram|Virtualization and basic analyzation of outcrop occurrence; distribution, tendency and anomalies as a rose diagram with stereographic projection on Wulf net and Schmidt net.|Zhou et al., 2003|
|QFL and QmFLt plots|“Triangular QFL and QmFLt compositional diagrams for plotting point counts of sandstones can be subdivided into fields that are characteristic of sandstone suites derived from the different kinds of provenance terranes controlled by plate tectonics.”|Dickinson et al. 1983|
|CIPW normalization|CIPW norm calculation with multiple samples |Johannsen, 1939; Washington, 1917; CIPW norm Excel spreadsheet by Kurt Hollocher|
|Zircon Ce4/Ce3|Calculate Ce(IV)/Ce(III) ratio in zircon to infer relative oxidation state in a wide range of intermediate to felsic igneous rocks.|Ballard et al., 2002|
|Zircon and Rutile thermometers|Use Ti element in Zircon and Zr element in Rutile to calculate the temperature of crystallization.|Watson et al., 2006|
|Cluster|A basic version of hierarchical clustering analyzation of different number valued items.|
|Loading any picture as base map|Both X-Y plot and triangular diagram is supported, that means users can use any picture form any articles as their base map to plot data on and generate their diagram even it has not been contained by any other softwares.|An original function|



## Installation

GeoPython can be used as a module inside Python, and can also run as a standalone application.



## Standalone Application

Packed up executable files are temporarily only provided for Windows and MacOS platform.



[Click here to get Download links.](https://github.com/chinageology/GeoPython/blob/master/Download.md)

### Mac APP

On macOS, everything is extremely easy to use GeoPython. Just download and unzip the file, then double click on the GeoPython.app file, you will find the APP available as the following picture shows.

![User Interface of the APP on macOS.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/MacOSScreenShot.png)


### Windows EXE

#### Windows 8/8.1/10 Users

On these modern Windows platforms, everything is also extremely easy to use GeoPython. Just download and unzip the file, then double click on the GeoPython.exe file, and make sure that you don't delete any file form the unziped folder because they are all required by the program, then you will find the APP available as the following picture shows.

![User Interface of the EXE on Windows.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/ScreenShot.png)

#### Windows 7 Users

Of corse, you must find that the screen shot above is actrually from a Windows 7  virtual machine.

That's right, you can obviously use GeoPython on Windows 7, on which some system patches need to be installed. You need to install the SP1 of Windows and then install KB2999226 and the `Visual C++ Redistributable 2015`. If you are using Windows 7 without the SP1 package installed, there might comes an`api-ms-win-crt`related error. So believe me my friend, just install these patched below, they won't harm you after all.

The SP1 package of Windows 7 can be found at [here, the official website of MicroSoft](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1).

The installation packages of KB2999226 and the `Visual C++ Redistributable 2015` are already contained in the Zip file of GeoPython for Windows, and can also be found here: [32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)，[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW).
I am really a sweet guy, isn't it?
So if you encounter any `api-ms-win-crt`related errors, please check those installations first.

#### Windows XP or Vista Users

I failed many times on both XP and Vista, and I think there might not be a lot users of these two antique systems.
If you are using one or both of them, please be good to yourself to update you old PC to at least Windows 7 SP1 or try Linux on your antique computers. My advice is that we should not waste our life on those systems that are not even supported by their developers and manufacturer. So, if you still want to run GeoPython on those two old systems, good luck and good bye.




## Use as a Python Module


Users of other Operating Systems, such as Debian Linux, Ubuntu Linux, Fedora Linux, FreeBSD or GNU/Hurd, please try to use GeoPython in Python, which is also recommended to all the users including those who use macOS or Windows 10, because the latest version of GeoPython can be installed with pip easilier and faster than using standalone executable files.

### Install Python First

The first thing to do is to install Python, newer than 3.5, which can be download from [Python Website](https://www.python.org/downloads/) or  [Tsinghua Tuna](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/).

Anaconda3-4.0.0 and other newer versions of Anaconda3 are recommended. Because they already contain useful modules such as cython, numpy, pandas, matplotlib, and the powerful ipython.


##### Useful links for Windows users to install GeoPython with PIP:

In fact, you guys can easily find instructions on how to install Python and PIP on the Internet. So I will just cast some links for newbie using Python on Windows.

###### 32bit：

|Item |Address |
|--|--|
|Anaconda|https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-4.4.0-Windows-x86.exe|

###### 64bit：

|Item |Address |
|--|--|
|Anaconda|https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-4.4.0-Windows-x86_64.exe|

### Install GeoPython with PIP


After installation of Python, you might think that finally you can install GeoPython.

**NO!** In fact you need to install some used packages first, even you are using Anaconda. Because some packages used to build the Graphic User Interface of GeoPython still need to be installed, and this is also a good chance for you to update all the modules to the latest version (OR not).

So use the following commands in your **terminal** to install these modules.

You don't know what a Terminal is? For Windows, it can be the mighty **CMD** or PowerShell. For other systems including macOS, it should be the **BASH** ore just labeled as **Terminal** in the built-in applications list. Still don't know how to launch a terminal? Google it dude, we can't do that hand by hand for you.

#### Notice

	Here we use pip as we assume that your default version of Python is Python 3.X and the pip will refer to the PIP under Python3. If you installed both Python 2.X and Python 3.X, you might need to try to use **pip3** instead of **pip** in all the following commands to call the PIP of Python 3.

So paste the following commands in your **terminal** as their sequence to install these modules in order.

```Bash
pip install cython
pip install numpy
pip install pandas
pip install xlrd
pip install matplotlib
pip install BeautifulSoup4
pip install pyqt5
pip install scipy
pip install scikit-learn
pip install sympy
```

After the installation of those packages above, you can use this similar command also in the **terminal** to install the GeoPython.
```Bash
pip install geopython
```

If there comes no error message, everything should have been done successfully.

### Update an existing GeoPython

If you installed GeoPython as a module in Python, you can use this similar command also in the **terminal** to update to the latest version of GeoPython.
```Bash
pip install geopython --update --no-cache-dir
```

### Launch GeoPython form a Python interpreter

After the installation step above, GeoPython now becomes available in Python interpreter. The **IPython** interpreter is recommended because it is much friendly than the buildin interpreter of Python. **IPython** can be also installed with pip:
```Bash
pip install ipython
```

Then you can run ipython in **terminal** with the following command:
```Bash
ipython
```

Then you can simply use **GeoPython** by type the following commands in your Python interpreter:

```Python
import geopython as gp
gp.main()
```


You would see the GUI of **GeoPython**, which is under development for now. So it is a good idea to update **GeoPython** with pip everytime before you use it:

```Bash
pip install --upgrade geopython
```

## Marker/Color/Style

All these details in GeoPython are the same as those in Matplotlib becasue that is what GeoPython used to visualize data.

Markers of Points can be reffered from here:
http://matplotlib.org/api/markers_api.html

Colors can be reffered from here:
http://matplotlib.org/api/colors_api.html

Here is a picture of Line Styles and Point Markers form [nrougier](http://www.labri.fr/perso/nrougier/teaching/matplotlib/):

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/LIneStylesMarkers.png)


## Need Further Help?

Visit our BBS http://bbs.geopython.com/ and write a post to describe your problems in detail. We will response as soon as we can.


## Appendix


The New Zircon Ce function need Data template file named as [ZirconCe.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/ZirconCe.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewZirconCe.png)


The New  TAS, REE and Trace Elements functions share a same Data template files:
[Data.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Data.xlsx)


![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTAS.png)
![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTrace.png)


The New StereoNet Projection and the RoseMap function need Data template file named as [Structure.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Structure.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/Rose.png)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/LoadPNG.png)

