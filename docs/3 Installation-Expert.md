Title: Installation-Expert
Date: 2018-04-21 11:27:50
Category: English
Tags: Doc,English,Support

# Installation, For Expert 

GeoPyTool can also be used as a module inside Python.

# 1. MacOS

## 1.1 Install Brew and Python3

Go to [brew.sh](http://brew.sh/) to to install brew in MacOS.

After the Installation of Brew, run the following commands to install python3:
```Bash
brew install python3
```
## 1.2 Install Needed Modules

Then run the following commands to install some base modules:
```Bash
pip3 install cython
pip3 install numpy
pip3 install pandas
pip3 install xlrd
pip3 install matplotlib
pip3 install BeautifulSoup4
pip3 install pyqt5
pip3 install scipy
pip3 install scikit-learn
pip3 install sympy
pip3 install requests
pip3 install pyopengl
pip3 install pyqtgraph
```

Or you may try to use one line command to install all the required modules:
```Bash
pip3 install cython numpy scipy matplotlib sympy pandas xlrd pyopengl BeautifulSoup4 pyqt5 scikit-learn requests pyqtgraph
```
## 1.3 Install GeoPyTool

After all the modules above getting installed, run the following command to install GeoPyTool:
```Bash
pip3 install geopytool
```


# 2. Linux
Here we only take Ubuntu 16.04.4 for example.

## 2.1 Update System to Latest

Open Terminal, run the following commands to keep your system updated:
```Bash
apt update
apt upgrade
```
## 2.2 Instal Python3 and Pip3
Then run the following commands to install Python3 and PIP for Python3:
```Bash
apt install python3
apt install python3-pip
```


## 2.3 Install Needed Modules

Then run the following commands to install some base modules:
```Bash
pip3 install cython
pip3 install numpy
pip3 install pandas
pip3 install xlrd
pip3 install matplotlib
pip3 install BeautifulSoup4
pip3 install pyqt5
pip3 install scipy
pip3 install scikit-learn
pip3 install sympy
pip3 install requests
pip3 install pyopengl
pip3 install pyqtgraph
```
Or you may try to use one line command to install all the required modules:
```Bash
pip3 install cython numpy scipy matplotlib sympy pandas xlrd pyopengl BeautifulSoup4 pyqt5 scikit-learn requests pyqtgraph
```
## 2.4 Install GeoPyTool

After all the modules above getting installed, run the following command to install GeoPyTool:
```Bash
pip3 install geopytool
```


# 3. Windows
The first thing to do is to install Python, newer than 3.6, which can be download from [Python Website](https://www.python.org/downloads/).

## 3.1 Install Patches Needed

[Microsoft Visual C++ Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) is required for the installation of scikit-learn. Another solution is to use conda to install scipy and scikit-learn.

### For Windows 7

To use GeoPyTool on Windows 7, You need to install the **SP1 of Windows** and then install **KB2999226 Patch** and the **Visual C++ Redistributable 2015**.

The SP1 package of Windows 7 can be found at [here, the official website of MicroSoft](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1).

The installation packages of KB2999226 and the `Visual C++ Redistributable 2015` can also be downloaded from here: 
[32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)
[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW)


Be careful to choose the right version suitable for your Windows.

If you are using Windows 7 without the SP1 package installed, there might comes an`api-ms-win-crt`related error. So believe me my friend, just install these patched below, they won't harm you after all.

So if you encounter any `api-ms-win-crt`related errors, please check those installations first.



## 3.2 Install Python

Then you can download a Python 3.6.4 or newer version of Python3 from [Python.org](https://www.python.org/downloads/windows/), and run the installer to install it to your Windows.

#### Notice
Make sure to check the box of setting Python to system Path:
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/WindowsInstallAddPythonToPath.png)




## 3.3 Install Needed Modules

After installation of Python, you need to install some used packages first.
So use the following commands in your **terminal** to install these modules.

>You don't know what a Terminal is? For Windows, it can be the mighty **CMD** or PowerShell. For other systems including macOS, it should be the **BASH** ore just labeled as **Terminal** in the built-in applications list. Still don't know how to launch a terminal? Google it dude, we can't do that hand by hand for you.


Here we use pip as we assume that your default version of Python is Python 3.X and the pip will refer to the PIP under Python3. If you installed both Python 2.X and Python 3.X, you might need to try to use **pip3** instead of **pip** in all the following commands to call the PIP of Python 3.

Then run the following commands in your **terminal** to install some base modules:
```Bash
pip3 install cython
pip3 install numpy
pip3 install pandas
pip3 install xlrd
pip3 install matplotlib
pip3 install BeautifulSoup4
pip3 install pyqt5
pip3 install scipy
pip3 install scikit-learn
pip3 install sympy
pip3 install requests
pip3 install pyopengl
pip3 install pyqtgraph
```

Or you may try to use one line command to install all the required modules:
```Bash
pip3 install cython numpy scipy matplotlib sympy pandas xlrd pyopengl BeautifulSoup4 pyqt5 scikit-learn requests pyqtgraph
```

## 3.4 Install GeoPyTool
After the installation of those packages above, you can use this similar command also in the **terminal** to install the GeoPyTool.
```Bash
pip3 install geopytool
```

If there comes no error message, everything should have been done successfully.

# 4. Run GeoPyTool

If there is no error reported, run the following commands in the Terminal to run GeoPyTool:
```Bash
python3 -c "import geopytool;geopytool.main()"
```

# 5. Update an existing GeoPyTool

If you installed GeoPyTool as a module in Python, you can use the following command in the **terminal** to update GeoPyTool to the latest version on any operating system:
```Bash
pip3 install geopytool --update --no-cache-dir
```

It is a good idea to update **GeoPyTool** with pip everytime before you use it.


