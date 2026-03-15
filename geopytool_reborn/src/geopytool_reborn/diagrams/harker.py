# -*- coding: utf-8 -*-
"""
Harker Diagram Module

Variation diagrams (Harker diagrams) for plotting major element oxides
vs. SiO2 or any selected index element. Each subplot has square aspect ratio.

Reference:
- Harker, A., 1909. The Natural History of Igneous Rocks.
"""

import numpy as np
import pandas as pd
from scipy import stats

from PySide6.QtWidgets import QCheckBox, QLabel, QComboBox

from ..core.base_widget import BasePlotWindow
from ..resources.i18n import tr


class Harker(BasePlotWindow):
    """
    Harker variation diagram.
    
    Plots multiple oxides against a single index oxide (typically SiO2)
    in a grid of subplots, each with square aspect ratio.
    """
    
    title = "Harker Diagram"
    reference = "Harker, A., 1909. The Natural History of Igneous Rocks."
    items_to_check = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 
                      'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    
    DEFAULT_Y_ELEMENTS = ['TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.axes_array = None
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add Harker-specific controls."""
        self.x_label = QLabel(tr('label_x_axis'))
        self.control_layout.addWidget(self.x_label)
        
        self.x_combo = QComboBox()
        self.x_combo.addItems(['SiO2', 'MgO', 'FeO', 'CaO', 'Al2O3'])
        self.x_combo.currentIndexChanged.connect(self.plot)
        self.control_layout.addWidget(self.x_combo)
        
        self.legend_cb = QCheckBox(tr('cb_legend'))
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        self.control_layout.addWidget(self.legend_cb)
        
        self.regression_cb = QCheckBox(tr('cb_regression'))
        self.regression_cb.setChecked(False)
        self.regression_cb.stateChanged.connect(self.plot)
        self.control_layout.addWidget(self.regression_cb)
    
    def plot(self):
        """Draw Harker variation diagrams with square subplots."""
        self.fig.clear()
        
        if self._df.empty:
            self.canvas.draw()
            return
        
        x_element = self.x_combo.currentText()
        if x_element not in self._df.columns:
            self.canvas.draw()
            return
        
        y_elements = [el for el in self.DEFAULT_Y_ELEMENTS 
                     if el in self._df.columns and el != x_element]
        
        if not y_elements:
            self.canvas.draw()
            return
        
        n_plots = len(y_elements)
        n_cols = int(np.ceil(np.sqrt(n_plots)))
        n_rows = int(np.ceil(n_plots / n_cols))
        
        self.axes_array = self.fig.subplots(n_rows, n_cols, squeeze=False)
        
        seen_labels = set()
        
        for i, y_element in enumerate(y_elements):
            ax = self.axes_array.flatten()[i]
            self._plot_single(ax, x_element, y_element, seen_labels)
        
        for i in range(len(y_elements), n_rows * n_cols):
            self.axes_array.flatten()[i].set_visible(False)
        
        if self.legend_cb.isChecked() and seen_labels:
            self.axes_array.flatten()[0].legend(fontsize=7, loc='best')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _plot_single(self, ax, x_element, y_element, seen_labels):
        """Plot a single Harker subplot."""
        df = self._df
        
        for label in df['Label'].unique() if 'Label' in df.columns else [None]:
            if label is None:
                group = df
                color, marker, size, alpha = 'red', 'o', 20, 0.7
            else:
                group = df[df['Label'] == label]
                row = group.iloc[0]
                color = row.get('Color', 'red')
                marker = row.get('Marker', 'o')
                size = row.get('Size', 20)
                alpha = row.get('Alpha', 0.7)
            
            x_data = group[x_element].values
            y_data = group[y_element].values
            
            valid = ~(np.isnan(x_data) | np.isnan(y_data))
            x_valid, y_valid = x_data[valid], y_data[valid]
            
            if len(x_valid) == 0:
                continue
            
            plot_label = "_nolegend_"
            if label is not None and self.legend_cb.isChecked():
                if label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
            
            ax.scatter(x_valid, y_valid, marker=marker, c=color, 
                      s=size, alpha=alpha, label=plot_label, edgecolors='none')
            
            if self.regression_cb.isChecked() and len(x_valid) >= 3:
                slope, intercept, r, p, std = stats.linregress(x_valid, y_valid)
                x_line = np.array([x_valid.min(), x_valid.max()])
                ax.plot(x_line, slope * x_line + intercept, color=color, 
                       linewidth=1, alpha=0.5, linestyle='--')
        
        ax.set_xlabel(f'{x_element} (wt%)', fontsize=9)
        ax.set_ylabel(f'{y_element} (wt%)', fontsize=9)
        ax.tick_params(labelsize=8)
        
        x_range = self._df[x_element].max() - self._df[x_element].min()
        y_range = self._df[y_element].max() - self._df[y_element].min()
        if x_range > 0 and y_range > 0:
            ax.set_aspect(x_range / y_range, adjustable='box')