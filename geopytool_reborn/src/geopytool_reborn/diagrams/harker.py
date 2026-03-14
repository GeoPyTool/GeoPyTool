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

from PySide6.QtWidgets import (
    QCheckBox, QLabel, QPushButton, QComboBox, QWidget, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ..core.base_widget import GrowingTextEdit
from ..resources.i18n import tr


class Harker(QWidget):
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
        super().__init__(parent)
        self.setWindowTitle(tr('win_harker'))
        self._df = df
        self.setMinimumSize(1000, 800)
        
        self._setup_ui()
        
        if not df.empty:
            self.plot()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.fig = Figure((12, 10), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        control_layout = QHBoxLayout()
        
        self.x_label = QLabel(tr('label_x_axis'))
        control_layout.addWidget(self.x_label)
        
        self.x_combo = QComboBox()
        self.x_combo.addItems(['SiO2', 'MgO', 'FeO', 'CaO', 'Al2O3'])
        self.x_combo.currentIndexChanged.connect(self.plot)
        control_layout.addWidget(self.x_combo)
        
        self.legend_cb = QCheckBox(tr('cb_legend'))
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        control_layout.addWidget(self.legend_cb)
        
        self.regression_cb = QCheckBox(tr('cb_regression'))
        self.regression_cb.setChecked(False)
        self.regression_cb.stateChanged.connect(self.plot)
        control_layout.addWidget(self.regression_cb)
        
        self.save_btn = QPushButton(tr('btn_save_image'))
        self.save_btn.clicked.connect(self._save_image)
        control_layout.addWidget(self.save_btn)
        
        control_layout.addStretch()
        
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        self.textbox.setReadOnly(True)
        self.textbox.setMaximumHeight(50)
        
        layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(control_layout)
        layout.addWidget(self.textbox)
    
    def plot(self):
        """Draw Harker variation diagrams with square subplots."""
        self.fig.clear()
        
        if self._df.empty:
            return
        
        df = self._df
        x_element = self.x_combo.currentText()
        
        if x_element not in df.columns:
            return
        
        y_elements = [el for el in self.DEFAULT_Y_ELEMENTS 
                     if el in df.columns and el != x_element]
        
        if not y_elements:
            return
        
        n_plots = len(y_elements)
        n_cols = int(np.ceil(np.sqrt(n_plots)))
        n_rows = int(np.ceil(n_plots / n_cols))
        
        axes = self.fig.subplots(n_rows, n_cols, squeeze=False)
        axes = axes.flatten()
        
        seen_labels = set()
        
        for i, y_element in enumerate(y_elements):
            ax = axes[i]
            
            for label in df['Label'].unique() if 'Label' in df.columns else [None]:
                if label is None:
                    group = df
                    color = 'red'
                    marker = 'o'
                    size = 20
                    alpha = 0.7
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
                x_valid = x_data[valid]
                y_valid = y_data[valid]
                
                if len(x_valid) == 0:
                    continue
                
                if label is not None and self.legend_cb.isChecked():
                    if label not in seen_labels:
                        plot_label = label
                        seen_labels.add(label)
                    else:
                        plot_label = "_nolegend_"
                else:
                    plot_label = "_nolegend_"
                
                ax.scatter(x_valid, y_valid, marker=marker, c=color, 
                          s=size, alpha=alpha, label=plot_label, edgecolors='none')
                
                if self.regression_cb.isChecked() and len(x_valid) >= 3:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid, y_valid)
                    x_line = np.array([x_valid.min(), x_valid.max()])
                    y_line = slope * x_line + intercept
                    ax.plot(x_line, y_line, color=color, linewidth=1, alpha=0.5, linestyle='--')
            
            ax.set_xlabel(f'{x_element} (wt%)', fontsize=9)
            ax.set_ylabel(f'{y_element} (wt%)', fontsize=9)
            ax.tick_params(labelsize=8)
            
            x_range = df[x_element].max() - df[x_element].min()
            y_range = df[y_element].max() - df[y_element].min()
            if x_range > 0 and y_range > 0:
                ax.set_aspect(x_range / y_range, adjustable='box')
        
        for i in range(len(y_elements), len(axes)):
            axes[i].set_visible(False)
        
        if self.legend_cb.isChecked() and seen_labels:
            axes[0].legend(fontsize=7, loc='best')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _save_image(self):
        from PySide6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)")
        
        if filepath:
            self.fig.savefig(filepath, dpi=150, bbox_inches='tight')