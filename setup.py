#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
from geopython.ImportDependence import *
from geopython.CustomClass import *


setup(name='geopython',
      version=version,
      description='a tool for daily geology related task. visit bbs.geopython.com for further information',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/chinageology/GeoPython',
      packages=['geopython'],
      package_data={
          'geopython': ['*.py','*.png','*.qm','*.ttf','*.ini'],
      },
      include_package_data=True,

      #py_modules=['CIPW','Cluster','geopython/CustomClass','Harker','IMP','Magic','MudStone','MultiDimension','OldCustomClass','Pearce','PlotModel','QAPF','QFL','QmFLt','REE','Rose','Stereo','TAS','TabelViewer','Temp','Test','Trace','XY','XYZ','ZirconCe','cli'],

      #py_modules=['geopython.CustomClass'],

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
