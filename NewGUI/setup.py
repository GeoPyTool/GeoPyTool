#!/usr/bin/env python

from distutils.core import setup
import CustomClass

import gpversion as gv

version= gv.version

setup(name='geopython',
      version=version,
      description='a tool set for daily geology related task.',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='http://blog.cycleuser.org',
      packages=['geopython'],
      py_modules=['CustomClass'],
      install_requires=[ "cython",
                         "numpy",
                         "pandas",
                         "xlrd",
                         "matplotlib",
                         "BeautifulSoup4",
                         "PyQt5",
                         ],
     )
