from distutils.core import setup
import py2exe


import pandas as pd
import numpy
import matplotlib

#sys is needed to add the files in the path to import
import sys
sys.path.append("./TAS.py")
sys.path.append("./QAPF.py")
sys.path.append("./QFL.py")
sys.path.append("./QmFt.py")
sys.path.append("./REE.py")

sys.path.append("./Drawer.py")

#import the module first and then you can use the functions in it
import TAS
import QAPF
import QFL
import QmFLt
import REE

import Drawer

setup(console=['Usage.py'])
