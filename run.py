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
from matplotlib.figure import Figure
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session
from werkzeug.utils import secure_filename
import zipfile
from io import BytesIO

# Import necessary GeoPyTool modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create a modified version of ImportDependence for web
class WebDependence:
    pass

# Create a simplified CustomClass for web
class WebCustomClass:
    pass

# We'll implement our own simplified versions of the GeoPyTool modules
# instead of importing them directly to avoid dependencies issues

# Base class for all plot types
class BasePlot:
    def __init__(self, df=None, fig=None):
        self.df = df
        self.fig = fig or plt.figure(figsize=(10, 8))
        
    def plot(self):
        pass

# TAS diagram implementation
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
        
        # Plot the data points
        ax.scatter(self.df['SiO2'], self.df['Na2O'] + self.df['K2O'], marker='o', color='red', alpha=0.6)
        
        # Set labels and title
        ax.set_xlabel('SiO2 (wt%)')
        ax.set_ylabel('Na2O + K2O (wt%)')
        ax.set_title('TAS Diagram')
        
        # Set axis limits
        ax.set_xlim(35, 80)
        ax.set_ylim(0, 16)
        
        # Draw the TAS fields (simplified)
        ax.text(43, 11, 'Foidite', fontsize=8)
        ax.text(48, 7, 'Tephrite\nBasanite', fontsize=8)
        ax.text(45, 3, 'Picro-\nbasalt', fontsize=8)
        ax.text(52, 3, 'Basalt', fontsize=8)
        ax.text(57, 5, 'Basaltic\nAndesite', fontsize=8)
        ax.text(63, 6, 'Andesite', fontsize=8)
        ax.text(69, 7, 'Dacite', fontsize=8)
        ax.text(74, 8, 'Rhyolite', fontsize=8)
        ax.text(60, 12, 'Phonolite', fontsize=8)
        ax.text(57, 9, 'Trachyte', fontsize=8)
        ax.text(52, 10, 'Tephri-\nphonolite', fontsize=8)
        ax.text(49, 8, 'Phono-\ntephrite', fontsize=8)
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.7)

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
            ax.scatter(self.df['SiO2'], self.df[oxide], marker='o', color='blue', alpha=0.6)
            ax.set_xlabel('SiO2 (wt%)')
            ax.set_ylabel(f'{oxide} (wt%)')
            ax.grid(True, linestyle='--', alpha=0.5)
            
        self.fig.tight_layout()
        self.fig.suptitle('Harker Diagrams', fontsize=16)
        self.fig.subplots_adjust(top=0.92)

