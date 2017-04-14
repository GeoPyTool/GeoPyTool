# !/usr/bin/env python3#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-03-13
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd

# Stacked Bar Chart for heavy minearls in sediments
"""

lang = "python"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
import math
import sys
import csv

import Unit

class StackedBar(Unit.Frame,Unit.Tool):

    name = "StackedBar.xlsx"

    def __init__(self, name="StackedBar.xlsx",Label=[u'Z', u'X', u'Y']):
        super().__init__()

        self.raw = ''

        self.Label = Label
        self.name=name


    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.raw=''
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        self.raw=raw
        self.raw.plot.barh(stacked=True)
        self.SavePic(name= self.name)

if __name__ == '__main__':
    StackedBar().read()
