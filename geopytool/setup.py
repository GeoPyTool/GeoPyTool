#!/usr/bin/env python
#coding:utf-8
import os
from distutils.core import setup
from geopytool.ImportDependence import *
from geopytool.CustomClass import *



here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    README = 'https://github.com/GeoPyTool/GeoPyTool/blob/master/README.md'


setup(name='geopytool',
      version=version,
      description='a tool for daily geology related task. visit geopytool.com for further information',
      longdescription=README,
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/GeoPyTool/GeoPyTool',
      packages=['geopytool'],
      package_data={
          'geopytool': ['*.py','*.png','*.qm','*.ttf','*.ini','*.md'],
      },
      include_package_data=True,

      #py_modules=['CIPW','Cluster','geopytool/CustomClass','Harker','IMP','Magic','MudStone','MultiDimension','OldCustomClass','Pearce','PlotModel','QAPF','QFL','QmFLt','REE','Rose','Stereo','TAS','TableViewer','Temp','Test','Trace','XY','XYZ','ZirconCe','cli'],

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
                         ],
     )