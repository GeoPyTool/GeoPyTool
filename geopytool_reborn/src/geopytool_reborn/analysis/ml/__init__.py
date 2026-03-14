# -*- coding: utf-8 -*-
"""
Machine Learning Analysis Module

Contains various ML algorithms for geochemical data analysis.
"""

from .svm import SVMAnalysis
from .lda import LDAAnalysis
from .mlp import MLPAnalysis
from .pca import PCAAnalysis

__all__ = ['SVMAnalysis', 'LDAAnalysis', 'MLPAnalysis', 'PCAAnalysis']