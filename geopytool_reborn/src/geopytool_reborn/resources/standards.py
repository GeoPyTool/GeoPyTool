# -*- coding: utf-8 -*-
"""
Geochemical standards for normalization.

Contains standard values for:
- REE (Rare Earth Elements) normalization
- Trace element normalization
- TAS (Total Alkali-Silica) diagram fields
"""

# =============================================================================
# REE Standards
# =============================================================================

REE_STANDARDS = {
    'C1 Chondrite (Sun & McDonough 1989)': {
        'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
        'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
        'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254
    },
    'Chondrite (Taylor & McLennan 1985)': {
        'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
        'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
        'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381
    },
    'Chondrite (Haskin et al. 1966)': {
        'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185,
        'Eu': 0.071, 'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07,
        'Er': 0.225, 'Tm': 0.03, 'Yb': 0.186, 'Lu': 0.034
    },
    'Chondrite (Nakamura 1977)': {
        'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203,
        'Eu': 0.077, 'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07,
        'Er': 0.225, 'Tm': 0.03, 'Yb': 0.22, 'Lu': 0.034
    },
    'MORB (Sun & McDonough 1989)': {
        'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63,
        'Eu': 1.02, 'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052,
        'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05, 'Lu': 0.46
    },
    'UCC (Rudnick & Gao 2003)': {
        'La': 31, 'Ce': 63, 'Pr': 7.1, 'Nd': 27, 'Sm': 4.7,
        'Eu': 1, 'Gd': 4, 'Tb': 0.7, 'Dy': 3.9, 'Ho': 0.83,
        'Er': 2.3, 'Tm': 0.3, 'Yb': 1.96, 'Lu': 0.31
    }
}

# REE element order for plotting
REE_ELEMENTS = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
LREE = ['La', 'Ce', 'Pr', 'Nd']
MREE = ['Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho']
HREE = ['Er', 'Tm', 'Yb', 'Lu']

# =============================================================================
# Trace Element Standards
# =============================================================================

TRACE_STANDARDS = {
    'PM (Sun & McDonough 1989)': {
        'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02,
        'Th': 0.085, 'U': 0.021, 'Nb': 0.713, 'Ta': 0.041, 'K': 250,
        'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063,
        'Sr': 21.1, 'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444,
        'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17, 'Sb': 0.005,
        'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.736, 'Li': 1.6,
        'Y': 4.55, 'Ho': 0.164, 'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074
    },
    'OIB (Sun & McDonough 1989)': {
        'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56,
        'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7, 'K': 12000,
        'La': 36, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4,
        'Sr': 660, 'P': 2700, 'Nd': 38.5, 'F': 1150, 'Sm': 10,
        'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03,
        'Ti': 17200, 'Gd': 7.62, 'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6,
        'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3
    },
    'E-MORB (Sun & McDonough 1989)': {
        'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092,
        'Th': 0.6, 'U': 0.18, 'Nb': 8.3, 'Ta': 0.47, 'K': 2100,
        'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47,
        'Sr': 155, 'P': 620, 'Nd': 9, 'F': 250, 'Sm': 2.6,
        'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01,
        'Ti': 6000, 'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5,
        'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356, 'Yb': 2.36, 'Lu': 0.354
    },
    'N-MORB (Sun & McDonough 1989)': {
        'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01,
        'Th': 0.12, 'U': 0.047, 'Nb': 2.33, 'Ta': 0.132, 'K': 600,
        'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31,
        'Sr': 90, 'P': 510, 'Nd': 7.3, 'F': 210, 'Sm': 2.63,
        'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01,
        'Ti': 7600, 'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3,
        'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456, 'Yb': 3.05, 'Lu': 0.455
    },
    'C1 Chondrite (Sun & McDonough 1989)': {
        'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095,
        'Th': 0.029, 'U': 0.008, 'Nb': 0.246, 'Ta': 0.014, 'K': 545,
        'La': 0.236, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92,
        'Sr': 7.26, 'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153,
        'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72, 'Sb': 0.16,
        'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0364, 'Dy': 0.254, 'Li': 1.57,
        'Y': 1.57, 'Ho': 0.0566, 'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254
    },
    'UCC (Rudnick & Gao 2003)': {
        'K': 23244.14, 'Ti': 3835.79, 'P': 654.63, 'Li': 24, 'Be': 2.1,
        'B': 17, 'N': 83, 'F': 557, 'S': 62, 'Cl': 370, 'Sc': 14,
        'V': 97, 'Cr': 92, 'Co': 17.3, 'Ni': 47, 'Cu': 28, 'Zn': 67,
        'Ga': 17.5, 'Ge': 1.4, 'As': 4.8, 'Se': 0.09, 'Br': 1.6,
        'Rb': 84, 'Sr': 320, 'Y': 21, 'Zr': 193, 'Nb': 12, 'Mo': 1.1,
        'Ru': 0.34, 'Pd': 0.52, 'Ag': 53, 'Cd': 0.09, 'In': 0.056,
        'Sn': 2.1, 'Sb': 0.4, 'I': 1.4, 'Cs': 4.9, 'Ba': 628,
        'La': 31, 'Ce': 63, 'Pr': 7.1, 'Nd': 27, 'Sm': 4.7, 'Eu': 1,
        'Gd': 4, 'Tb': 0.7, 'Dy': 3.9, 'Ho': 0.83, 'Er': 2.3, 'Tm': 0.3,
        'Yb': 1.96, 'Lu': 0.31, 'Hf': 5.3, 'Ta': 0.9, 'W': 1.9,
        'Re': 0.198, 'Os': 0.031, 'Ir': 0.022, 'Pt': 0.5, 'Au': 1.5,
        'Hg': 0.05, 'Tl': 0.9, 'Pb': 17, 'Bi': 0.16, 'Th': 10.5, 'U': 2.7
    }
}

