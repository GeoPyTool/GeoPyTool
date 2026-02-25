# -*- coding: utf-8 -*-
"""
Constants module - Atomic masses and mineral properties.
"""

# =============================================================================
# Element Atomic Masses
# =============================================================================

ELEMENT_MASSES = {
    'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.81,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.18,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
    'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938,
    'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.64, 'As': 74.922, 'Se': 78.96, 'Br': 79.904,
    'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.96, 'Tc': 98, 'Ru': 101.07, 'Rh': 102.906,
    'Pd': 106.42, 'Ag': 107.868, 'Cd': 112.411, 'In': 114.818, 'Sn': 118.71,
    'Sb': 121.76, 'Te': 127.6, 'I': 126.904, 'Xe': 131.293, 'Cs': 132.905,
    'Ba': 137.327, 'La': 138.905, 'Ce': 140.116, 'Pr': 140.908, 'Nd': 144.242,
    'Pm': 145, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25, 'Tb': 158.925,
    'Dy': 162.5, 'Ho': 164.93, 'Er': 167.259, 'Tm': 168.934, 'Yb': 173.054,
    'Lu': 174.967, 'Hf': 178.49, 'Ta': 180.948, 'W': 183.84, 'Re': 186.207,
    'Os': 190.23, 'Ir': 192.217, 'Pt': 195.084, 'Au': 196.967, 'Hg': 200.59,
    'Tl': 204.383, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209, 'At': 210,
    'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232.038,
    'Pa': 231.036, 'U': 238.029
}

# =============================================================================
# Oxide Molecular Weights
# =============================================================================

OXIDE_MASSES = {
    'SiO2': 60.0843, 'TiO2': 79.8658, 'Al2O3': 101.9613,
    'Fe2O3': 159.6882, 'FeO': 71.8444, 'MnO': 70.9374,
    'MgO': 40.3044, 'CaO': 56.0774, 'Na2O': 61.9789,
    'K2O': 94.1960, 'P2O5': 141.9445, 'H2O': 18.0153,
    'CO2': 44.0095, 'SO3': 80.0642, 'Cr2O3': 151.9904,
    'NiO': 74.6928, 'BaO': 153.3264, 'SrO': 103.6194,
    'ZrO2': 123.2228
}

# =============================================================================
# Mineral Data for CIPW Calculations
# =============================================================================

MINERAL_DATA = {
    'Quartz': {'formula': 'SiO2', 'mass': 60.0843, 'density': 2.65},
    'Orthoclase': {'formula': 'KAlSi3O8', 'mass': 556.6631, 'density': 2.56},
    'Albite': {'formula': 'NaAlSi3O8', 'mass': 524.446, 'density': 2.62},
    'Anorthite': {'formula': 'CaAl2Si2O8', 'mass': 278.2093, 'density': 2.76},
    'Leucite': {'formula': 'KAlSi2O6', 'mass': 436.4945, 'density': 2.49},
    'Nepheline': {'formula': 'NaAlSiO4', 'mass': 284.1088, 'density': 2.56},
    'Kalsilite': {'formula': 'KAlSiO4', 'mass': 316.3259, 'density': 2.6},
    'Corundum': {'formula': 'Al2O3', 'mass': 101.9613, 'density': 3.98},
    'Diopside': {'formula': 'CaMgSi2O6', 'mass': 229.0692, 'density': 3.355},
    'Hypersthene': {'formula': '(Mg,Fe)SiO3', 'mass': 112.9055, 'density': 3.508},
    'Olivine': {'formula': '(Mg,Fe)2SiO4', 'mass': 165.7267, 'density': 3.684},
    'Wollastonite': {'formula': 'CaSiO3', 'mass': 116.1637, 'density': 2.86},
    'Larnite': {'formula': 'Ca2SiO4', 'mass': 172.2431, 'density': 3.27},
    'Acmite': {'formula': 'NaFeSi2O6', 'mass': 462.0083, 'density': 3.6},
    'Magnetite': {'formula': 'Fe3O4', 'mass': 231.5386, 'density': 5.2},
    'Hematite': {'formula': 'Fe2O3', 'mass': 159.6922, 'density': 5.25},
    'Ilmenite': {'formula': 'FeTiO3', 'mass': 151.7452, 'density': 4.75},
    'Rutile': {'formula': 'TiO2', 'mass': 79.8988, 'density': 4.2},
    'Sphene': {'formula': 'CaTiSiO5', 'mass': 196.0625, 'density': 3.5},
    'Perovskite': {'formula': 'CaTiO3', 'mass': 135.9782, 'density': 4.0},
    'Apatite': {'formula': 'Ca5(PO4)3(F,Cl,OH)', 'mass': 493.3138, 'density': 3.2},
    'Calcite': {'formula': 'CaCOite', 'mass': 100.0892, 'density': 2.71},
    'Pyrite': {'formula': 'FeS2', 'mass': 135.9664, 'density': 4.99},
    'Chromite': {'formula': 'FeCr2O4', 'mass': 223.8366, 'density': 5.09},
    'Zircon': {'formula': 'ZrSiO4', 'mass': 183.3031, 'density': 4.56},
    'Fluorite': {'formula': 'CaF2', 'mass': 94.0762, 'density': 3.18},
    'Halite': {'formula': 'NaCl', 'mass': 66.44245, 'density': 2.17},
    'Anhydrite': {'formula': 'CaSO4', 'mass': 136.1376, 'density': 2.96}
}