# REE diagram implementation
class REE(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # REE elements in order
        ree_elements = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        available_rees = [ree for ree in ree_elements if ree in self.df.columns]
        
        if not available_rees:
            plt.text(0.5, 0.5, 'No REE columns found', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Chondrite normalization values (simplified)
        chondrite = {
            'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
            'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
            'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254
        }
        
        # Plot each sample
        for i, row in self.df.iterrows():
            ree_values = [row[ree] / chondrite[ree] if not pd.isna(row[ree]) else np.nan for ree in available_rees]
            ax.plot(range(len(available_rees)), ree_values, marker='o', label=f'Sample {i+1}')
            
        # Set x-axis labels to REE names
        ax.set_xticks(range(len(available_rees)))
        ax.set_xticklabels(available_rees, rotation=45)
        
        # Set y-axis to log scale
        ax.set_yscale('log')
        
        # Set labels and title
        ax.set_xlabel('Rare Earth Elements')
        ax.set_ylabel('Sample/Chondrite')
        ax.set_title('REE Pattern')
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add a legend if there are multiple samples
        if len(self.df) > 1:
            ax.legend(loc='upper right', fontsize='small')

# Trace element diagram implementation
class Trace(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Common trace elements
        trace_elements = ['Rb', 'Ba', 'Th', 'U', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Sr', 'Nd', 'P', 'Sm', 'Zr', 'Hf', 'Ti', 'Tb', 'Y', 'Yb']
        available_traces = [elem for elem in trace_elements if elem in self.df.columns]
        
        if not available_traces:
            plt.text(0.5, 0.5, 'No trace element columns found', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Primitive mantle normalization values (simplified)
        pm_values = {
            'Rb': 0.635, 'Ba': 6.989, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713, 'Ta': 0.041,
            'K': 250, 'La': 0.687, 'Ce': 1.775, 'Sr': 21.1, 'Nd': 1.354, 'P': 95,
            'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Ti': 1300, 'Tb': 0.108, 'Y': 4.55, 'Yb': 0.493
        }
        
        # Plot each sample
        for i, row in self.df.iterrows():
            trace_values = [row[elem] / pm_values[elem] if not pd.isna(row[elem]) else np.nan for elem in available_traces]
            ax.plot(range(len(available_traces)), trace_values, marker='o', label=f'Sample {i+1}')
            
        # Set x-axis labels to trace element names
        ax.set_xticks(range(len(available_traces)))
        ax.set_xticklabels(available_traces, rotation=45)
        
        # Set y-axis to log scale
        ax.set_yscale('log')
        
        # Set labels and title
        ax.set_xlabel('Trace Elements')
        ax.set_ylabel('Sample/Primitive Mantle')
        ax.set_title('Trace Element Pattern')
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add a legend if there are multiple samples
        if len(self.df) > 1:
            ax.legend(loc='upper right', fontsize='small')

# Pearce diagram implementation
class Pearce(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Check if required columns exist
        required_cols = ['Rb', 'Y', 'Nb']
        if not all(col in self.df.columns for col in required_cols):
            plt.text(0.5, 0.5, 'Missing required columns: Rb, Y, Nb', 
                    horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
            return
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Plot the data points
        ax.scatter(self.df['Y'] + self.df['Nb'], self.df['Rb'], marker='o', color='green', alpha=0.6)
        
        # Set labels and title
        ax.set_xlabel('Y + Nb (ppm)')
        ax.set_ylabel('Rb (ppm)')
        ax.set_title('Pearce Diagram (Rb vs Y+Nb)')
        
        # Set log scales
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        # Set axis limits
        ax.set_xlim(1, 2000)
        ax.set_ylim(0.1, 2000)
        
        # Add field labels
        ax.text(5, 1000, 'Syn-COLG', fontsize=10)
        ax.text(200, 1000, 'VAG', fontsize=10)
        ax.text(200, 5, 'ORG', fontsize=10)
        ax.text(50, 5, 'WPG', fontsize=10)
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.7)

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

# QAPF diagram implementation
class QAPF(BasePlot):
    def plot(self):
        if self.df is None or self.fig is None:
            return
            
        # Check if we have CIPW norm results
        cipw_cols = ['Quartz', 'Orthoclase', 'Albite', 'Anorthite']
        if not all(col in self.df.columns for col in cipw_cols):
            # Try to calculate CIPW norm
            cipw = CIPW(df=self.df)
            cipw.calculate()
            if cipw.result_df is not None:
                norm_df = cipw.result_df
            else:
                plt.text(0.5, 0.5, 'Missing required CIPW norm columns and unable to calculate them', 
                        horizontalalignment='center', verticalalignment='center', transform=self.fig.transFigure)
                return
        else:
            norm_df = self.df
            
        # Get the axes
        ax = self.fig.add_subplot(111)
        
        # Calculate QAPF parameters
        for i, row in norm_df.iterrows():
            q = row['Quartz']
            a = row['Orthoclase']
            p = row['Albite']
            f = row['Anorthite']
            
            # Normalize to 100%
            total = q + a + p + f
            if total > 0:
                q_norm = q / total * 100
                a_norm = a / total * 100
                p_norm = p / total * 100
                f_norm = f / total * 100
                
                # Plot in ternary diagram (simplified as a scatter plot)
                # This is a very simplified representation of a ternary plot
                ax.scatter(a_norm, p_norm, marker='o', color='purple', alpha=0.6)
        
        # Set labels and title
        ax.set_xlabel('Orthoclase (A)')
        ax.set_ylabel('Plagioclase (P)')
        ax.set_title('Simplified QAPF Diagram')
        
        # Set axis limits
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add a note about the simplification
        ax.text(50, 50, 'Note: This is a simplified 2D representation\nof the QAPF diagram', 
                horizontalalignment='center', verticalalignment='center', fontsize=8)

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

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

def process_plot(plot_function, df, **kwargs):
    try:
        # Create a figure
        fig = plt.figure(figsize=(10, 8))
        
        # Call the appropriate plot function
        result = plot_function(df=df, fig=fig, **kwargs)
        
        # Convert the figure to base64 string
        img_str = fig_to_base64(fig)
        plt.close(fig)
        
        return img_str, result
    except Exception as e:
        plt.close()
        return None, str(e)

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
    
    try:
        df = read_dataframe(file_path)
        
        # Process based on plot type
        if plot_type == 'tas':
            img_str, result = process_tas(df)
        elif plot_type == 'harker':
            img_str, result = process_harker(df)
        elif plot_type == 'ree':
            img_str, result = process_ree(df)
        elif plot_type == 'trace':
            img_str, result = process_trace(df)
        elif plot_type == 'pearce':
            img_str, result = process_pearce(df)
        elif plot_type == 'cipw':
            img_str, result = process_cipw(df)
        elif plot_type == 'qapf':
            img_str, result = process_qapf(df)
        # Add more plot types as needed
        else:
            return jsonify({'error': f'Unknown plot type: {plot_type}'})
        
        if img_str:
            return jsonify({
                'success': True,
                'image': img_str,
                'result': result if isinstance(result, str) else None
            })
        else:
            return jsonify({'error': result})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Plot processing functions
def process_tas(df):
    tas = TAS(df=df)
    fig = plt.figure(figsize=(10, 8))
    tas.fig = fig
    tas.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

def process_harker(df):
    harker = Harker(df=df)
    fig = plt.figure(figsize=(10, 8))
    harker.fig = fig
    harker.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

def process_ree(df):
    ree = REE(df=df)
    fig = plt.figure(figsize=(10, 8))
    ree.fig = fig
    ree.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

def process_trace(df):
    trace = Trace(df=df)
    fig = plt.figure(figsize=(10, 8))
    trace.fig = fig
    trace.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

def process_pearce(df):
    pearce = Pearce(df=df)
    fig = plt.figure(figsize=(10, 8))
    pearce.fig = fig
    pearce.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

def process_cipw(df):
    cipw = CIPW(df=df)
    cipw.calculate()
    result_df = cipw.result_df
    
    if result_df is None:
        return None, "Failed to calculate CIPW norm. Check if all required oxide columns are present."
    
    # Convert result to HTML table
    result_html = result_df.to_html(classes='table table-striped table-sm')
    
    # Create a simple bar chart of the results
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Plot the first sample as a bar chart
    if len(result_df) > 0:
        result_df.iloc[0].plot(kind='bar', ax=ax)
        ax.set_title('CIPW Norm Results (Sample 1)')
        ax.set_ylabel('Weight %')
        ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    
    return img_str, result_html

def process_qapf(df):
    qapf = QAPF(df=df)
    fig = plt.figure(figsize=(10, 8))
    qapf.fig = fig
    qapf.plot()
    img_str = fig_to_base64(fig)
    plt.close(fig)
    return img_str, None

# Create HTML templates directory and files
os.makedirs('templates', exist_ok=True)

# Create index.html template
with open('templates/index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoPyTool Web</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 20px;
        }
        .header {
            padding-bottom: 20px;
            border-bottom: 1px solid #e5e5e5;
            margin-bottom: 30px;
        }
        .plot-container {
            margin-top: 20px;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .result-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>GeoPyTool Web</h1>
            <p class="lead">Web version of GeoPyTool for geochemical analysis and plotting</p>
        </div>

        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        Upload Data
                    </div>
                    <div class="card-body">
                        <form id="upload-form" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="file" class="form-label">Select CSV or Excel file</label>
                                <input type="file" class="form-control" id="file" name="file" accept=".csv,.xlsx,.xls">
                            </div>
                            <button type="submit" class="btn btn-primary">Upload</button>
                        </form>
                    </div>
                </div>

                <div class="card mt-3" id="plot-options" style="display: none;">
                    <div class="card-header">
                        Plot Options
                    </div>
                    <div class="card-body">
                        <form id="plot-form">
                            <div class="mb-3">
                                <label for="plot-type" class="form-label">Select Plot Type</label>
                                <select class="form-select" id="plot-type" name="plot_type">
                                    <option value="tas">TAS Diagram</option>
                                    <option value="harker">Harker Diagram</option>
                                    <option value="ree">REE Diagram</option>
                                    <option value="trace">Trace Element Diagram</option>
                                    <option value="pearce">Pearce Diagram</option>
                                    <option value="cipw">CIPW Norm Calculation</option>
                                    <option value="qapf">QAPF Diagram</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success">Generate Plot</button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        Data Preview
                    </div>
                    <div class="card-body">
                        <div id="data-preview">
                            <p>No data uploaded yet. Please upload a file.</p>
                        </div>
                    </div>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>Processing data...</p>
                </div>

                <div class="plot-container" id="plot-container" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            Plot Result
                        </div>
                        <div class="card-body text-center">
                            <img id="plot-image" class="img-fluid" alt="Plot Result">
                        </div>
                    </div>
                </div>

                <div class="result-container" id="result-container" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            Calculation Results
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
        document.getElementById('upload-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('data-preview').innerHTML = data.preview;
                    document.getElementById('plot-options').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during upload');
            });
        });

        document.getElementById('plot-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            // Show loading spinner
            document.getElementById('loading').style.display = 'block';
            document.getElementById('plot-container').style.display = 'none';
            document.getElementById('result-container').style.display = 'none';
            
            fetch('/process', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading spinner
                document.getElementById('loading').style.display = 'none';
                
                if (data.error) {
                    alert(data.error);
                } else {
                    // Display the plot
                    document.getElementById('plot-image').src = 'data:image/png;base64,' + data.image;
                    document.getElementById('plot-container').style.display = 'block';
                    
                    // Display results if available
                    if (data.result) {
                        document.getElementById('result-data').innerHTML = data.result;
                        document.getElementById('result-container').style.display = 'block';
                    } else {
                        document.getElementById('result-container').style.display = 'none';
                    }
                }
            })
            .catch(error => {
                // Hide loading spinner
                document.getElementById('loading').style.display = 'none';
                console.error('Error:', error);
                alert('An error occurred during processing');
            });
        });
    </script>
</body>
</html>''')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 