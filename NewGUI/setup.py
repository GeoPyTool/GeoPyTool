#!/usr/bin/env python

from distutils.core import setup
import CustomClass

setup(name='geopython',
      version='0.3.42',
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
                         ],
     )
