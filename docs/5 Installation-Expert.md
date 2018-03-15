Title: Installation-Expert
Date: 2017-11-15 0:00
Category: Doc
Tags: Doc,English,Chinese

#Installation, For Expert 




GeoPyTool can be used as a module inside Python, and can also run as a standalone application.



## Use as a Python Module


Users of other Operating Systems, such as Debian Linux, Ubuntu Linux, Fedora Linux, FreeBSD or GNU/Hurd, please try to use GeoPyTool in Python, which is also recommended to all the users including those who use macOS or Windows 10, because the latest version of GeoPyTool can be installed with pip easilier and faster than using standalone executable files.

## Install Python First

### MacOS

### Linux Users
Here we only take Ubuntu 16.04.4 for example.

Open Terminal, run the following commands to keep your system updated:
```Bash
apt update
apt upgrade
```
Then run the following commands to install Python3 and PIP for Python3:
```Bash
apt install python3
apt install python3-pip
```
After the installation above, run the following command to install conda to make the installation of some modules such as numpy/scipy easy:
```Bash
pip3 install conda
```
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
pip3 install cython numpy scipy matplotlib sympy pandas xlrd pyopengl BeautifulSoup4 pyqt5 scikit-learn  requests pyqtgraph
```

After all the modules above getting installed, run the following command to install GeoPyTool:
```Bash
pip3 install geopytool
```

If there is no error reported, run the following commands in the Terminal to run GeoPyTool:
```Bash
python3 -c "import geopytool;geopytool.main()"
```




### Windows Users
The first thing to do is to install Python, newer than 3.6, which can be download from [Python Website](https://www.python.org/downloads/) or  [Tsinghua Tuna](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/).

Anaconda3-4.0.0 and other newer versions of Anaconda3 are recommended. Because they already contain useful modules such as cython, numpy, pandas, matplotlib, and the powerful ipython.

#### Patches Needed

[Microsoft Visual C++ Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) is required for the installation of scikit-learn. Another solution is to use conda to install scipy and scikit-learn.

#### For Windows 7

To use GeoPyTool on Windows 7, You need to install the **SP1 of Windows** and then install **KB2999226 Patch** and the **Visual C++ Redistributable 2015**.

The SP1 package of Windows 7 can be found at [here, the official website of MicroSoft](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1).

The installation packages of KB2999226 and the `Visual C++ Redistributable 2015` are already contained in the Zip file of GeoPyTool for Windows, and can also be found here: [32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)，[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW).
I am really a sweet guy, isn't it?

If you are using Windows 7 without the SP1 package installed, there might comes an`api-ms-win-crt`related error. So believe me my friend, just install these patched below, they won't harm you after all.

So if you encounter any `api-ms-win-crt`related errors, please check those installations first.



### Install GeoPyTool with PIP

Then you can download a Python 3.6.4 or newer version of Python3 from Python.org, and run the installer to install it to your Windows.

But, be sure to check the box of setting Python to system Path:



After installation of Python, you might think that finally you can install GeoPyTool.

**NO!** In fact you need to install some used packages first, even you are using Anaconda. Because some packages used to build the Graphic User Interface of GeoPyTool still need to be installed, and this is also a good chance for you to update all the modules to the latest version (OR not).

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
pip install pyopengl
pip install pyqtgraph
```



We install conda with pip first:

```Bash
pip install requests
pip install pyopengl
pip install pyqtgraph
pip install conda
```
Then we use conda to install some other packages:
```Bash
python3 -m conda install cython numpy pandas xlrd matplotlib BeautifulSoup4 scipy scikit-learn sympy requests pyopengl
pip3 install pyqt5  pyqtgraph
```

After the installation of those packages above, you can use this similar command also in the **terminal** to install the GeoPyTool.
```Bash
pip install geopytool
```

If there comes no error message, everything should have been done successfully.

### Update an existing GeoPyTool

If you installed GeoPyTool as a module in Python, you can use this similar command also in the **terminal** to update to the latest version of GeoPyTool.
```Bash
pip install geopytool --update --no-cache-dir
```

### Launch GeoPyTool form a Python interpreter

After the installation step above, GeoPyTool now becomes available in Python interpreter. The **IPython** interpreter is recommended because it is much friendly than the buildin interpreter of Python. **IPython** can be also installed with pip:
```Bash
pip install ipython
```

Then you can run ipython in **terminal** with the following command:
```Bash
ipython
```

Then you can simply use **GeoPyTool** by type the following commands in your Python interpreter:

```Python
import geopytool as gp
gp.main()
```


You would see the GUI of **GeoPyTool**, which is under development for now. So it is a good idea to update **GeoPyTool** with pip everytime before you use it:

```Bash
pip install --upgrade geopytool
```


