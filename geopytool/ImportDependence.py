#coding:utf-8
import matplotlib
matplotlib.use('Qt5Agg')

import importlib

'''
try:
    importlib.import_module(package)
except ImportError:
    import pip

    pip.main(['install', package])
finally:
    globals()[package] = importlib.import_module(package)
'''

import pip
import subprocess

import webbrowser
import sys
import sklearn as sk

from sklearn.neural_network import MLPClassifier,BernoulliRBM

#import vispy.app, vispy.visuals, vispy.scene, vispy.plot, vispy.io, vispy.color
#import sklearn_pandas as skpd

import scipy.stats as st

from scipy.interpolate import make_interp_spline, BSpline


from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import requests
import re
import random
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import path
import matplotlib.patches as patches
import matplotlib.image as mpimg
import matplotlib.font_manager as font_manager
import matplotlib.backends.backend_pdf
import math
import csv
from xml.dom import minidom
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer, Binarizer, LabelEncoder, OneHotEncoder,  PolynomialFeatures, FunctionTransformer
from sklearn.neighbors import NearestNeighbors, KernelDensity
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import PCA, FastICA, FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from sklearn import svm
from sklearn import tree
from sklearn import datasets
from scipy.stats import mode, gaussian_kde
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy as hc
from scipy.signal import find_peaks, find_peaks_cwt, fftconvolve

from itertools import product, combinations, permutations, repeat

from PyQt5.QtWidgets import QMainWindow, QMenu, QSizePolicy, QMessageBox, QWidget, QFileDialog, QAction, QTextEdit, QLineEdit, QApplication, QPushButton, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QProxyStyle, QStyle, qApp, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import vstack, array, nan, mean, median, ptp, var, std, cov, corrcoef, arange, sin, pi , nanmean, nanmedian, nanvar, nanstd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import ttfFontProperty
import matplotlib.tri as tri
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import cm
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib import ft2font
from bs4 import BeautifulSoup
#from TableViewer import TableViewer



from sklearn import mixture
import keras
from keras.layers import Conv1D, Flatten, Dense, Dropout, Input, Activation, Reshape
from keras.models import Model,Sequential
from keras.datasets import mnist
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import SGD, Adam
from tqdm import tqdm_notebook as tqdm  # 进度条

import tensorflow as tf

from keras.layers import Input, Dense, Lambda, concatenate
from keras.models import Model
from keras.optimizers import Adam
import keras.backend as K

import os
import random
import gym
from collections import deque

import numpy as np
import tensorflow as tf

from keras.layers import Input, Dense, Lambda, concatenate
from keras.models import Model
from keras.optimizers import Adam
import keras.backend as K




LocationOfMySelf=os.path.dirname(__file__)

#print(LocationOfMySelf, 'Import Denpendence')

fpath = LocationOfMySelf+('/wqy.ttf')

font = ft2font.FT2Font(fpath)
fprop = font_manager.FontProperties(fname=fpath)

ttfFontProp = ttfFontProperty(font)
fontprop = font_manager.FontProperties(family='sans-serif', 
                            size=9, 
                            fname=ttfFontProp.fname, 
                            stretch=ttfFontProp.stretch, 
                            style=ttfFontProp.style, 
                            variant=ttfFontProp.variant, 
                            weight=ttfFontProp.weight)


'''
fontprop = font_manager.FontProperties(family='sans-serif', 
                            size=9, 
                            fname=ttfFontProp.fname, 
                            stretch=ttfFontProp.stretch, 
                            style=ttfFontProp.style, 
                            variant=ttfFontProp.variant, 
                            weight=ttfFontProp.weight)
'''

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['axes.unicode_minus']=False


_translate = QtCore.QCoreApplication.translate