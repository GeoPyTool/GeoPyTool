Title: Installation-Expert
Date: 2020-12-29 19:13:50
Category: English
Tags: Doc,English,Support

# Installation, For Expert 

GeoPyTool can also be used as a module inside Python.

# 1. Install Python

Find help from [Python official website](https://www.python.org/downloads/) please.

# 2. Install Needed Modules

Then run the following commands in **terminal** to install some base modules:
```Bash
pip install cython numpy scipy matplotlib sympy pandas xlrd pyopengl BeautifulSoup4 pyqt5 scikit-learn requests tensorflow torch keras tqdm
```

If you encounter errors, which might be related to numpy or tensorflow, please run the following commands to specify a particular version.
```Bash
pip install numpy ==1.8.5
pip install tensorflow==2.3.1
```

# 3. Install GeoPyTool

After all the modules above getting installed, run the following command to install GeoPyTool:
```Bash
pip install geopytool
```

If there comes no error message, everything should have been done successfully.

# 4. Run GeoPyTool

If there is no error reported, run the following commands in the Terminal to run GeoPyTool:
```Bash
python -c "import geopytool;geopytool.main()"
```

# 5. Update an existing GeoPyTool

If you installed GeoPyTool as a module in Python, you can use the following command in the **terminal** to update GeoPyTool to the latest version on any operating system:
```Bash
pip install geopytool --update --no-cache-dir
```

It is a good idea to update **GeoPyTool** with pip everytime before you use it.


