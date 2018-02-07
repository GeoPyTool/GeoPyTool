#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
from geopytool.ImportDependence import *
from geopytool.CustomClass import *


setup(name='geopytool',
      version=version,
      description='a tool for daily geology related task. visit geopytool.com for further information',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/GeoPyTool/GeoPyTool',
      packages=['geopytool'],
      package_data={
          'geopytool': ['*.py','*.png','*.qm','*.ttf','*.ini'],
      },
      include_package_data=True,

      #py_modules=['CIPW','Cluster','geopytool/CustomClass','Harker','IMP','Magic','MudStone','MultiDimension','OldCustomClass','Pearce','PlotModel','QAPF','QFL','QmFLt','REE','Rose','Stereo','TAS','TabelViewer','Temp','Test','Trace','XY','XYZ','ZirconCe','cli'],

      #py_modules=['geopytool.CustomClass'],

      install_requires=[ 
                        'cython',
                        'numpy',
                        'pandas',
                        'scipy',
                        'xlrd',
                        'openpyxl',
                        'matplotlib',
                        'BeautifulSoup4',
                        'requests',
                        'PyQt5',
                        'scikit-image',
                        'scikit-learn',
                        'pyqtgraph',
                         ],
     )
