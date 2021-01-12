#!/usr/bin/env python
#coding:utf-8
import os
from geopytool.ImportDependence import *
from geopytool.CustomClass import *
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    README = 'https://github.com/GeoPyTool/GeoPyTool/blob/master/README.md'


setup(name='geopytool',
      version="0.9.21.0.003",
      description='a tool for daily geology related task. visit geopytool.com for further information',
      longdescription=README,
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/GeoPyTool/GeoPyTool',
      packages=['geopytool'],
      package_data={
          'geopytool': ['*.py','*.txt','*.png','*.qm','*.ttf','*.ini','*.md'],},
      include_package_data=True,
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
                        'tensorflow',
                        'torch',
                        'keras',
                        'tqdm',
                        'gym',
                         ],
     )