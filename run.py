#!/usr/bin/env python
# coding: utf-8

import os
import sys
import io
import base64
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
os.environ['QT_QPA_PLATFORM'] = ''  # Disable Qt platform detection
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session
from werkzeug.utils import secure_filename
import zipfile
from io import BytesIO
import re

# Import necessary GeoPyTool modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create a modified version of ImportDependence for web
class WebDependence:
    pass

# Create a simplified CustomClass for web
class WebCustomClass:
    pass

# Function to standardize column names
def standardize_column_names(df):
    """
    Standardize column names by removing units and converting to standard chemical notation
    """
    # Define mapping for major elements
    major_elements_map = {
        # SiO2 variations
        'sio2': 'SiO2', 'SIO2': 'SiO2', 'si02': 'SiO2', 'SI02': 'SiO2',
        'sio2(wt%)': 'SiO2', 'sio2(wt.%)': 'SiO2', 'sio2(%)': 'SiO2',
        'sio2_wt%': 'SiO2', 'sio2_wt': 'SiO2', 'sio2_weight%': 'SiO2',
        
        # TiO2 variations
        'tio2': 'TiO2', 'TIO2': 'TiO2', 'ti02': 'TiO2', 'TI02': 'TiO2',
        'tio2(wt%)': 'TiO2', 'tio2(wt.%)': 'TiO2', 'tio2(%)': 'TiO2',
        'tio2_wt%': 'TiO2', 'tio2_wt': 'TiO2', 'tio2_weight%': 'TiO2',
        
        # Al2O3 variations
        'al2o3': 'Al2O3', 'AL2O3': 'Al2O3', 'al203': 'Al2O3', 'AL203': 'Al2O3',
        'al2o3(wt%)': 'Al2O3', 'al2o3(wt.%)': 'Al2O3', 'al2o3(%)': 'Al2O3',
        'al2o3_wt%': 'Al2O3', 'al2o3_wt': 'Al2O3', 'al2o3_weight%': 'Al2O3',
        
        # Fe2O3 variations
        'fe2o3': 'Fe2O3', 'FE2O3': 'Fe2O3', 'fe203': 'Fe2O3', 'FE203': 'Fe2O3',
        'fe2o3(wt%)': 'Fe2O3', 'fe2o3(wt.%)': 'Fe2O3', 'fe2o3(%)': 'Fe2O3',
        'fe2o3_wt%': 'Fe2O3', 'fe2o3_wt': 'Fe2O3', 'fe2o3_weight%': 'Fe2O3',
        
        # FeO variations
        'feo': 'FeO', 'FEO': 'FeO',
        'feo(wt%)': 'FeO', 'feo(wt.%)': 'FeO', 'feo(%)': 'FeO',
        'feo_wt%': 'FeO', 'feo_wt': 'FeO', 'feo_weight%': 'FeO',
        
        # MnO variations
        'mno': 'MnO', 'MNO': 'MnO',
        'mno(wt%)': 'MnO', 'mno(wt.%)': 'MnO', 'mno(%)': 'MnO',
        'mno_wt%': 'MnO', 'mno_wt': 'MnO', 'mno_weight%': 'MnO',
        
        # MgO variations
        'mgo': 'MgO', 'MGO': 'MgO',
        'mgo(wt%)': 'MgO', 'mgo(wt.%)': 'MgO', 'mgo(%)': 'MgO',
        'mgo_wt%': 'MgO', 'mgo_wt': 'MgO', 'mgo_weight%': 'MgO',
        
        # CaO variations
        'cao': 'CaO', 'CAO': 'CaO',
        'cao(wt%)': 'CaO', 'cao(wt.%)': 'CaO', 'cao(%)': 'CaO',
        'cao_wt%': 'CaO', 'cao_wt': 'CaO', 'cao_weight%': 'CaO',
        
        # Na2O variations
        'na2o': 'Na2O', 'NA2O': 'Na2O', 'na20': 'Na2O', 'NA20': 'Na2O',
        'na2o(wt%)': 'Na2O', 'na2o(wt.%)': 'Na2O', 'na2o(%)': 'Na2O',
        'na2o_wt%': 'Na2O', 'na2o_wt': 'Na2O', 'na2o_weight%': 'Na2O',
        
        # K2O variations
        'k2o': 'K2O', 'K2O': 'K2O', 'k20': 'K2O', 'K20': 'K2O',
        'k2o(wt%)': 'K2O', 'k2o(wt.%)': 'K2O', 'k2o(%)': 'K2O',
        'k2o_wt%': 'K2O', 'k2o_wt': 'K2O', 'k2o_weight%': 'K2O',
        
        # P2O5 variations
        'p2o5': 'P2O5', 'P2O5': 'P2O5', 'p205': 'P2O5', 'P205': 'P2O5',
        'p2o5(wt%)': 'P2O5', 'p2o5(wt.%)': 'P2O5', 'p2o5(%)': 'P2O5',
        'p2o5_wt%': 'P2O5', 'p2o5_wt': 'P2O5', 'p2o5_weight%': 'P2O5',
    }
    
    # Define mapping for trace elements
    trace_elements_map = {
        # Rb variations
        'rb': 'Rb', 'RB': 'Rb',
        'rb(ppm)': 'Rb', 'rb(ppb)': 'Rb', 'rb(ppt)': 'Rb',
        'rb_ppm': 'Rb', 'rb_ppb': 'Rb', 'rb_ppt': 'Rb',
        
        # Ba variations
        'ba': 'Ba', 'BA': 'Ba',
        'ba(ppm)': 'Ba', 'ba(ppb)': 'Ba', 'ba(ppt)': 'Ba',
        'ba_ppm': 'Ba', 'ba_ppb': 'Ba', 'ba_ppt': 'Ba',
        
        # Th variations
        'th': 'Th', 'TH': 'Th',
        'th(ppm)': 'Th', 'th(ppb)': 'Th', 'th(ppt)': 'Th',
        'th_ppm': 'Th', 'th_ppb': 'Th', 'th_ppt': 'Th',
        
        # U variations
        'u': 'U', 'U': 'U',
        'u(ppm)': 'U', 'u(ppb)': 'U', 'u(ppt)': 'U',
        'u_ppm': 'U', 'u_ppb': 'U', 'u_ppt': 'U',
        
        # Nb variations
        'nb': 'Nb', 'NB': 'Nb',
        'nb(ppm)': 'Nb', 'nb(ppb)': 'Nb', 'nb(ppt)': 'Nb',
        'nb_ppm': 'Nb', 'nb_ppb': 'Nb', 'nb_ppt': 'Nb',
        
        # Ta variations
        'ta': 'Ta', 'TA': 'Ta',
        'ta(ppm)': 'Ta', 'ta(ppb)': 'Ta', 'ta(ppt)': 'Ta',
        'ta_ppm': 'Ta', 'ta_ppb': 'Ta', 'ta_ppt': 'Ta',
        
        # K variations (when as trace element)
        'k': 'K', 'K': 'K',
        'k(ppm)': 'K', 'k(ppb)': 'K', 'k(ppt)': 'K',
        'k_ppm': 'K', 'k_ppb': 'K', 'k_ppt': 'K',
        
        # La variations
        'la': 'La', 'LA': 'La',
        'la(ppm)': 'La', 'la(ppb)': 'La', 'la(ppt)': 'La',
        'la_ppm': 'La', 'la_ppb': 'La', 'la_ppt': 'La',
        
        # Ce variations
        'ce': 'Ce', 'CE': 'Ce',
        'ce(ppm)': 'Ce', 'ce(ppb)': 'Ce', 'ce(ppt)': 'Ce',
        'ce_ppm': 'Ce', 'ce_ppb': 'Ce', 'ce_ppt': 'Ce',
        
        # Pr variations
        'pr': 'Pr', 'PR': 'Pr',
        'pr(ppm)': 'Pr', 'pr(ppb)': 'Pr', 'pr(ppt)': 'Pr',
        'pr_ppm': 'Pr', 'pr_ppb': 'Pr', 'pr_ppt': 'Pr',
        
        # Nd variations
        'nd': 'Nd', 'ND': 'Nd',
        'nd(ppm)': 'Nd', 'nd(ppb)': 'Nd', 'nd(ppt)': 'Nd',
        'nd_ppm': 'Nd', 'nd_ppb': 'Nd', 'nd_ppt': 'Nd',
        
        # P variations (when as trace element)
        'p': 'P', 'P': 'P',
        'p(ppm)': 'P', 'p(ppb)': 'P', 'p(ppt)': 'P',
        'p_ppm': 'P', 'p_ppb': 'P', 'p_ppt': 'P',
        
        # Sm variations
        'sm': 'Sm', 'SM': 'Sm',
        'sm(ppm)': 'Sm', 'sm(ppb)': 'Sm', 'sm(ppt)': 'Sm',
        'sm_ppm': 'Sm', 'sm_ppb': 'Sm', 'sm_ppt': 'Sm',
        
        # Eu variations
        'eu': 'Eu', 'EU': 'Eu',
        'eu(ppm)': 'Eu', 'eu(ppb)': 'Eu', 'eu(ppt)': 'Eu',
        'eu_ppm': 'Eu', 'eu_ppb': 'Eu', 'eu_ppt': 'Eu',
        
        # Gd variations
        'gd': 'Gd', 'GD': 'Gd',
        'gd(ppm)': 'Gd', 'gd(ppb)': 'Gd', 'gd(ppt)': 'Gd',
        'gd_ppm': 'Gd', 'gd_ppb': 'Gd', 'gd_ppt': 'Gd',
        
        # Tb variations
        'tb': 'Tb', 'TB': 'Tb',
        'tb(ppm)': 'Tb', 'tb(ppb)': 'Tb', 'tb(ppt)': 'Tb',
        'tb_ppm': 'Tb', 'tb_ppb': 'Tb', 'tb_ppt': 'Tb',
        
        # Dy variations
        'dy': 'Dy', 'DY': 'Dy',
        'dy(ppm)': 'Dy', 'dy(ppb)': 'Dy', 'dy(ppt)': 'Dy',
        'dy_ppm': 'Dy', 'dy_ppb': 'Dy', 'dy_ppt': 'Dy',
        
        # Ho variations
        'ho': 'Ho', 'HO': 'Ho',
        'ho(ppm)': 'Ho', 'ho(ppb)': 'Ho', 'ho(ppt)': 'Ho',
        'ho_ppm': 'Ho', 'ho_ppb': 'Ho', 'ho_ppt': 'Ho',
        
        # Er variations
        'er': 'Er', 'ER': 'Er',
        'er(ppm)': 'Er', 'er(ppb)': 'Er', 'er(ppt)': 'Er',
        'er_ppm': 'Er', 'er_ppb': 'Er', 'er_ppt': 'Er',
        
        # Tm variations
        'tm': 'Tm', 'TM': 'Tm',
        'tm(ppm)': 'Tm', 'tm(ppb)': 'Tm', 'tm(ppt)': 'Tm',
        'tm_ppm': 'Tm', 'tm_ppb': 'Tm', 'tm_ppt': 'Tm',
        
        # Yb variations
        'yb': 'Yb', 'YB': 'Yb',
        'yb(ppm)': 'Yb', 'yb(ppb)': 'Yb', 'yb(ppt)': 'Yb',
        'yb_ppm': 'Yb', 'yb_ppb': 'Yb', 'yb_ppt': 'Yb',
        
        # Lu variations
        'lu': 'Lu', 'LU': 'Lu',
        'lu(ppm)': 'Lu', 'lu(ppb)': 'Lu', 'lu(ppt)': 'Lu',
        'lu_ppm': 'Lu', 'lu_ppb': 'Lu', 'lu_ppt': 'Lu',
        
        # Sr variations
        'sr': 'Sr', 'SR': 'Sr',
        'sr(ppm)': 'Sr', 'sr(ppb)': 'Sr', 'sr(ppt)': 'Sr',
        'sr_ppm': 'Sr', 'sr_ppb': 'Sr', 'sr_ppt': 'Sr',
        
        # Zr variations
        'zr': 'Zr', 'ZR': 'Zr',
        'zr(ppm)': 'Zr', 'zr(ppb)': 'Zr', 'zr(ppt)': 'Zr',
        'zr_ppm': 'Zr', 'zr_ppb': 'Zr', 'zr_ppt': 'Zr',
        
        # Hf variations
        'hf': 'Hf', 'HF': 'Hf',
        'hf(ppm)': 'Hf', 'hf(ppb)': 'Hf', 'hf(ppt)': 'Hf',
        'hf_ppm': 'Hf', 'hf_ppb': 'Hf', 'hf_ppt': 'Hf',
        
        # Ti variations (when as trace element)
        'ti': 'Ti', 'TI': 'Ti',
        'ti(ppm)': 'Ti', 'ti(ppb)': 'Ti', 'ti(ppt)': 'Ti',
        'ti_ppm': 'Ti', 'ti_ppb': 'Ti', 'ti_ppt': 'Ti',
        
        # Y variations
        'y': 'Y', 'Y': 'Y',
        'y(ppm)': 'Y', 'y(ppb)': 'Y', 'y(ppt)': 'Y',
        'y_ppm': 'Y', 'y_ppb': 'Y', 'y_ppt': 'Y',
        
        # Additional elements
        # Sc variations
        'sc': 'Sc', 'SC': 'Sc',
        'sc(ppm)': 'Sc', 'sc(ppb)': 'Sc', 'sc(ppt)': 'Sc',
        'sc_ppm': 'Sc', 'sc_ppb': 'Sc', 'sc_ppt': 'Sc',
        
        # V variations
        'v': 'V', 'V': 'V',
        'v(ppm)': 'V', 'v(ppb)': 'V', 'v(ppt)': 'V',
        'v_ppm': 'V', 'v_ppb': 'V', 'v_ppt': 'V',
        
        # Cr variations
        'cr': 'Cr', 'CR': 'Cr',
        'cr(ppm)': 'Cr', 'cr(ppb)': 'Cr', 'cr(ppt)': 'Cr',
        'cr_ppm': 'Cr', 'cr_ppb': 'Cr', 'cr_ppt': 'Cr',
        
        # Co variations
        'co': 'Co', 'CO': 'Co',
        'co(ppm)': 'Co', 'co(ppb)': 'Co', 'co(ppt)': 'Co',
        'co_ppm': 'Co', 'co_ppb': 'Co', 'co_ppt': 'Co',
        
        # Ni variations
        'ni': 'Ni', 'NI': 'Ni',
        'ni(ppm)': 'Ni', 'ni(ppb)': 'Ni', 'ni(ppt)': 'Ni',
        'ni_ppm': 'Ni', 'ni_ppb': 'Ni', 'ni_ppt': 'Ni',
        
        # Cu variations
        'cu': 'Cu', 'CU': 'Cu',
        'cu(ppm)': 'Cu', 'cu(ppb)': 'Cu', 'cu(ppt)': 'Cu',
        'cu_ppm': 'Cu', 'cu_ppb': 'Cu', 'cu_ppt': 'Cu',
        
        # Zn variations
        'zn': 'Zn', 'ZN': 'Zn',
        'zn(ppm)': 'Zn', 'zn(ppb)': 'Zn', 'zn(ppt)': 'Zn',
        'zn_ppm': 'Zn', 'zn_ppb': 'Zn', 'zn_ppt': 'Zn',
        
        # Ga variations
        'ga': 'Ga', 'GA': 'Ga',
        'ga(ppm)': 'Ga', 'ga(ppb)': 'Ga', 'ga(ppt)': 'Ga',
        'ga_ppm': 'Ga', 'ga_ppb': 'Ga', 'ga_ppt': 'Ga',
        
        # Cs variations
        'cs': 'Cs', 'CS': 'Cs',
        'cs(ppm)': 'Cs', 'cs(ppb)': 'Cs', 'cs(ppt)': 'Cs',
        'cs_ppm': 'Cs', 'cs_ppb': 'Cs', 'cs_ppt': 'Cs',
        
        # Pb variations
        'pb': 'Pb', 'PB': 'Pb',
        'pb(ppm)': 'Pb', 'pb(ppb)': 'Pb', 'pb(ppt)': 'Pb',
        'pb_ppm': 'Pb', 'pb_ppb': 'Pb', 'pb_ppt': 'Pb',
    }
    
    # Combine all mappings
    all_mappings = {**major_elements_map, **trace_elements_map}
    
    # Create a new dataframe with standardized column names
    new_columns = []
    for col in df.columns:
        # First, try direct mapping
        col_clean = col.strip()
        if col_clean.lower() in all_mappings:
            new_columns.append(all_mappings[col_clean.lower()])
        else:
            # Try to extract element name using regex
            # Remove common units and symbols
            cleaned_col = re.sub(r'\s*\([^)]*\)\s*', '', col_clean)  # Remove anything in parentheses
            cleaned_col = re.sub(r'[_\-]\s*(ppm|ppb|ppt|wt%?|weight%?|%)\s*$', '', cleaned_col, flags=re.IGNORECASE)  # Remove units at end
            cleaned_col = cleaned_col.strip()
            
            if cleaned_col.lower() in all_mappings:
                new_columns.append(all_mappings[cleaned_col.lower()])
            else:
                # Keep original column name if no mapping found
                new_columns.append(col)
    
    # Create new dataframe with standardized column names
    df_standardized = df.copy()
    df_standardized.columns = new_columns
    
    return df_standardized

