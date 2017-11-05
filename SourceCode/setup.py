#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
import CustomClass
version=CustomClass.version

date=CustomClass.date

setup(name='geopython',
      version=version,
      description='a tool for daily geology related task. visit bbs.geopython.com for further information',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='https://github.com/chinageology/GeoPython',
      packages=['geopython'],
      package_data={
          'geopython': ['*.png','*.qm','*.ttf'],
      },
      include_package_data=True,

      py_modules=['CustomClass'],
      install_requires=[ "cython",
                         "numpy",
                         "pandas",
                         "xlrd",
                         "matplotlib",
                         "BeautifulSoup4",
                         "requests",
                         "PyQt5",
                         ],
     )
