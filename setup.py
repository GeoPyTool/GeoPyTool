#!/usr/bin/env python

from distutils.core import setup

setup(name='geopython',
      version='0.2.23',
      description='a tool set for daily geology related task.',
      author='cycleuser',
      author_email='cycleuser@cycleuser.org',
      url='http://blog.cycleuser.org',
      packages=['geopython'],
      install_requires=[ "cython",
                         "numpy",
                         "pandas",
                         "xlrd",
                         "matplotlib",
                         "chempy ",
                         ],
     )