# Trace element order for full spider diagram
TRACE_ELEMENTS_FULL = [
    'Cs', 'Tl', 'Rb', 'Ba', 'W', 'Th', 'U', 'Nb', 'Ta', 'K',
    'La', 'Ce', 'Pb', 'Pr', 'Mo', 'Sr', 'P', 'Nd', 'F', 'Sm',
    'Zr', 'Hf', 'Eu', 'Sn', 'Sb', 'Ti', 'Gd', 'Tb', 'Dy', 'Li',
    'Y', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'
]

# Abbreviated trace element order (Rb-Lu)
TRACE_ELEMENTS_SHORT = [
    'Rb', 'Ba', 'Th', 'U', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Pb',
    'Pr', 'Sr', 'P', 'Nd', 'Zr', 'Hf', 'Sm', 'Eu', 'Ti', 'Gd',
    'Tb', 'Dy', 'Y', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'
]

# =============================================================================
# TAS Diagram Data
# =============================================================================

# TAS field boundaries (polygon vertices as [SiO2, Na2O+K2O])
TAS_FIELDS = {
    'Foidite': [[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]],
    'Picrobasalt': [[41, 0], [41, 3], [45, 3], [45, 0]],
    'Basanite': [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]],
    'Phonotephrite': [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]],
    'Tephriphonolite': [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]],
    'Phonolite': [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]],
    'Basalt_Bs': [[45, 0], [45, 2], [52, 5], [52, 0]],
    'Basalt_Ba': [[45, 2], [45, 5], [52, 5]],
    'Trachybasalt': [[45, 5], [49.4, 7.3], [52, 5]],
    'Basaltic_Trachyandesite': [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]],
    'Trachyandesite': [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]],
    'Trachyte': [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]],
    'Trachydacite': [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]],
    'Basaltic_Andesite': [[52, 0], [52, 5], [57, 5.9], [57, 0]],
    'Andesite': [[57, 0], [57, 5.9], [63, 7], [63, 0]],
    'Dacite': [[63, 0], [63, 7], [69, 8], [77.3, 0]],
    'Rhyolite': [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]],
    'Quartzolite': [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]]
}

# Volcanic rock names for TAS
TAS_LABELS_VOLCANIC = {
    'Foidite': 'Foidite', 'Picrobasalt': 'Picrobasalt',
    'Basanite': 'Tephrite\nBasanite', 'Phonotephrite': 'Phono-\ntephrite',
    'Tephriphonolite': 'Tephri-\nphonolite', 'Phonolite': 'Phonolite',
    'Basalt_Bs': 'Subalkalic\nBasalt', 'Basalt_Ba': 'Alkalic\nBasalt',
    'Trachybasalt': 'Trachybasalt', 'Basaltic_Trachyandesite': 'Basaltic\nTrachyandesite',
    'Trachyandesite': 'Trachy-\nandesite', 'Trachyte': 'Trachyte',
    'Trachydacite': 'Trachydacite', 'Basaltic_Andesite': 'Basaltic\nAndesite',
    'Andesite': 'Andesite', 'Dacite': 'Dacite',
    'Rhyolite': 'Rhyolite', 'Quartzolite': 'Silexite'
}

