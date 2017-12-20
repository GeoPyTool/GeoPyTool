Title: Installation
Date: 2017-11-15 0:00
Category: Doc
Tags: Doc,English,Chinese

## Installation

GeoPython can be used as a module inside Python, and can also run as a standalone application.



## Standalone Application

Packed up executable files are temporarily only provided for Windows and MacOS platform.



[Click here to get Download links.](http://doc.geopython.com/Download/)

### Mac APP

On macOS, everything is extremely easy to use GeoPython. Just download and unzip the file, then double click on the GeoPython.app file, you will find the APP available as the following picture shows.

![User Interface of the APP on macOS.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/MacOSScreenShot.png)


### Mac APP Update

Drag the **UpdateGeoPython.sh** file into your terminal and hit the Enter key to run it. It will update the GeoPython inside your GeoPython.app file. Remember that never modify any files directly under the same folder unless you are an expert on dealing with Python.

![Update the APP on macOS.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/OSXUpdate.png)

### Windows EXE

#### Windows 8/8.1/10 Users

On these modern Windows platforms, everything is also extremely easy to use GeoPython. Just download and unzip the file, then double click on the **RunGeoPython.bat** file, and make sure that you don't delete any file form the unziped folder because they are all required by the program, then you will find the APP available as the following picture shows.

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

### Windows EXE Update

Double click on the  **Update.bat** file to run update. It will update the GeoPython inside your GeoPython folder. Remember that never modify any files directly under the same folder unless you are an expert on dealing with Python.


![Update the EXE on Windows.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/WinUpdate.png)



# Attention！ If you already download the packed up APP, just egnore the parts below and READ CAREFULLY PLEASE!!!!!!


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
pip install requests
pip install pyqtgraph
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


The New Zircon Ce function need Data template file named as [ZirconCe.xlsx](https://github.com/chinageology/GeoPython/blob/master/DataFileSamples/ZirconCe.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewZirconCe.png)


The New  TAS, REE and Trace Elements functions share a same Data template files:
[Data.xlsx](https://github.com/chinageology/GeoPython/blob/master/DataFileSamples/Data.xlsx)


![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTAS.png)
![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTrace.png)


The New StereoNet Projection and the RoseMap function need Data template file named as [Structure.xlsx](https://github.com/chinageology/GeoPython/blob/master/DataFileSamples/Structure.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/Rose.png)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/LoadPNG.png)

