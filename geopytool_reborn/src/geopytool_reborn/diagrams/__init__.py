# -*- coding: utf-8 -*-
"""
Diagrams module - Geochemical diagram implementations.
"""

from .tas import TAS
from .ree import REE
from .trace import Trace
from .harker import Harker
from .pearce import Pearce
from .triangular.qapf import QAPF
from .triangular.qfl import QFL

__all__ = ['TAS', 'REE', 'Trace', 'Harker', 'Pearce', 'QAPF', 'QFL']