# Plutonic rock names for TAS
TAS_LABELS_PLUTONIC = {
    'Foidite': 'Foidolite', 'Picrobasalt': 'Peridotgabbro',
    'Basanite': 'Foid Gabbro', 'Phonotephrite': 'Foid\nMonzodiorite',
    'Tephriphonolite': 'Foid\nMonzosyenite', 'Phonolite': 'Foid Syenite',
    'Basalt_Bs': 'Subalkalic\nGabbro', 'Basalt_Ba': 'Alkalic\nGabbro',
    'Trachybasalt': 'Monzogabbro', 'Basaltic_Trachyandesite': 'Monzodiorite',
    'Trachyandesite': 'Monzonite', 'Trachyte': 'Syenite',
    'Trachydacite': 'Quartz\nMonzonite', 'Basaltic_Andesite': 'Gabbroic\nDiorite',
    'Andesite': 'Diorite', 'Dacite': 'Granodiorite',
    'Rhyolite': 'Granite', 'Quartzolite': 'Quartzolite'
}

# TAS label positions (approximate centers of each field)
TAS_LABEL_POSITIONS = {
    'Foidite': (39, 10), 'Picrobasalt': (43, 1.5),
    'Basanite': (44, 6), 'Phonotephrite': (50, 10),
    'Tephriphonolite': (54, 12.5), 'Phonolite': (57, 15.5),
    'Basalt_Bs': (48.5, 1), 'Basalt_Ba': (47, 4),
    'Trachybasalt': (48, 6.2), 'Basaltic_Trachyandesite': (53, 7.2),
    'Trachyandesite': (58, 9.5), 'Trachyte': (64, 13),
    'Trachydacite': (66, 9), 'Basaltic_Andesite': (54.5, 2.5),
    'Andesite': (60, 3.5), 'Dacite': (68, 3.5),
    'Rhyolite': (78, 8), 'Quartzolite': (84, 2)
}

# =============================================================================
# CIPW Norm Database
# =============================================================================

CIPW_DATABASE = {
    'minerals': {
        'Quartz': {'mass': 60.0843, 'density': 2.65},
        'Zircon': {'mass': 183.3031, 'density': 4.56},
        'K2SiO3': {'mass': 154.2803, 'density': 2.5},
        'Anorthite': {'mass': 278.2093, 'density': 2.76},
        'Na2SiO3': {'mass': 122.0632, 'density': 2.4},
        'Acmite': {'mass': 462.0083, 'density': 3.6},
        'Diopside': {'mass': 229.0692, 'density': 3.355},
        'Sphene': {'mass': 196.0625, 'density': 3.5},
        'Hypersthene': {'mass': 112.9055, 'density': 3.508},
        'Albite': {'mass': 524.446, 'density': 2.62},
        'Orthoclase': {'mass': 556.6631, 'density': 2.56},
        'Wollastonite': {'mass': 116.1637, 'density': 2.86},
        'Olivine': {'mass': 165.7267, 'density': 3.684},
        'Perovskite': {'mass': 135.9782, 'density': 4.0},
        'Nepheline': {'mass': 284.1088, 'density': 2.56},
        'Leucite': {'mass': 436.4945, 'density': 2.49},
        'Larnite': {'mass': 172.2431, 'density': 3.27},
        'Kalsilite': {'mass': 316.3259, 'density': 2.6},
        'Apatite': {'mass': 493.3138, 'density': 3.2},
        'Halite': {'mass': 66.44245, 'density': 2.17},
        'Fluorite': {'mass': 94.0762, 'density': 3.18},
        'Anhydrite': {'mass': 136.1376, 'density': 2.96},
        'Thenardite': {'mass': 142.0371, 'density': 2.68},
        'Pyrite': {'mass': 135.9664, 'density': 4.99},
        'Magnesiochromite': {'mass': 192.2946, 'density': 4.43},
        'Chromite': {'mass': 223.8366, 'density': 5.09},
        'Ilmenite': {'mass': 151.7452, 'density': 4.75},
        'Calcite': {'mass': 100.0892, 'density': 2.71},
        'Na2CO3': {'mass': 105.9887, 'density': 2.53},
        'Corundum': {'mass': 101.9613, 'density': 3.98},
        'Rutile': {'mass': 79.8988, 'density': 4.2},
        'Magnetite': {'mass': 231.5386, 'density': 5.2},
        'Hematite': {'mass': 159.6922, 'density': 5.25}
    },
    'oxides': {
        'SiO2': 60.083, 'TiO2': 79.865, 'Al2O3': 101.960077,
        'Fe2O3': 159.687, 'FeO': 71.844, 'MnO': 70.937044,
        'MgO': 40.304, 'CaO': 56.077, 'Na2O': 61.978539,
        'K2O': 94.1956, 'P2O5': 141.942524, 'CO2': 44.009,
        'SO3': 80.057, 'S': 32.06, 'F': 18.998403,
        'Cl': 35.45, 'Sr': 87.62, 'Ba': 137.327,
        'Ni': 58.6934, 'Cr': 51.9961, 'Zr': 91.224
    }
}
