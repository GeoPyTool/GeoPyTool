#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
import CustomClass
version=CustomClass.version

date=CustomClass.date

setup(name='geopython',
      version=version,
      description='a tool set for daily geology related task.',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='http://blog.cycleuser.org',
      packages=['geopython'],
      package_data={
          'geopython': ['*.png','*.qm'],
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