# =============================================================================
# Conversion Factors
# =============================================================================

# Conversion from oxide wt% to element ppm
OXIDE_TO_ELEMENT_FACTORS = {
    'K2O_to_K': 8301.6,    # K2O wt% * factor = K ppm
    'TiO2_to_Ti': 5995.0,  # TiO2 wt% * factor = Ti ppm
    'P2O5_to_P': 4364.9,   # P2O5 wt% * factor = P ppm
    'MnO_to_Mn': 7745.0,   # MnO wt% * factor = Mn ppm
}

# =============================================================================
# Pearce Diagram Data
# =============================================================================

PEARCE_DIAGRAMS = {
    'Y+Nb_vs_Rb': {
        'x_label': 'Y+Nb (ppm)',
        'y_label': 'Rb (ppm)',
        'x_scale': 'log',
        'y_scale': 'log',
        'x_lim': (1, 3000),
        'y_lim': (1, 3000),
        'boundaries': [
            [(2, 80), (55, 300)],
            [(55, 300), (400, 2000)],
            [(55, 300), (51.5, 8)],
            [(51.5, 8), (50, 1)],
            [(51.5, 8), (2000, 400)]
        ],
        'fields': {
            'syn-COLG': (10, 1000),
            'VAG': (10, 10),
            'WPG': (250, 250),
            'ORG': (1000, 10)
        }
    },
    'Yb+Ta_vs_Rb': {
        'x_label': 'Yb+Ta (ppm)',
        'y_label': 'Rb (ppm)',
        'x_scale': 'log',
        'y_scale': 'log',
        'x_lim': (0.1, 300),
        'y_lim': (1, 3000),
        'boundaries': [
            [(0.5, 140), (6, 200)],
            [(6, 200), (50, 2000)],
            [(6, 200), (6, 8)],
            [(6, 8), (6, 1)],
            [(6, 8), (200, 400)]
        ],
        'fields': {
            'syn-COLG': (1, 1000),
            'VAG': (1, 10),
            'WPG': (30, 250),
            'ORG': (100, 10)
        }
    },
    'Y_vs_Nb': {
        'x_label': 'Y (ppm)',
        'y_label': 'Nb (ppm)',
        'x_scale': 'log',
        'y_scale': 'log',
        'x_lim': (1, 3000),
        'y_lim': (1, 3000),
        'boundaries': [
            [(1, 2000), (50, 10)],
            [(40, 1), (50, 10)],
            [(50, 10), (1000, 100)],
            [(25, 25), (1000, 400)]
        ],
        'fields': {
            'WPG': (100, 100),
            'ORG': (150, 2),
            'VAG+syn-COLG': (10, 50)
        }
    },
    'Yb_vs_Ta': {
        'x_label': 'Yb (ppm)',
        'y_label': 'Ta (ppm)',
        'x_scale': 'log',
        'y_scale': 'log',
        'x_lim': (0.1, 100),
        'y_lim': (0.01, 100),
        'boundaries': [
            [(0.55, 20), (3, 2)],
            [(0.1, 0.35), (3, 2)],
            [(3, 2), (5, 1)],
            [(5, 0.05), (5, 1)],
            [(5, 1), (100, 7)],
            [(3, 2), (100, 20)]
        ],
        'fields': {
            'syn-COLG': (0.5, 1),
            'VAG': (0.5, 0.1),
            'WPG': (5, 10),
            'ORG': (30, 1)
        }
    }
}