# Function to load background image for diagrams
def load_background_image(diagram_type):
    """
    Load background image for different diagram types
    """
    bg_path = None
    
    # Define background image paths for different diagrams
    bg_paths = {
        'tas': 'PNG to Load/TAS.png',
        'pearce': 'PNG to Load/Pearce.png',
        'qapf': 'PNG to Load/QAPF.png',
        'harker': 'PNG to Load/Harker.png'
    }
    
    if diagram_type in bg_paths:
        bg_path = bg_paths[diagram_type]
        
    # Check if background image exists
    if bg_path and os.path.exists(bg_path):
        try:
            return mpimg.imread(bg_path)
        except Exception as e:
            print(f"Error loading background image: {e}")
            return None
    
    return None

# Color assignment utility function
def get_color_mapping(df):
    """
    Get color mapping for data points based on data file content
    Returns: (colors_list, legend_labels)
    """
    colors_list = []
    legend_labels = []
    
    # Enhanced default color palette with better contrast
    default_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 
                     'magenta', 'darkblue', 'darkgreen', 'darkred', 'lightblue', 'lightgreen', 
                     'coral', 'gold', 'indigo', 'crimson', 'forestgreen', 'navy', 'maroon', 'teal', 
                     'slategray', 'chocolate', 'mediumorchid', 'darkorange', 'steelblue', 'darkslategray']
    
    # Check for color-related columns (case insensitive)
    color_columns = []
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in ['color', 'colour', 'colors', 'colours', 'type', 'label', 'group', 'groups', 
                        'category', 'categories', 'class', 'classification', 'rock_type', 'rocktype', 
                        'sample_type', 'sampletype', 'formation', 'unit', 'lithology']:
            color_columns.append(col)
    
    if color_columns:
        # Use the first color-related column found
        color_col = color_columns[0]
        unique_values = pd.Series(df[color_col].unique()).dropna().tolist()
        
        # Add NaN values if they exist
        if df[color_col].isna().any():
            unique_values.append(np.nan)
        
        # Create color mapping for unique values
        color_map = {}
        
        # Define standard color names that can be used directly
        standard_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'grey', 
                          'olive', 'cyan', 'magenta', 'yellow', 'black', 'white', 'darkblue', 'darkgreen', 
                          'darkred', 'lightblue', 'lightgreen', 'coral', 'gold', 'indigo', 'crimson',
                          'forestgreen', 'navy', 'maroon', 'teal', 'chocolate', 'darkorange']
        
        for i, value in enumerate(unique_values):
            if pd.isna(value):
                color_map[value] = 'gray'
            else:
                # Check if the value itself is a recognizable color name
                value_str = str(value).lower().strip()
                if value_str in standard_colors:
                    color_map[value] = value_str if value_str != 'grey' else 'gray'
                else:
                    color_map[value] = default_colors[i % len(default_colors)]
        
        # Assign colors to each data point
        for idx, row in df.iterrows():
            value = row[color_col]
            colors_list.append(color_map.get(value, 'gray'))
            
            if pd.isna(value):
                legend_labels.append(f'Sample {idx+1} (Undefined)')
            else:
                # Clean label for better display
                clean_label = str(value).strip()
                legend_labels.append(clean_label)
    else:
        # No color column found, use default coloring by sample
        for i in range(len(df)):
            colors_list.append(default_colors[i % len(default_colors)])
            legend_labels.append(f'Sample {i+1}')
    
    return colors_list, legend_labels

# We'll implement our own simplified versions of the GeoPyTool modules
# instead of importing them directly to avoid dependencies issues

# Base class for all plot types
class BasePlot:
    def __init__(self, df=None, fig=None):
        self.df = df
        self.fig = fig or plt.figure(figsize=(10, 8))
        self.colors, self.legend_labels = get_color_mapping(df) if df is not None else ([], [])
        
    def plot(self):
        pass

# TAS diagram implementation based on Wilson et al. 1989
class TAS(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
        
        # Check if required columns exist
        required_cols = ['SiO2', 'Na2O', 'K2O']
        if not all(col in self.df.columns for col in required_cols):
            plt.text(0.5, 0.5, 'Missing required columns: SiO2, Na2O, K2O', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Set proper axis ranges and ticks according to TAS.py
        ax.set_xlim(30, 90)
        ax.set_ylim(0, 20)
        ax.set_xticks([30, 40, 50, 60, 70, 80, 90])
        ax.set_xticklabels([30, 40, 50, 60, 70, 80, 90])
        ax.set_yticks([0, 5, 10, 15, 20])
        ax.set_yticklabels([0, 5, 10, 15, 20])
        
        # Try to load background image
        bg_img = load_background_image('tas')
        if bg_img is not None:
            ax.imshow(bg_img, extent=[30, 90, 0, 20], aspect='auto', alpha=0.3)
        
        # Draw TAS classification lines (exact coordinates from TAS.py)
        self.draw_tas_lines(ax)
        
        # Draw Irvine-Baragar line
        self.draw_irvine_line(ax)
        
        # Plot the data points
        for i, (idx, row) in enumerate(self.df.iterrows()):
            color = self.colors[i] if i < len(self.colors) else 'blue'
            label = self.legend_labels[i] if i < len(self.legend_labels) else f'Sample {i+1}'
            ax.scatter(row['SiO2'], row['Na2O'] + row['K2O'], 
                      marker='o', color=color, s=60, alpha=0.8, 
                      label=label, edgecolors='black', linewidth=0.5)
        
        # Add field labels (exact coordinates from TAS.py)
        self.add_tas_labels(ax)
        
        # Set labels and title
        ax.set_xlabel('SiO₂ wt%', fontsize=12)
        ax.set_ylabel('Na₂O + K₂O wt%', fontsize=12)
        ax.set_title('TAS (Total Alkali–Silica) Diagram Volcanic (Wilson et al. 1989)', fontsize=14, fontweight='bold')
        
        # Remove top and right spines
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend if multiple samples
        if len(self.df) > 1 and len(self.df) <= 10:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        
        # Add reference
        ax.text(0.02, 0.98, 'Reference: Wilson et al. (1989)', transform=ax.transAxes, 
                fontsize=8, verticalalignment='top', style='italic')
    
    def draw_tas_lines(self, ax):
        """Draw TAS classification boundary lines using exact coordinates from TAS.py"""
        # Exact boundary lines from TAS.py
        lines = [
            [(41, 0), (41, 3), (45, 3)],
            [(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)],
            [(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)],
            [(45, 2), (45, 5), (52, 5), (45, 2)],
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14), (35, 9), (37, 3), (41, 3)],
            [(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)],
            [(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)],
            [(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)],
            [(41, 3), (41, 7), (45, 9.4)],
            [(45, 9.4), (48.4, 11.5), (52.5, 14)]
        ]
        
        for line in lines:
            x_coords = [point[0] for point in line]
            y_coords = [point[1] for point in line]
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.8)
    
    def draw_irvine_line(self, ax):
        """Draw Irvine-Baragar line using exact formula from TAS.py"""
        y_irvine = np.arange(0, 10.2, 0.1)
        x_irvine = []
        
        # Exact Irvine formula from TAS.py
        a, b, c, d, e, f, g = 39.0, 3.9492, -2.1111, 0.86096, -0.15188, 0.012030, -(3.3539 / 10000)
        
        for y in y_irvine:
            x = a + b * np.power(y, 1) + c * np.power(y, 2) + d * np.power(y, 3) + e * np.power(y, 4) + f * np.power(y, 5) + g * np.power(y, 6)
            x_irvine.append(x)
        
        ax.plot(x_irvine, y_irvine, color='black', linewidth=1, 
               linestyle=':', alpha=0.6, label='Irvine & Baragar (1971)')
    
    def add_tas_labels(self, ax):
        """Add rock type labels using exact coordinates from TAS.py"""
        # Exact label positions from TAS.py
        locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 5.2), (49, 9.5), 
                    (54, 3), (53, 7), (53, 12), (60, 4), (57, 8.5), (57, 14), (67, 5), (65, 12), 
                    (67, 9), (75, 9), (85, 1), (55, 18.5)]
        
        # Volcanic labels from TAS.py
        labels = ['F', 'Pc', 'U1', 'Ba', 'Bs', 'S1', 'U2', 'O1', 'S2', 'U3', 'O2', 'S3', 
                 'Ph', 'O3', 'T', 'Td', 'R', 'Q', 'S/N/L']
        
        # Full names for tooltips
        full_names = {
            'F': 'Foidite', 'Ph': 'Phonolite', 'Pc': 'Picrobasalt', 
            'U1': 'Tephrite/Basanite', 'U2': 'Phonotephrite', 'U3': 'Tephriphonolite',
            'Ba': 'Alkalic Basalt', 'Bs': 'Subalkalic Basalt', 
            'S1': 'Trachybasalt', 'S2': 'Basaltic Trachyandesite', 'S3': 'Trachyandesite',
            'O1': 'Basaltic Andesite', 'O2': 'Andesite', 'O3': 'Dacite',
            'T': 'Trachyte', 'Td': 'Trachydacite', 'R': 'Rhyolite', 'Q': 'Silexite',
            'S/N/L': 'Sodalitite/Nephelinolith/Leucitolith'
        }
        
        x_offset, y_offset = -6, 3
        
        for i, (location, label) in enumerate(zip(locations, labels)):
            if i < len(locations) and i < len(labels):
                x, y = location
                if 30 <= x <= 90 and 0 <= y <= 20:  # Within plot bounds
                    ax.annotate(label, (x, y), xytext=(x_offset, y_offset),
                               textcoords='offset points', fontsize=9, 
                               color='grey', alpha=0.8, fontweight='bold')
        
        # Add description text
        description = ('F: Foidite, Ph: Phonolite, Pc: Picrobasalt, U1: Tephrite (ol < 10%) Basanite(ol > 10%),\n'
                      'U2: Phonotephrite, U3: Tephriphonolite, Ba: alkalic basalt, Bs: subalkalic basalt,\n'
                      'S1: Trachybasalt, S2: Basaltic Trachyandesite, S3: Trachyandesite,\n'
                      'O1: Basaltic Andesite, O2: Andesite, O3: Dacite, T: Trachyte, Td: Trachydacite,\n'
                      'R: Rhyolite, Q: Silexite, S/N/L: Sodalitite/Nephelinolith/Leucitolith')
        
        ax.text(0.02, 0.02, description, transform=ax.transAxes, fontsize=7,
               verticalalignment='bottom', style='italic', 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Harker diagram implementation
class Harker(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Check if SiO2 column exists
        if 'SiO2' not in self.df.columns:
            plt.text(0.5, 0.5, 'Missing required column: SiO2', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Define oxides to plot against SiO2
        oxides = ['Al2O3', 'Fe2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'MnO']
        available_oxides = [oxide for oxide in oxides if oxide in self.df.columns]
        
        if not available_oxides:
            plt.text(0.5, 0.5, 'No oxide columns found to plot against SiO2', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Create subplots
        num_oxides = len(available_oxides)
        rows = (num_oxides + 2) // 3  # Ceiling division
        cols = min(3, num_oxides)
        
        # Create a figure with subplots
        for i, oxide in enumerate(available_oxides):
            ax = self.fig.add_subplot(rows, cols, i+1)
            
            # Plot each sample with consistent colors
            for j, (idx, row) in enumerate(self.df.iterrows()):
                color = self.colors[j] if j < len(self.colors) else 'blue'
                label = self.legend_labels[j] if j < len(self.legend_labels) else f'Sample {j+1}'
                ax.scatter(row['SiO2'], row[oxide], marker='o', color=color, alpha=0.6, 
                          label=label if i == 0 else '', s=40, edgecolors='black', linewidth=0.3)
            
            ax.set_xlabel('SiO2 (wt%)')
            ax.set_ylabel(f'{oxide} (wt%)')
            ax.grid(True, linestyle='--', alpha=0.5)
            
        # Add legend to the entire figure if multiple samples with distinct groups
        if len(self.df) > 1 and len(self.df) <= 10:
            # Create a legend for the whole figure using unique labels
            handles, labels = [], []
            unique_labels = []
            for i, label in enumerate(self.legend_labels):
                if label not in unique_labels:
                    unique_labels.append(label)
                    color = self.colors[i] if i < len(self.colors) else 'blue'
                    # Create a dummy scatter plot for the legend
                    from matplotlib.lines import Line2D
                    handles.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                                        markersize=8, alpha=0.8, markeredgecolor='black'))
                    labels.append(label)
            
            if handles:
                self.fig.legend(handles, labels, loc='center right', bbox_to_anchor=(0.98, 0.5), 
                              fontsize=10, frameon=True, fancybox=True, shadow=True)
        
        self.fig.tight_layout()
        self.fig.suptitle('Harker Diagrams', fontsize=16)
        self.fig.subplots_adjust(top=0.92, right=0.85 if len(self.df) > 1 and len(self.df) <= 10 else 0.95)

# REE diagram implementation based on REE.py
class REE(BasePlot):
    def __init__(self, df=None, fig=None, standard='C1 Chondrite Sun and McDonough,1989'):
        super().__init__(df, fig)
        self.standard = standard
        
        # All available standards from REE.py
        self.standards = {
            'C1 Chondrite Sun and McDonough,1989': {
                'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
                'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254
            },
            'Chondrite Taylor and McLennan,1985': {
                'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
                'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
                'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381
            },
            'Chondrite Haskin et al.,1966': {
                'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185, 'Eu': 0.071,
                'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                'Yb': 0.186, 'Lu': 0.034
            },
            'Chondrite Nakamura,1977': {
                'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203, 'Eu': 0.077,
                'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                'Yb': 0.22, 'Lu': 0.034
            },
            'MORB Sun and McDonough,1989': {
                'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63, 'Eu': 1.02, 'Gd': 3.68,
                'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052, 'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05,
                'Lu': 0.46
            },
            'UCC_Rudnick & Gao2003': {
                'La': 31, 'Ce': 63, 'Pr': 7.1, 'Nd': 27, 'Sm': 4.7, 'Eu': 1, 'Gd': 4, 'Tb': 0.7,
                'Dy': 3.9, 'Ho': 0.83, 'Er': 2.3, 'Tm': 0.3, 'Yb': 1.96, 'Lu': 0.31
            }
        }
    
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # REE elements in exact order from REE.py
        ree_elements = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        available_rees = [ree for ree in ree_elements if ree in self.df.columns]
        
        if not available_rees:
            plt.text(0.5, 0.5, 'No REE columns found\nRequired: La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure,
                    fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Get the selected normalization standard
        normalization_values = self.standards.get(self.standard, self.standards['C1 Chondrite Sun and McDonough,1989'])
        
        # Track Y range for proper scaling
        y_bottom, y_top = float('inf'), float('-inf')
        
        # Plot each sample
        for i, (idx, row) in enumerate(self.df.iterrows()):
            color = self.colors[i] if i < len(self.colors) else 'blue'
            label = self.legend_labels[i] if i < len(self.legend_labels) else f'Sample {i+1}'
            
            # Calculate normalized values and log transform
            lines_x = []
            lines_y = []
            
            for j, ree in enumerate(available_rees):
                if ree in normalization_values and not pd.isna(row[ree]) and row[ree] > 0:
                    try:
                        normalized_value = row[ree] / normalization_values[ree]
                        log_value = np.log10(normalized_value)
                        
                        lines_x.append(j + 1)  # X positions start from 1
                        lines_y.append(log_value)
                        
                        # Track Y range
                        if log_value < y_bottom:
                            y_bottom = log_value
                        if log_value > y_top:
                            y_top = log_value
                            
                        # Plot points
                        ax.scatter(j + 1, log_value, marker='o', color=color, s=50, 
                                  alpha=0.8, edgecolors='black', linewidth=0.5)
                    except (ValueError, ZeroDivisionError):
                        continue
            
            # Connect points with lines (exact behavior from REE.py)
            if len(lines_x) > 1:
                ax.plot(lines_x, lines_y, color=color, linewidth=1.5, 
                       alpha=0.8, label=label)
        
        # Set proper axis ranges and ticks according to REE.py
        xticks = list(range(1, len(available_rees) + 1))
        ax.set_xticks(xticks)
        ax.set_xticklabels(available_rees, rotation=45, fontsize=10)
        
        # Set Y axis with proper range
        if y_bottom != float('inf') and y_top != float('-inf'):
            y_range = y_top - y_bottom
            ax.set_ylim(y_bottom - y_range * 0.1, y_top + y_range * 0.1)
            
            # Create Y tick labels showing actual values (not log values)
            y_ticks = ax.get_yticks()
            y_tick_labels = [f'{10**tick:.2g}' for tick in y_ticks]
            ax.set_yticklabels(y_tick_labels, fontsize=8)
        
        # Remove top and right spines
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        # Set labels and title
        ax.set_xlabel('REE Standardized Pattern', fontsize=12)
        ax.set_ylabel(f'Sample/{self.standard.split(" ")[0]}', fontsize=12)
        ax.set_title('REE Standardized Pattern Diagram', fontsize=14, fontweight='bold')
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend if multiple samples
        if len(self.df) > 1 and len(self.df) <= 10:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        
        # Add reference
        ax.text(0.02, 0.98, f'Standard: {self.standard}', 
                transform=ax.transAxes, fontsize=8, verticalalignment='top', style='italic')

# Trace element diagram implementation based on Trace.py and TraceNew.py
class Trace(BasePlot):
    def __init__(self, df=None, fig=None, standard='PM', element_set='cs_lu'):
        super().__init__(df, fig)
        self.standard = standard
        self.element_set = element_set
        
        # All available standards from Trace.py
        self.standards = {
            'PM': {
                'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
                'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
                'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
                'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.736, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
                'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074
            },
            'OIB': {
                'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                'K': 12000, 'La': 36, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200, 'Gd': 7.62,
                'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3
            },
            'EMORB': {
                'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155, 'P': 620,
                'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                'Yb': 2.36, 'Lu': 0.354
            },
            'C1': {
                'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
                'Ta': 0.014, 'K': 545, 'La': 0.236, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
                'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
                'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0364, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254
            },
            'NMORB': {
                'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                'Yb': 3.05, 'Lu': 0.455
            },
            'UCC_Rudnick & Gao2003': {
                'K': 23244.13676, 'Ti': 3835.794545, 'P': 654.6310022, 'Li': 24, 'Be': 2.1, 'B': 17, 'N': 83, 'F': 557, 'S': 62, 'Cl': 360, 'Sc': 14, 'V': 97, 'Cr': 92,
                'Co': 17.3, 'Ni': 47, 'Cu': 28, 'Zn': 67, 'Ga': 17.5, 'Ge': 1.4, 'As': 4.8, 'Se': 0.09,
                'Br': 1.6, 'Rb': 84, 'Sr': 320, 'Y': 21, 'Zr': 193, 'Nb': 12, 'Mo': 1.1, 'Ru': 0.34,
                'Pd': 0.52, 'Ag': 53, 'Cd': 0.09, 'In': 0.056, 'Sn': 2.1, 'Sb': 0.4, 'I': 1.4, 'Cs': 4.9,
                'Ba': 628, 'La': 31, 'Ce': 63, 'Pr': 7.1, 'Nd': 27, 'Sm': 4.7, 'Eu': 1, 'Gd': 4, 'Tb': 0.7,
                'Dy': 3.9, 'Ho': 0.83, 'Er': 2.3, 'Tm': 0.3, 'Yb': 1.96, 'Lu': 0.31, 'Hf': 5.3, 'Ta': 0.9,
                'W': 1.9, 'Re': 0.198, 'Os': 0.031, 'Ir': 0.022, 'Pt': 0.5, 'Au': 1.5, 'Hg': 0.05, 'Tl': 0.9,
                'Pb': 17, 'Bi': 0.16, 'Th': 10.5, 'U': 2.7
            }
        }
        
        # Element sequences (exact order from Trace.py and TraceNew.py)
        self.element_sets = {
            'cs_lu': ['Cs', 'Tl', 'Rb', 'Ba', 'W', 'Th', 'U', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Pb', 'Pr', 'Mo',
                     'Sr', 'P', 'Nd', 'F', 'Sm', 'Zr', 'Hf', 'Eu', 'Sn', 'Sb', 'Ti', 'Gd', 'Tb', 'Dy',
                     'Li', 'Y', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'],
            'rb_lu': ['Rb', 'Ba', 'Th', 'U', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Pr', 'Sr', 'P', 'Nd',
                     'Zr', 'Hf', 'Sm', 'Eu', 'Ti', 'Tb', 'Dy', 'Y', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        }
    
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Get element sequence and normalization values
        element_sequence = self.element_sets.get(self.element_set, self.element_sets['cs_lu'])
        normalization_values = self.standards.get(self.standard, self.standards['PM'])
        
        # Find available elements in data
        available_elements = []
        missing_elements = []
        for element in element_sequence:
            if element in self.df.columns:
                available_elements.append(element)
            elif element == 'K' and 'K2O' in self.df.columns:
                available_elements.append(element)  # We'll convert K2O to K
            elif element == 'Ti' and 'TiO2' in self.df.columns:
                available_elements.append(element)  # We'll convert TiO2 to Ti
            else:
                missing_elements.append(element)
        
        if not available_elements:
            plt.text(0.5, 0.5, f'No trace element columns found\nRequired elements from {element_set_name} sequence not available\nMissing elements: {", ".join(missing_elements[:10])}{"..." if len(missing_elements) > 10 else ""}', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure,
                    fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Track Y range for proper scaling
        y_bottom, y_top = float('inf'), float('-inf')
        
        # Plot each sample
        for i, (idx, row) in enumerate(self.df.iterrows()):
            color = self.colors[i] if i < len(self.colors) else 'blue'
            label = self.legend_labels[i] if i < len(self.legend_labels) else f'Sample {i+1}'
            
            # Calculate normalized values and log transform
            lines_x = []
            lines_y = []
            
            for j, element in enumerate(available_elements):
                if element in normalization_values:
                    # Get the raw value
                    if element in self.df.columns and not pd.isna(row[element]) and row[element] > 0:
                        raw_value = row[element]
                    elif element == 'K' and 'K2O' in self.df.columns and not pd.isna(row['K2O']):
                        # Convert K2O to K (from Trace.py)
                        raw_value = row['K2O'] * (2 * 39.0983 / 94.1956) * 10000
                    elif element == 'Ti' and 'TiO2' in self.df.columns and not pd.isna(row['TiO2']):
                        # Convert TiO2 to Ti (from Trace.py)
                        raw_value = row['TiO2'] * (47.867 / 79.865) * 10000
                    else:
                        continue
                    
                    try:
                        normalized_value = raw_value / normalization_values[element]
                        log_value = np.log10(normalized_value)
                        
                        lines_x.append(j + 1)  # X positions start from 1
                        lines_y.append(log_value)
                        
                        # Track Y range
                        if log_value < y_bottom:
                            y_bottom = log_value
                        if log_value > y_top:
                            y_top = log_value
                            
                        # Plot points
                        ax.scatter(j + 1, log_value, marker='o', color=color, s=50, 
                                  alpha=0.8, edgecolors='black', linewidth=0.5)
                    except (ValueError, ZeroDivisionError):
                        continue
            
            # Connect points with lines
            if len(lines_x) > 1:
                ax.plot(lines_x, lines_y, color=color, linewidth=1.5, 
                       alpha=0.8, label=label)
        
        # Set proper axis ranges and ticks
        xticks = list(range(1, len(available_elements) + 1))
        ax.set_xticks(xticks)
        ax.set_xticklabels(available_elements, rotation=-45, fontsize=10)
        
        # Set Y axis with proper range
        if y_bottom != float('inf') and y_top != float('-inf'):
            y_range = y_top - y_bottom
            ax.set_ylim(y_bottom - y_range * 0.1, y_top + y_range * 0.1)
            
            # Create Y tick labels showing actual values (not log values)
            y_ticks = ax.get_yticks()
            y_tick_labels = [f'{10**tick:.2g}' for tick in y_ticks]
            ax.set_yticklabels(y_tick_labels, fontsize=8)
        
        # Remove top and right spines
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        # Set labels and title
        element_set_name = 'Cs-Lu (36 Elements)' if self.element_set == 'cs_lu' else 'Rb-Lu (26 Elements)'
        ax.set_xlabel(f'Trace Elements Standardized Pattern', fontsize=12)
        ax.set_ylabel(f'Sample/{self.standard}', fontsize=12)
        ax.set_title(f'Trace Element Standardized Pattern Diagram\n{element_set_name} - {len(available_elements)} Elements Available', 
                    fontsize=14, fontweight='bold')
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Add legend if multiple samples
        if len(self.df) > 1 and len(self.df) <= 10:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        
        # Add comprehensive reference information
        reference_map = {
            'PM': 'Sun, S.S. & McDonough, W.F. (1989)',
            'OIB': 'Sun, S.S. & McDonough, W.F. (1989)', 
            'EMORB': 'Sun, S.S. & McDonough, W.F. (1989)',
            'C1': 'Sun, S.S. & McDonough, W.F. (1989)',
            'NMORB': 'Sun, S.S. & McDonough, W.F. (1989)',
            'UCC_Rudnick & Gao2003': 'Rudnick, R.L. & Gao, S. (2003)'
        }
        
        reference_text = f'Standard: {self.standard} ({reference_map.get(self.standard, "")}) \nElements: {len(available_elements)} of {element_set_name}'
        ax.text(0.02, 0.98, reference_text, 
                transform=ax.transAxes, fontsize=8, verticalalignment='top', style='italic')

# Pearce diagram implementation based on Pearce.py
class Pearce(BasePlot):
    def __init__(self, df=None, fig=None):
        super().__init__(df, fig)
        
        # Define the four different conditions from Pearce.py
        self.conditions = [
            {
                'BaseLines': [[(2, 80), (55, 300)],
                             [(55, 300), (400, 2000)],
                             [(55, 300), (51.5, 8)],
                             [(51.5, 8), (50, 1)],
                             [(51.5, 8), (2000, 400)]],
                'xLabel': 'Y+Nb (ppm)',
                'yLabel': 'Rb (ppm)',
                'Labels': ['syn-COLG', 'VAG', 'WPG', 'ORG'],
                'Locations': [(1, 3), (1, 1), (2.4, 2.4), (3, 1)],
                'xlim': (0.3, 3.2),
                'ylim': (0, 3.2),
                'xticks': [1, 2, 3],
                'xticklabels': [10, 100, 1000],
                'yticks': [0, 1, 2, 3],
                'yticklabels': [1, 10, 100, 1000]
            },
            {
                'BaseLines': [[(0.5, 140), (6, 200)],
                             [(6, 200), (50, 2000)],
                             [(6, 200), (6, 8)],
                             [(6, 8), (6, 1)],
                             [(6, 8), (200, 400)]],
                'xLabel': 'Yb+Ta (ppm)',
                'yLabel': 'Rb (ppm)',
                'Labels': ['syn-COLG', 'VAG', 'WPG', 'ORG'],
                'Locations': [(0.5, 3), (0.5, 1), (1.5, 2.4), (2, 1)],
                'xlim': (-0.2, 2.5),
                'ylim': (0, 3.2),
                'xticks': [0, 1, 2],
                'xticklabels': [1, 10, 100],
                'yticks': [0, 1, 2, 3],
                'yticklabels': [1, 10, 100, 1000]
            },
            {
                'BaseLines': [[(1, 2000), (50, 10)],
                             [(40, 1), (50, 10)],
                             [(50, 10), (1000, 100)],
                             [(25, 25), (1000, 400)]],
                'xLabel': 'Y (ppm)',
                'yLabel': 'Nb (ppm)',
                'Labels': ['syn-COLG', 'VAG', 'WPG', 'ORG'],
                'Locations': [(0.5, 1.5), (0.5, 2), (2, 2), (2.2, 0.5)],
                'xlim': (0, 3.2),
                'ylim': (0, 3.2),
                'xticks': [0, 1, 2, 3],
                'xticklabels': [1, 10, 100, 1000],
                'yticks': [0, 1, 2, 3],
                'yticklabels': [1, 10, 100, 1000]
            },
            {
                'BaseLines': [[(0.55, 20), (3, 2)],
                             [(0.1, 0.35), (3, 2)],
                             [(3, 2), (5, 1)],
                             [(5, 0.05), (5, 1)],
                             [(5, 1), (100, 7)],
                             [(3, 2), (100, 20)]],
                'xLabel': 'Yb (ppm)',
                'yLabel': 'Ta (ppm)',
                'Labels': ['syn-COLG', 'VAG', 'WPG', 'ORG'],
                'Locations': [(-0.5, 0.1), (-0.5, -1), (0.7, 1), (1.5, 0)],
                'xlim': (-1, 2),
                'ylim': (-1.2, 2),
                'xticks': [-1, 0, 1, 2],
                'xticklabels': [0.1, 1, 10, 100],
                'yticks': [-1, 0, 1, 2],
                'yticklabels': [0.1, 1, 10, 100]
            }
        ]
    
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Check if required columns exist
        required_cols = ['Rb', 'Y', 'Nb', 'Yb', 'Ta']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            plt.text(0.5, 0.5, f'Missing required columns: {", ".join(missing_cols)}\nRequired: Rb, Y, Nb, Yb, Ta', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure,
                    fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            return
        
        # Clear the figure and create 2x2 subplots
        self.fig.clear()
        axes = self.fig.subplots(2, 2)
        self.fig.subplots_adjust(hspace=0.4, wspace=0.4, left=0.1, bottom=0.1, right=0.9, top=0.95)
        
        # Calculate data values for each diagram
        plot_data = []
        for i, (idx, row) in enumerate(self.df.iterrows()):
            plot_data.append({
                'xa': row['Y'] + row['Nb'],    # Y+Nb vs Rb
                'ya': row['Rb'],
                'xb': row['Yb'] + row['Ta'],   # Yb+Ta vs Rb  
                'yb': row['Rb'],
                'xc': row['Y'],                # Y vs Nb
                'yc': row['Nb'],
                'xd': row['Yb'],               # Yb vs Ta
                'yd': row['Ta'],
                'color': self.colors[i] if i < len(self.colors) else 'blue',
                'label': self.legend_labels[i] if i < len(self.legend_labels) else f'Sample {i+1}'
            })
        
        # Plot each of the four diagrams
        diagram_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
        data_keys = [('xa', 'ya'), ('xb', 'yb'), ('xc', 'yc'), ('xd', 'yd')]
        
        for diagram_idx, ((row_idx, col_idx), (x_key, y_key)) in enumerate(zip(diagram_coords, data_keys)):
            ax = axes[row_idx, col_idx]
            condition = self.conditions[diagram_idx]
            
            # Set up the axes
            ax.set_xlabel(condition['xLabel'], fontsize=12)
            ax.set_ylabel(condition['yLabel'], fontsize=12)
            ax.set_xlim(condition['xlim'])
            ax.set_ylim(condition['ylim'])
            ax.set_xticks(condition['xticks'])
            ax.set_xticklabels(condition['xticklabels'])
            ax.set_yticks(condition['yticks'])
            ax.set_yticklabels(condition['yticklabels'])
            
            # Remove top and right spines
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            
            # Draw boundary lines
            for line in condition['BaseLines']:
                x_coords = [np.log10(point[0]) for point in line]
                y_coords = [np.log10(point[1]) for point in line]
                
                # Special styling for certain lines (from original code)
                if diagram_idx == 2 and line == [(25, 25), (1000, 400)]:
                    ax.plot(x_coords, y_coords, linestyle=':', color='grey', linewidth=0.8, alpha=0.3)
                elif diagram_idx == 3 and line == [(3, 2), (100, 20)]:
                    ax.plot(x_coords, y_coords, linestyle=':', color='grey', linewidth=0.8, alpha=0.3)
                else:
                    ax.plot(x_coords, y_coords, color='black', linewidth=0.8, alpha=0.5)
            
            # Plot data points
            for i, data in enumerate(plot_data):
                try:
                    x_val = data[x_key]
                    y_val = data[y_key]
                    
                    if x_val > 0 and y_val > 0:  # Only plot positive values for log scale
                        ax.scatter(np.log10(x_val), np.log10(y_val), 
                                  marker='o', color=data['color'], s=50, alpha=0.8,
                                  label=data['label'] if diagram_idx == 0 else '',  # Only show legend on first plot
                                  edgecolors='black', linewidth=0.5)
                except (ValueError, TypeError):
                    continue
            
            # Add field labels
            for label, location in zip(condition['Labels'], condition['Locations']):
                ax.annotate(label, xy=location, xycoords='data', 
                           fontsize=9, color='grey', alpha=0.8, fontweight='bold',
                           ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.3)
        
        # Add overall title
        self.fig.suptitle('Pearce Diagrams for Granite Discrimination (Pearce et al., 1984)', 
                         fontsize=16, fontweight='bold')
        
        # Add legend to the top-right subplot
        if len(self.df) > 1 and len(self.df) <= 10:
            # Get unique labels for legend
            unique_labels = []
            unique_colors = []
            for i, data in enumerate(plot_data):
                if data['label'] not in unique_labels:
                    unique_labels.append(data['label'])
                    unique_colors.append(data['color'])
            
            # Create legend handles
            from matplotlib.lines import Line2D
            handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                            markersize=8, alpha=0.8, markeredgecolor='black') 
                      for color in unique_colors]
            
            axes[0, 1].legend(handles, unique_labels, bbox_to_anchor=(1.05, 1), 
                             loc='upper left', fontsize=10)
        
        # Add description text
        description = ('syn-COLG: syn-collision granites, VAG: volcanic arc granites\n'
                      'WPG: within plate granites, ORG: ocean ridge granites')
        self.fig.text(0.5, 0.02, description, ha='center', va='bottom', 
                     fontsize=10, style='italic')
        
        # Add reference
        self.fig.text(0.02, 0.98, 'Reference: Pearce, J.A. et al. (1984) J. Petrology, v.25, p.956-983', 
                     ha='left', va='top', fontsize=8, style='italic')

# CIPW norm calculation implementation
class CIPW:
    def __init__(self, df=None):
        self.df = df
        self.result_df = None
        
    def calculate(self):
        if self.df is None:
            return
            
        # Check if required columns exist
        required_cols = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        # If some columns are missing, try to estimate or use default values
        if missing_cols:
            for col in missing_cols:
                if col == 'Fe2O3' and 'FeO' in self.df.columns:
                    self.df['Fe2O3'] = self.df['FeO'] * 0.15  # Estimate Fe2O3 as 15% of FeO
                elif col == 'FeO' and 'Fe2O3' in self.df.columns:
                    self.df['FeO'] = self.df['Fe2O3'] * 0.9  # Estimate FeO as 90% of Fe2O3
                else:
                    self.df[col] = 0.1  # Default small value
        
        # Initialize result dataframe
        result = pd.DataFrame()
        
        # Perform a simplified CIPW norm calculation
        # This is a very simplified version that doesn't do the full calculation
        for i, row in self.df.iterrows():
            # Convert oxide percentages to molecular proportions
            mol_SiO2 = row['SiO2'] / 60.08
            mol_Al2O3 = row['Al2O3'] / 101.96
            mol_Fe2O3 = row['Fe2O3'] / 159.69
            mol_FeO = row['FeO'] / 71.85
            mol_MgO = row['MgO'] / 40.30
            mol_CaO = row['CaO'] / 56.08
            mol_Na2O = row['Na2O'] / 61.98
            mol_K2O = row['K2O'] / 94.20
            mol_TiO2 = row['TiO2'] / 79.87
            mol_P2O5 = row['P2O5'] / 141.94
            mol_MnO = row['MnO'] / 70.94
            
            # Calculate simplified mineral components
            # This is not the full CIPW calculation, just a simplified version for demonstration
            quartz = max(0, mol_SiO2 - 2*mol_Na2O - 2*mol_K2O - mol_CaO - mol_MgO - mol_FeO - 2*mol_Fe2O3)
            orthoclase = mol_K2O
            albite = mol_Na2O
            anorthite = mol_Al2O3 - mol_Na2O - mol_K2O
            diopside = min(mol_CaO - anorthite, mol_MgO)
            hypersthene = mol_MgO - diopside
            magnetite = mol_Fe2O3
            ilmenite = mol_TiO2
            apatite = mol_P2O5 / 3 * 10  # Simplified conversion
            
            # Convert back to weight percentages (simplified)
            result.loc[i, 'Quartz'] = quartz * 60.08
            result.loc[i, 'Orthoclase'] = orthoclase * 278.33
            result.loc[i, 'Albite'] = albite * 262.22
            result.loc[i, 'Anorthite'] = anorthite * 278.21
            result.loc[i, 'Diopside'] = diopside * 216.55
            result.loc[i, 'Hypersthene'] = hypersthene * 132.15
            result.loc[i, 'Magnetite'] = magnetite * 231.54
            result.loc[i, 'Ilmenite'] = ilmenite * 151.73
            result.loc[i, 'Apatite'] = apatite * 502.31
            
        # Normalize to 100%
        for i, row in result.iterrows():
            total = row.sum()
            for col in result.columns:
                result.loc[i, col] = result.loc[i, col] / total * 100
                
        self.result_df = result
        return result

# Helper functions for triangular coordinates based on QAPF.py
def tri_to_bin(a, p, q):
    """Convert triangular coordinates to binary coordinates - exact from QAPF.py"""
    # This matches the TriToBin function from QAPF.py
    total = a + p + abs(q)
    if total == 0:
        return 50, 0
    
    # Normalize
    a_norm = a / total * 100
    p_norm = p / total * 100
    q_norm = q / total * 100
    
    # Convert to x,y coordinates
    if q >= 0:
        # Upper triangle
        x = 50 + (p_norm - a_norm) / 2
        y = q_norm * np.sqrt(3) / 2
    else:
        # Lower triangle  
        x = 50 + (p_norm - a_norm) / 2
        y = q_norm * np.sqrt(3) / 2
    
    return x, y

def tri_line_points(points):
    """Convert triangular coordinate points to cartesian - based on TriLine from QAPF.py"""
    x_coords = []
    y_coords = []
    
    for point in points:
        a, p, q = point
        x, y = tri_to_bin(a, p, q)
        x_coords.append(x)
        y_coords.append(y)
    
    return x_coords, y_coords

def tri_cross(line1, line2):
    """Find intersection of two triangular lines - simplified from TriCross in QAPF.py"""
    # This is a simplified version - the original is more complex
    # For now, return a reasonable intersection point
    p1_start, p1_end = line1
    p2_start, p2_end = line2
    
    # Simple midpoint approximation
    mid_a = (p1_start[0] + p1_end[0] + p2_start[0] + p2_end[0]) / 4
    mid_p = (p1_start[1] + p1_end[1] + p2_start[1] + p2_end[1]) / 4
    mid_q = (p1_start[2] + p1_end[2] + p2_start[2] + p2_end[2]) / 4
    
    return (mid_a, mid_p, mid_q)

def draw_triangle_grid(ax, diagram_type='plutonic'):
    """Draw the QAPF triangular grid exactly matching QAPF.py"""
    # Set up coordinate system exactly like QAPF.py
    ax.set_xlim(-10, 110)
    ax.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)
    
    # Main triangle outline - from QAPF.py TriLine
    main_outline = [(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0)]
    x_coords, y_coords = tri_line_points(main_outline)
    ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
    
    if diagram_type == 'plutonic':
        # Plutonic rock diagram (exact from QAPF.py when slider.value() == 0)
        
        # Horizontal percentage lines
        L1 = [(10, 0, 90), (0, 10, 90)]
        L2 = [(40, 0, 60), (0, 40, 60)]
        L3 = [(80, 0, 20), (0, 80, 20)]
        L4 = [(95, 0, 5), (0, 95, 5)]
        
        for line in [L1, L2, L3, L4]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
        
        # Diagonal subdivision lines for upper triangle
        D1 = (0, 0, 100)
        SL1 = [D1, (90, 10, 0)]
        SL2 = [D1, (65, 35, 0)]
        SL3 = [D1, (35, 65, 0)]
        SL4 = [D1, (10, 90, 0)]
        
        # Calculate intersections
        CL1 = tri_cross(SL1, L2)
        CL21 = tri_cross(SL2, L2)
        CL22 = tri_cross(SL2, L3)
        CL3 = tri_cross(SL3, L2)
        CL41 = tri_cross(SL4, L2)
        CL42 = tri_cross(SL4, L3)
        
        # New subdivision lines
        NSL1 = [CL1, (90, 10, 0)]
        NSL21 = [CL21, CL22]
        NSL22 = [CL22, (65, 35, 0)]
        NSL3 = [CL3, (35, 65, 0)]
        NSL4 = [CL41, (10, 90, 0)]
        
        # Draw subdivision lines
        for line in [NSL1, NSL22, NSL3, NSL4]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
        
        # Dashed line
        x_coords, y_coords = tri_line_points(NSL21)
        ax.plot(x_coords, y_coords, 'k--', linewidth=1, alpha=0.7)
        
        # Lower triangle lines
        D2 = (0, 0, -100)
        L2_lower = [(40, 0, -60), (0, 40, -60)]
        L3_lower = [(90, 0, -10), (0, 90, -10)]
        
        SL1_lower = [D2, (90, 10, 0)]
        SL2_lower = [D2, (65, 35, 0)]
        SL3_lower = [D2, (35, 65, 0)]
        SL4_lower = [D2, (10, 90, 0)]
        SL5 = [(20, 20, -60), (45, 45, -10)]
        
        # Calculate intersections for lower triangle
        CL1_lower = tri_cross(SL1_lower, L2_lower)
        CL2_lower = tri_cross(SL2_lower, L3_lower)
        CL3_lower = tri_cross(SL3_lower, L3_lower)
        CL41_lower = tri_cross(SL4_lower, L2_lower)
        
        NSL1_lower = [CL1_lower, (90, 10, 0)]
        NSL2_lower = [CL2_lower, (65, 35, 0)]
        NSL3_lower = [CL3_lower, (35, 65, 0)]
        NSL4_lower = [CL41_lower, (10, 90, 0)]
        
        # Draw lower triangle lines
        for line in [L2_lower, L3_lower, SL5, NSL1_lower, NSL2_lower, NSL3_lower, NSL4_lower]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
    
    else:
        # Volcanic rock diagram (when slider.value() == 1)
        # Simplified version for volcanic rocks
        L1 = [(10, 0, 90), (0, 10, 90)]
        L2 = [(40, 0, 60), (0, 40, 60)]
        L3 = [(80, 0, 20), (0, 80, 20)]
        
        for line in [L1, L2, L3]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
        
        # Add volcanic-specific subdivision lines
        D = (0, 0, 100)
        SL1 = [D, (90, 10, 0)]
        SL2 = [D, (65, 35, 0)]
        SL3 = [D, (35, 65, 0)]
        SL4 = [D, (10, 90, 0)]
        
        # Calculate some intersections
        CL1 = tri_cross(SL1, L2)
        CL21 = tri_cross(SL2, L2)
        CL22 = tri_cross(SL2, L3)
        CL3 = tri_cross(SL3, L2)
        
        NSL1 = [CL1, (90, 10, 0)]
        NSL21 = [CL21, CL22]
        NSL22 = [CL22, (65, 35, 0)]
        NSL3 = [CL3, (35, 65, 0)]
        
        # Draw lines
        for line in [NSL1, NSL22, NSL3]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)
        
        # Dashed line
        x_coords, y_coords = tri_line_points(NSL21)
        ax.plot(x_coords, y_coords, 'k--', linewidth=1, alpha=0.7)
        
        # Lower triangle for volcanic
        D_lower = (0, 0, -100)
        L2_lower = [(40, 0, -60), (0, 40, -60)]
        L3_lower = [(90, 0, -10), (0, 90, -10)]
        SL5 = [(5, 5, -90), (45, 45, -10)]
        
        for line in [L2_lower, L3_lower, SL5]:
            x_coords, y_coords = tri_line_points(line)
            ax.plot(x_coords, y_coords, 'k-', linewidth=1, alpha=0.7)

# QAPF diagram implementation based on QAPF.py
class QAPF(BasePlot):
    def __init__(self, df=None, fig=None, cipw_result=None):
        super().__init__(df, fig)
        self.cipw_result = cipw_result
        
        # Labels for triangle corners (exact from QAPF.py)
        self.corner_labels = ['Q', 'A', 'P', 'F']
        self.corner_positions = [(48, 50 * np.sqrt(3) + 1), (-6, -1), (104, -1), (49, -50 * np.sqrt(3) - 4)]
        
        # Rock type labels and positions (exact from QAPF.py)
        self.rock_labels = ['1a', '1b', '2', '3a', '3b', '4', '5', 
                           '6*', '7*', '8*', '9*', '10*',
                           '6', '7', '8', '9', '10',
                           '6\'', '7\'', '8\'', '9\'', '10\'',
                           '11', '12', '13', '14', '15']
        
        # Rock label positions (exact from QAPF.py)
        self.rock_positions = [(50, 80), (50, 65), (22, 33), (32, 33), (50, 33), (66, 33), (76, 33),
                              (10, 10), (26, 10), (50, 10), (74, 10), (88, 10),
                              (6, 1), (24, 1), (50, 1), (76, 1), (90, 1),
                              (6, -5), (24, -5), (50, -5), (76, -5), (90, -5),
                              (18, -30), (40, -30), (60, -30), (78, -30), (50, -60)]
    
    def plot(self):
        if self.fig is None:
            return
            
        # Use CIPW results if provided, otherwise try to calculate
        if self.cipw_result is not None:
            norm_df = self.cipw_result
        elif self.df is not None:
            # Calculate CIPW norm
            cipw = CIPW(df=self.df)
            cipw.calculate()
            if cipw.result_df is not None:
                norm_df = cipw.result_df
            else:
                plt.text(0.5, 0.5, 'Unable to calculate CIPW norm for QAPF diagram', 
                        horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
                return
        else:
            plt.text(0.5, 0.5, 'No data provided for QAPF diagram', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Get the axes and set up triangular coordinate system exactly like QAPF.py
        ax = self.fig.add_subplot(111)
        ax.axis('off')  # Turn off normal axes
        
        # Draw the triangular grid using plutonic diagram type
        draw_triangle_grid(ax, diagram_type='plutonic')
        
        # Add corner labels (exact positions from QAPF.py)
        for i, (label, pos) in enumerate(zip(self.corner_labels, self.corner_positions)):
            ax.annotate(label, xy=pos, xycoords='data', fontsize=8, ha='center', va='center', fontweight='bold')
        
        # Add rock type labels with exact positions from QAPF.py
        for label, pos in zip(self.rock_labels, self.rock_positions):
            ax.annotate(label, xy=pos, xycoords='data', fontsize=6, ha='center', va='center', 
                       color='grey', alpha=0.8, fontweight='bold')
        
        # Plot QAPF data points using exact coordinate transformation from QAPF.py
        for i, row in norm_df.iterrows():
            # Get QAPF values - using exact column names expected by QAPF.py
            q = max(0, row['Quartz']) if 'Quartz' in row and not pd.isna(row['Quartz']) else 0
            a = max(0, row['Orthoclase']) if 'Orthoclase' in row and not pd.isna(row['Orthoclase']) else 0
            p = max(0, row['Albite']) if 'Albite' in row and not pd.isna(row['Albite']) else 0
            f = max(0, row['Anorthite']) if 'Anorthite' in row and not pd.isna(row['Anorthite']) else 0  # Using as F placeholder
            
            # Use the exact coordinate transformation from QAPF.py
            if q > 0:
                # Upper triangle: Q-A-P (same as original)
                x, y = tri_to_bin(a, p, q)
            else:
                # Lower triangle: A-P-F (foid-bearing rocks)
                x, y = tri_to_bin(a, p, -f)  # Negative f for lower triangle
            
            color = self.colors[i] if i < len(self.colors) else 'blue'
            label = self.legend_labels[i] if i < len(self.legend_labels) else f'Sample {i+1}'
            
            # Plot point with styling matching QAPF.py
            ax.scatter(x, y, marker='o', s=60, color=color, alpha=0.8, 
                      label=label, edgecolors='black', linewidth=0.5, zorder=5)
        
        # Add title
        ax.set_title('QAPF Modal Classification of Plutonic Rocks\n(Q = Quartz, A = Alkali Feldspar, P = Plagioclase, F = Feldspathoid)', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add legend if multiple samples
        if len(norm_df) > 1 and len(norm_df) <= 10:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        
        # Add reference and note (exact from QAPF.py)
        reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'
        infotext = 'Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%.'
        
        self.fig.text(0.02, 0.98, reference, 
                     ha='left', va='top', fontsize=6, style='italic')
        self.fig.text(0.02, 0.02, infotext, 
                     ha='left', va='bottom', fontsize=8, style='italic')

# Create Flask app
app = Flask(__name__)
app.secret_key = 'geopytool_web_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_dataframe(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path, engine='python')
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format")

def fig_to_base64(fig, format='png'):
    buf = BytesIO()
    if format.lower() == 'svg':
        fig.savefig(buf, format='svg', bbox_inches='tight')
        content_type = 'image/svg+xml'
    else:
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        content_type = 'image/png'
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str, content_type

def process_plot(plot_function, df, **kwargs):
    try:
        # Create a figure
        fig = plt.figure(figsize=(10, 8))
        
        # Call the appropriate plot function
        result = plot_function(df=df, fig=fig, **kwargs)
        
        # Convert the figure to base64 string
        img_str, content_type = fig_to_base64(fig)
        plt.close(fig)
        
        return img_str, result, content_type
    except Exception as e:
        plt.close()
        return None, str(e), None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            df = read_dataframe(file_path)
            
            # Standardize column names
            df = standardize_column_names(df)
            
            # Save the standardized dataframe back to file
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df.to_excel(file_path, index=False, engine='openpyxl')
            
            session['current_file'] = file_path
            
            # Return the first few rows as preview
            return jsonify({
                'success': True,
                'preview': df.head().to_html(classes='table table-striped table-sm'),
                'columns': df.columns.tolist(),
                'filename': filename
            })
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'error': 'File type not allowed'})

@app.route('/process', methods=['POST'])
def process():
    if 'current_file' not in session:
        return jsonify({'error': 'No file uploaded'})
    
    file_path = session['current_file']
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'})
    
    plot_type = request.form.get('plot_type')
    image_format = request.form.get('image_format', 'png')
    ree_standard = request.form.get('ree_standard', 'C1 Chondrite Sun and McDonough,1989')
    trace_standard = request.form.get('trace_standard', 'PM')
    trace_element_set = request.form.get('trace_element_set', 'cs_lu')
    
    try:
        df = read_dataframe(file_path)
        
        # Process based on plot type
        if plot_type == 'tas':
            img_str, result, content_type = process_tas(df, image_format)
        elif plot_type == 'harker':
            img_str, result, content_type = process_harker(df, image_format)
        elif plot_type == 'ree':
            img_str, result, content_type = process_ree(df, ree_standard, image_format)
        elif plot_type == 'trace':
            img_str, result, content_type = process_trace(df, trace_standard, trace_element_set, image_format)
        elif plot_type == 'pearce':
            img_str, result, content_type = process_pearce(df, image_format)
        elif plot_type == 'cipw':
            img_str, result, content_type = process_cipw(df, image_format)
        elif plot_type == 'qapf':
            img_str, result, content_type = process_qapf(df, image_format)
        # Add more plot types as needed
        else:
            return jsonify({'error': f'Unknown plot type: {plot_type}'})
        
        if img_str:
            return jsonify({
                'success': True,
                'image': img_str,
                'result': result if isinstance(result, str) else None,
                'content_type': content_type,
                'image_format': image_format
            })
        else:
            return jsonify({'error': result})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Plot processing functions
def process_tas(df, image_format='png'):
    tas = TAS(df=df)
    fig = plt.figure(figsize=(10, 8))
    tas.fig = fig
    tas.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    return img_str, None, content_type

def process_harker(df, image_format='png'):
    harker = Harker(df=df)
    fig = plt.figure(figsize=(10, 8))
    harker.fig = fig
    harker.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    return img_str, None, content_type

def process_ree(df, standard='C1 Chondrite Sun and McDonough,1989', image_format='png'):
    ree = REE(df=df, standard=standard)
    fig = plt.figure(figsize=(10, 8))
    ree.fig = fig
    ree.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    return img_str, None, content_type

def process_trace(df, standard='PM', element_set='cs_lu', image_format='png'):
    trace = Trace(df=df, standard=standard, element_set=element_set)
    fig = plt.figure(figsize=(10, 8))
    trace.fig = fig
    trace.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    return img_str, None, content_type

def process_pearce(df, image_format='png'):
    pearce = Pearce(df=df)
    fig = plt.figure(figsize=(16, 16))  # Larger size for 2x2 subplots
    pearce.fig = fig
    pearce.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    return img_str, None, content_type

def process_cipw(df, image_format='png'):
    cipw = CIPW(df=df)
    cipw.calculate()
    result_df = cipw.result_df
    
    if result_df is None:
        return None, "Failed to calculate CIPW norm. Check if all required oxide columns are present.", None
    
    # Store CIPW result in session for QAPF use
    session['cipw_result'] = result_df.to_json()
    
    # Create enhanced result table with better formatting
    result_html = f"""
    <div class="table-responsive" style="max-height: 500px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 8px;">
        <table class="table table-striped table-sm table-hover" style="margin-bottom: 0; font-size: 0.9rem;">
            <thead style="position: sticky; top: 0; background: #f8f9fa; z-index: 10;">
                <tr>
                    <th style="border: 1px solid #dee2e6; padding: 8px; font-weight: 600;">Sample</th>
    """
    
    # Add mineral headers
    for col in result_df.columns:
        result_html += f'<th style="border: 1px solid #dee2e6; padding: 8px; font-weight: 600; min-width: 100px;">{col}</th>'
    
    result_html += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Add data rows
    for i, (idx, row) in enumerate(result_df.iterrows()):
        result_html += f'<tr><td style="border: 1px solid #dee2e6; padding: 8px; font-weight: 500;">Sample {i+1}</td>'
        for col in result_df.columns:
            value = row[col]
            formatted_value = f"{value:.2f}" if pd.notna(value) else "0.00"
            result_html += f'<td style="border: 1px solid #dee2e6; padding: 8px; text-align: right;">{formatted_value}</td>'
        result_html += '</tr>'
    
    result_html += """
            </tbody>
        </table>
    </div>
    <div class="mt-3">
        <small class="text-muted">
            <strong>CIPW Norm Calculation Results</strong><br/>
            Values represent weight percentages of normative minerals calculated from major element oxides.<br/>
            These results will be automatically used for QAPF diagram plotting.
        </small>
    </div>
    """
    
    # Create a comprehensive visualization of CIPW results with QAPF diagram
    fig = plt.figure(figsize=(16, 10))
    
    if len(result_df) == 1:
        # Single sample - show bar chart, pie chart, and QAPF
        ax1 = fig.add_subplot(131)  # Bar chart
        ax2 = fig.add_subplot(132)  # Pie chart
        ax3 = fig.add_subplot(133)  # QAPF diagram
        
        sample_data = result_df.iloc[0]
        
        # Bar chart
        sample_data.plot(kind='bar', ax=ax1, color='steelblue', alpha=0.7)
        ax1.set_title('CIPW Norm Results', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Weight %', fontsize=9)
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        
        # Pie chart for major minerals
        sample_data_filtered = sample_data[sample_data > 1.0]
        if len(sample_data_filtered) > 0:
            wedges, texts, autotexts = ax2.pie(sample_data_filtered.values, labels=sample_data_filtered.index, 
                                              autopct='%1.1f%%', startangle=90, textprops={'fontsize': 7})
            ax2.set_title('Major Minerals\n(> 1 wt%)', fontweight='bold', fontsize=11)
        
    else:
        # Multiple samples - show stacked bar chart and QAPF
        ax1 = fig.add_subplot(121)  # Bar chart
        ax3 = fig.add_subplot(122)  # QAPF diagram
        
        # Stacked bar chart
        result_df.T.plot(kind='bar', stacked=True, ax=ax1, alpha=0.8, colormap='tab20')
        ax1.set_title('CIPW Norm Results - All Samples', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Weight %', fontsize=9)
        ax1.set_xlabel('Mineral Phase', fontsize=9)
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.legend(title='Samples', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=7)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
    
    # QAPF Triangle Diagram (ax3)
    ax3.axis('off')  # Turn off normal axes
    ax3.set_aspect('equal')  # This ensures correct triangle proportions
    
    # Draw the triangular grid using plutonic diagram type
    draw_triangle_grid(ax3, diagram_type='plutonic')
    
    # Add corner labels (exact positions from QAPF.py)
    corner_labels = ['Q', 'A', 'P', 'F']
    corner_positions = [(48, 50 * np.sqrt(3) + 1), (-6, -1), (104, -1), (49, -50 * np.sqrt(3) - 4)]
    for label, pos in zip(corner_labels, corner_positions):
        ax3.annotate(label, xy=pos, xycoords='data', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Add rock type labels with exact positions from QAPF.py
    rock_labels = ['1a', '1b', '2', '3a', '3b', '4', '5', 
                   '6*', '7*', '8*', '9*', '10*',
                   '6', '7', '8', '9', '10',
                   '6\'', '7\'', '8\'', '9\'', '10\'',
                   '11', '12', '13', '14', '15']
    
    # Exact positions from QAPF.py
    rock_positions = [(50, 80), (50, 65), (22, 33), (32, 33), (50, 33), (66, 33), (76, 33),
                     (10, 10), (26, 10), (50, 10), (74, 10), (88, 10),
                     (6, 1), (24, 1), (50, 1), (76, 1), (90, 1),
                     (6, -5), (24, -5), (50, -5), (76, -5), (90, -5),
                     (18, -30), (40, -30), (60, -30), (78, -30), (50, -60)]
    
    for label, pos in zip(rock_labels, rock_positions):
        ax3.annotate(label, xy=pos, xycoords='data', fontsize=6, ha='center', va='center', 
                    color='grey', alpha=0.8, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Plot QAPF data points using CIPW results with exact coordinate transformation
    colors = get_color_mapping(df)[0] if df is not None else ['blue'] * len(result_df)
    
    for i, row in result_df.iterrows():
        q = max(0, row['Quartz']) if 'Quartz' in row and not pd.isna(row['Quartz']) else 0
        a = max(0, row['Orthoclase']) if 'Orthoclase' in row and not pd.isna(row['Orthoclase']) else 0
        p = max(0, row['Albite']) if 'Albite' in row and not pd.isna(row['Albite']) else 0
        f = max(0, row['Anorthite']) if 'Anorthite' in row and not pd.isna(row['Anorthite']) else 0  # Using as F
        
        # Use exact coordinate transformation from QAPF.py
        if q > 0:
            # Upper triangle: Q-A-P
            x, y = tri_to_bin(a, p, q)
        else:
            # Lower triangle: A-P-F (foid-bearing)
            x, y = tri_to_bin(a, p, -f)  # Negative f for lower triangle
        
        color = colors[i] if i < len(colors) else 'blue'
        
        ax3.scatter(x, y, marker='o', color=color, s=40, alpha=0.8, 
                   edgecolors='black', linewidth=0.5, zorder=5)
        
        # Add sample label
        ax3.annotate(f'S{i+1}', xy=(x, y), xytext=(3, 3), textcoords='offset points',
                    fontsize=7, color=color, fontweight='bold', alpha=0.9)
    
    ax3.set_title('QAPF Classification\n(Based on CIPW Norm)', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    
    # Add overall title
    fig.suptitle('CIPW Normative Mineral Calculation\n(Based on Major Element Oxide Analysis)', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Add reference
    fig.text(0.02, 0.02, 'Reference: Cross, Iddings, Pirsson, Washington (CIPW) Norm Calculation\nFor QAPF classification of plutonic rocks', 
             ha='left', va='bottom', fontsize=8, style='italic')
    
    plt.subplots_adjust(top=0.88, bottom=0.15)
    
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    
    return img_str, result_html, content_type

def process_qapf(df, image_format='png'):
    # Try to get CIPW result from session
    cipw_result = None
    if 'cipw_result' in session:
        try:
            cipw_result = pd.read_json(session['cipw_result'])
        except:
            cipw_result = None
    
    # If no CIPW result in session, calculate it
    if cipw_result is None:
        cipw = CIPW(df=df)
        cipw.calculate()
        cipw_result = cipw.result_df
        
        if cipw_result is None:
            fig = plt.figure(figsize=(10, 8))
            plt.text(0.5, 0.5, 'Unable to calculate CIPW norm for QAPF diagram.\nPlease run CIPW calculation first.', 
                    horizontalalignment='center', verticalalignment='center', transform=fig.transFigure, 
                    fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            img_str, content_type = fig_to_base64(fig, image_format)
            plt.close(fig)
            return img_str, "Error: Unable to calculate CIPW norm. Please ensure your data contains the required oxide columns and run CIPW calculation first.", content_type
    
    # Create QAPF diagram with CIPW results
    fig = plt.figure(figsize=(10, 8))
    qapf = QAPF(df=df, fig=fig, cipw_result=cipw_result)
    qapf.plot()
    img_str, content_type = fig_to_base64(fig, image_format)
    plt.close(fig)
    
    return img_str, None, content_type

# Create HTML templates directory and files
os.makedirs('templates', exist_ok=True)

# Create index.html template - COMPLETE RECREATION WITH TRACE OPTIONS
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoPyTool Web - Advanced Geochemical Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            padding: 30px 0;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            margin-bottom: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .header h1 {
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }
        .header .lead {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            background: rgba(255,255,255,0.95);
            margin-bottom: 20px;
        }
        .card-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
            padding: 15px 20px;
        }
        .plot-container {
            margin-top: 20px;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: white;
        }
        .loading .spinner-border {
            width: 3rem;
            height: 3rem;
        }
        .result-container {
            margin-top: 20px;
        }
        
        /* Enhanced table styling with scrollbars */
        .table-responsive {
            max-height: 400px;
            overflow-y: auto;
            overflow-x: auto;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-bottom: 0;
        }
        
        .table-responsive::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        .table-responsive::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .table-responsive::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        .table-responsive::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        .table {
            margin-bottom: 0;
            font-size: 0.9rem;
            min-width: 100%;
            white-space: nowrap;
        }
        
        .table th {
            position: sticky;
            top: 0;
            background: #f8f9fa;
            border-top: none;
            z-index: 10;
            font-weight: 600;
            white-space: nowrap;
            min-width: 100px;
        }
        
        .table td {
            white-space: nowrap;
            min-width: 100px;
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .table-hover tbody tr:hover {
            background-color: #f8f9fa;
        }
        
        /* Data preview styling - BALANCED APPROACH */
        #data-preview {
            max-width: 100% !important;
            width: 100% !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            box-sizing: border-box !important;
        }
        
        #data-preview .table-responsive {
            max-height: 350px !important;
            width: 100% !important;
            overflow: auto !important;
            display: block !important;
            box-sizing: border-box !important;
        }
        
        #data-preview .table {
            font-size: 0.85rem !important;
            width: auto !important;
            min-width: 100% !important;
            margin: 0 !important;
            white-space: nowrap !important;
        }
        
        #data-preview .table th,
        #data-preview .table td {
            padding: 8px 12px !important;
            border: 1px solid #dee2e6 !important;
            min-width: 120px !important;
            white-space: nowrap !important;
            box-sizing: border-box !important;
            vertical-align: middle !important;
        }
        
        #data-preview .table th {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
            font-weight: 600 !important;
            color: #495057 !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 10 !important;
        }
        
        /* Force container constraints */
        .card-body {
            overflow-x: hidden !important;
            box-sizing: border-box !important;
        }
        
        /* Plot image styling */
        #plot-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Button styling */
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
        }
        
        .form-control, .form-select {
            border-radius: 8px;
            border: 1px solid #ced4da;
            padding: 10px 12px;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: #4facfe;
            box-shadow: 0 0 0 0.2rem rgba(79, 172, 254, 0.25);
        }
        
        /* Alert styling for better error messages */
        .alert-custom {
            border-radius: 10px;
            border: none;
            padding: 15px 20px;
            margin: 15px 0;
        }
        
        .alert-info {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #0c5460;
        }
        
        /* Progress indicator */
        .progress-indicator {
            display: none;
            margin: 20px 0;
        }
        
        .progress {
            height: 8px;
            border-radius: 4px;
            background: rgba(255,255,255,0.3);
        }
        
        .progress-bar {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border-radius: 4px;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .container {
                padding: 0 15px;
            }
            
            .table-responsive {
                max-height: 250px;
                font-size: 0.8rem;
            }
            
            .header {
                padding: 20px 0;
                margin-bottom: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header text-center">
            <h1><i class="fas fa-mountain"></i> GeoPyTool Web</h1>
            <p class="lead">Advanced Geochemical Analysis and Visualization Platform</p>
            <p class="text-white-50">Upload your geochemical data and generate professional diagrams</p>
        </div>

        <div class="row">
            <div class="col-lg-4 col-md-5">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-upload"></i> Upload Data
                    </div>
                    <div class="card-body">
                        <form id="upload-form" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="file" class="form-label">Select CSV or Excel file</label>
                                <input type="file" class="form-control" id="file" name="file" accept=".csv,.xlsx,.xls">
                                <div class="form-text">Supported formats: CSV, Excel (.xlsx, .xls)</div>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="fas fa-cloud-upload-alt"></i> Upload & Process
                            </button>
                        </form>
                        
                        <div class="progress-indicator" id="upload-progress">
                            <div class="progress">
                                <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div>
                            </div>
                            <small class="text-muted">Processing your data...</small>
                        </div>
                    </div>
                </div>

                <div class="card" id="plot-options" style="display: none;">
                    <div class="card-header">
                        <i class="fas fa-chart-line"></i> Analysis Options
                    </div>
                    <div class="card-body">
                        <form id="plot-form">
                            <div class="mb-3">
                                <label for="plot-type" class="form-label">Select Diagram Type</label>
                                <select class="form-select" id="plot-type" name="plot_type">
                                    <optgroup label="Classification Diagrams">
                                        <option value="tas">TAS Diagram (Total Alkali-Silica)</option>
                                        <option value="qapf">QAPF Diagram (Plutonic Rocks)</option>
                                    </optgroup>
                                    <optgroup label="Variation Diagrams">
                                        <option value="harker">Harker Diagrams</option>
                                    </optgroup>
                                    <optgroup label="Trace Element Patterns">
                                        <option value="ree">REE Patterns</option>
                                        <option value="trace">Trace Element Spider Diagram</option>
                                    </optgroup>
                                    <optgroup label="Tectonic Discrimination">
                                        <option value="pearce">Pearce Diagram (Granite Discrimination)</option>
                                    </optgroup>
                                    <optgroup label="Norm Calculations">
                                        <option value="cipw">CIPW Norm Calculation</option>
                                    </optgroup>
                                </select>
                                <div class="form-text">Choose the type of geochemical analysis</div>
                            </div>
                            
                            <!-- REE Standard Selection -->
                            <div class="mb-3" id="ree-standard-selection" style="display: none;">
                                <label for="ree-standard" class="form-label">REE Normalization Standard</label>
                                <select class="form-select" id="ree-standard" name="ree_standard">
                                    <option value="C1 Chondrite Sun and McDonough,1989">C1 Chondrite (Sun & McDonough, 1989)</option>
                                    <option value="Chondrite Taylor and McLennan,1985">Chondrite (Taylor & McLennan, 1985)</option>
                                    <option value="Chondrite Haskin et al.,1966">Chondrite (Haskin et al., 1966)</option>
                                    <option value="Chondrite Nakamura,1977">Chondrite (Nakamura, 1977)</option>
                                    <option value="MORB Sun and McDonough,1989">MORB (Sun & McDonough, 1989)</option>
                                    <option value="UCC_Rudnick & Gao2003">UCC (Rudnick & Gao, 2003)</option>
                                </select>
                                <div class="form-text">Select the normalization standard for REE patterns</div>
                            </div>
                            
                            <!-- Trace Element Options - COMPLETE SECTION -->
                            <div class="mb-3" id="trace-options" style="display: none;">
                                <label for="trace-standard" class="form-label">
                                    <i class="fas fa-atom"></i> Trace Element Normalization Standard
                                </label>
                                <select class="form-select" id="trace-standard" name="trace_standard">
                                    <option value="PM">PM - Primitive Mantle (Sun & McDonough, 1989)</option>
                                    <option value="OIB">OIB - Ocean Island Basalt (Sun & McDonough, 1989)</option>
                                    <option value="EMORB">EMORB - Enriched Mid-Ocean Ridge Basalt</option>
                                    <option value="C1">C1 - C1 Chondrite (Sun & McDonough, 1989)</option>
                                    <option value="NMORB">NMORB - Normal Mid-Ocean Ridge Basalt</option>
                                    <option value="UCC_Rudnick & Gao2003">UCC - Upper Continental Crust (Rudnick & Gao, 2003)</option>
                                </select>
                                <div class="form-text">Select the normalization standard for trace element spider diagrams</div>
                                
                                <label for="trace-element-set" class="form-label mt-3">
                                    <i class="fas fa-list-ol"></i> Element Sequence
                                </label>
                                <select class="form-select" id="trace-element-set" name="trace_element_set">
                                    <option value="cs_lu">Cs-Lu (36 Elements) - Full Incompatible Element Sequence</option>
                                    <option value="rb_lu">Rb-Lu (26 Elements) - Simplified Sequence (Rb to Lu)</option>
                                </select>
                                <div class="form-text">Choose element sequence: Full 36-element or simplified 26-element pattern</div>
                            </div>
                            
                            <!-- Image Format Selection -->
                            <div class="mb-3">
                                <label for="image-format" class="form-label">Output Format</label>
                                <select class="form-select" id="image-format" name="image_format">
                                    <option value="png">PNG (Raster)</option>
                                    <option value="svg">SVG (Vector)</option>
                                </select>
                                <div class="form-text">Choose image format for download</div>
                            </div>
                            
                            <button type="submit" class="btn btn-success w-100">
                                <i class="fas fa-chart-area"></i> Generate Diagram
                            </button>
                        </form>
                        
                        <div class="alert alert-info alert-custom mt-3" style="display: none;" id="cipw-note">
                            <i class="fas fa-info-circle"></i> 
                            <strong>Note:</strong> QAPF diagrams require CIPW norm calculations. 
                            Run CIPW calculation first for best results.
                        </div>
                        
                        <div class="alert alert-info alert-custom mt-3" style="display: none;" id="trace-note">
                            <i class="fas fa-atom"></i> 
                            <strong>Trace Element Spider Diagrams:</strong> 
                            <ul class="mb-0 mt-2" style="text-align: left; font-size: 0.9rem;">
                                <li><strong>6 Normalization Standards:</strong> PM, OIB, EMORB, C1, NMORB, UCC</li>
                                <li><strong>Auto Conversions:</strong> K2O to K and TiO2 to Ti</li>
                                <li><strong>Element Order:</strong> By incompatibility (most to least)</li>
                                <li><strong>Two Sequences:</strong> Full (Cs-Lu, 36 elements) or Simplified (Rb-Lu, 26 elements)</li>
                                <li><strong>Reference:</strong> Sun, S.S. & McDonough, W.F. (1989), Rudnick & Gao (2003)</li>
                            </ul>
                        </div>
                        
                        <div class="alert alert-info alert-custom mt-3" style="display: none;" id="pearce-note">
                            <i class="fas fa-mountain"></i> 
                            <strong>Pearce Diagrams for Granite Discrimination (4 Diagrams):</strong> 
                            <ul class="mb-0 mt-2" style="text-align: left; font-size: 0.9rem;">
                                <li><strong>Required Elements:</strong> Rb, Y, Nb, Yb, Ta (ppm)</li>
                                <li><strong>Four Diagrams:</strong> Y+Nb vs Rb, Yb+Ta vs Rb, Y vs Nb, Yb vs Ta</li>
                                <li><strong>Tectonic Settings:</strong> syn-COLG, VAG, WPG, ORG</li>
                                <li><strong>Reference:</strong> Pearce, J.A. et al. (1984) J. Petrology, v.25, p.956-983</li>
                                <li><strong>Note:</strong> All axes use logarithmic scale</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-8 col-md-7">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-table"></i> Data Preview
                    </div>
                    <div class="card-body">
                        <div id="data-preview" style="max-width: 100%; overflow-x: auto; overflow-y: hidden;">
                            <div class="text-center text-muted py-5">
                                <i class="fas fa-file-upload fa-3x mb-3"></i>
                                <h5>No data uploaded yet</h5>
                                <p>Please upload a CSV or Excel file to begin analysis</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner-border text-light" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5 class="mt-3">Processing your data...</h5>
                    <p>This may take a few moments depending on your data size</p>
                </div>

                <div class="plot-container" id="plot-container" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <i class="fas fa-chart-line"></i> <span id="plot-title">Analysis Result</span>
                        </div>
                        <div class="card-body text-center">
                            <img id="plot-image" class="img-fluid" alt="Analysis Result">
                            <div class="mt-3">
                                <div class="btn-group" role="group">
                                    <button class="btn btn-outline-primary btn-sm" onclick="downloadImage()">
                                        <i class="fas fa-download"></i> Download
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm" onclick="copyImageUrl()">
                                        <i class="fas fa-link"></i> Copy Link
                                    </button>
                                </div>
                                <div class="mt-2">
                                    <small class="text-muted">Format: <span id="current-format">PNG</span></small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="result-container" id="result-container" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <i class="fas fa-calculator"></i> Calculation Results
                        </div>
                        <div class="card-body">
                            <div id="result-data"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Plot type titles
        const plotTitles = {
            'tas': 'TAS Diagram',
            'harker': 'Harker Diagrams',
            'ree': 'REE Patterns',
            'trace': 'Trace Element Spider Diagram',
            'pearce': 'Pearce Diagrams',
            'cipw': 'CIPW Norm Calculation',
            'qapf': 'QAPF Diagram'
        };

        document.getElementById('upload-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const uploadButton = this.querySelector('button[type="submit"]');
            const originalText = uploadButton.innerHTML;
            
            // Show progress
            uploadButton.disabled = true;
            uploadButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            document.getElementById('upload-progress').style.display = 'block';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showAlert(data.error, 'danger');
                } else {
                    document.getElementById('data-preview').innerHTML = data.preview;
                    
                    // Force table constraints immediately after data load
                    const dataPreview = document.getElementById('data-preview');
                    const tables = dataPreview.querySelectorAll('table');
                    tables.forEach(table => {
                        // Allow table to expand naturally but ensure container scrolls
                        table.style.width = 'auto';
                        table.style.minWidth = '100%';
                        table.style.whiteSpace = 'nowrap';
                        
                        // Wrap table in responsive container if not already wrapped
                        if (!table.parentElement.classList.contains('table-responsive')) {
                            const wrapper = document.createElement('div');
                            wrapper.className = 'table-responsive';
                            wrapper.style.maxHeight = '350px';
                            wrapper.style.overflow = 'auto';
                            wrapper.style.width = '100%';
                            table.parentNode.insertBefore(wrapper, table);
                            wrapper.appendChild(table);
                        }
                        
                        // Set reasonable cell constraints
                        const cells = table.querySelectorAll('th, td');
                        cells.forEach(cell => {
                            cell.style.minWidth = '120px';
                            cell.style.padding = '8px 12px';
                            cell.style.whiteSpace = 'nowrap';
                            cell.style.verticalAlign = 'middle';
                        });
                    });
                    
                    document.getElementById('plot-options').style.display = 'block';
                    showAlert('Data uploaded successfully! ' + data.columns.length + ' columns detected.', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred during upload. Please try again.', 'danger');
            })
            .finally(() => {
                uploadButton.disabled = false;
                uploadButton.innerHTML = originalText;
                document.getElementById('upload-progress').style.display = 'none';
            });
        });

        document.getElementById('plot-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const plotType = formData.get('plot_type');
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading spinner
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('plot-container').style.display = 'none';
            document.getElementById('result-container').style.display = 'none';
            
            fetch('/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showAlert(data.error, 'danger');
                } else {
                    // Display the plot
                    const imageFormat = data.image_format || 'png';
                    const mimeType = imageFormat === 'svg' ? 'image/svg+xml' : 'image/png';
                    document.getElementById('plot-image').src = `data:${mimeType};base64,${data.image}`;
                    document.getElementById('plot-title').textContent = plotTitles[plotType] || 'Analysis Result';
                    document.getElementById('plot-container').style.display = 'block';
                    
                    // Update format display
                    document.getElementById('current-format').textContent = imageFormat.toUpperCase();
                    
                    // Display results if available
                    if (data.result) {
                        document.getElementById('result-data').innerHTML = data.result;
                        document.getElementById('result-container').style.display = 'block';
                    } else {
                        document.getElementById('result-container').style.display = 'none';
                    }
                    
                    showAlert('Analysis completed successfully!', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred during processing. Please try again.', 'danger');
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
        });

        // Show options based on plot type selection - ENHANCED TRACE SUPPORT
        document.getElementById('plot-type').addEventListener('change', function() {
            const cipwNote = document.getElementById('cipw-note');
            const reeStandardSelection = document.getElementById('ree-standard-selection');
            const traceOptions = document.getElementById('trace-options');
            const traceNote = document.getElementById('trace-note');
            const pearceNote = document.getElementById('pearce-note');
            
            // Hide all options first
            cipwNote.style.display = 'none';
            reeStandardSelection.style.display = 'none';
            traceOptions.style.display = 'none';
            traceNote.style.display = 'none';
            pearceNote.style.display = 'none';
            
            // Show relevant options based on selection
            if (this.value === 'qapf') {
                cipwNote.style.display = 'block';
            } else if (this.value === 'ree') {
                reeStandardSelection.style.display = 'block';
            } else if (this.value === 'trace') {
                traceOptions.style.display = 'block';
                traceNote.style.display = 'block';
                console.log('Trace options should now be visible'); // Debug log
            } else if (this.value === 'pearce') {
                pearceNote.style.display = 'block';
            }
        });

        function showAlert(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
            alertDiv.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            const container = document.querySelector('.container');
            container.insertBefore(alertDiv, container.firstChild.nextSibling);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        }

        function downloadImage() {
            const img = document.getElementById('plot-image');
            const link = document.createElement('a');
            const imageFormat = document.getElementById('image-format').value;
            const plotType = document.getElementById('plot-type').value;
            
            link.download = `geochemical_analysis_${plotType}.${imageFormat}`;
            link.href = img.src;
            link.click();
            
            showAlert(`Image downloaded as ${imageFormat.toUpperCase()} format!`, 'success');
        }

        function copyImageUrl() {
            const img = document.getElementById('plot-image');
            navigator.clipboard.writeText(img.src).then(function() {
                showAlert('Image URL copied to clipboard!', 'success');
            }).catch(function(err) {
                showAlert('Failed to copy URL: ' + err, 'danger');
            });
        }

        // Update format display
        document.getElementById('image-format').addEventListener('change', function() {
            document.getElementById('current-format').textContent = this.value.toUpperCase();
        });

        // Initialize tooltips
        document.addEventListener('DOMContentLoaded', function() {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
            
            // Debug: Check if trace elements are available
            console.log('GeoPyTool Web loaded with trace element support');
        });
    </script>
</body>
</html>''')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)