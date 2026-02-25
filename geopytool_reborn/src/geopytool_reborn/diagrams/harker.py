# -*- coding: utf-8 -*-
"""
Harker Diagram Module

Variation diagrams (Harker diagrams) for plotting major element oxides
vs. SiO2 or any selected index element.

Reference:
- Harker, A., 1909. The Natural History of Igneous Rocks.
"""

import numpy as np
import pandas as pd
from scipy import stats

from PySide6.QtWidgets import (
    QCheckBox, QSlider, QLabel, QPushButton, QComboBox, QSpinBox,
    QWidget, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ..core.base_widget import BasePlotWindow, GrowingTextEdit


class Harker(BasePlotWindow):
    """
    Harker variation diagram.
    
    Plots multiple oxides against a single index oxide (typically SiO2)
    in a grid of subplots.
    """
    
    title = "Harker Diagram"
    reference = "Reference: Harker, A., 1909. The Natural History of Igneous Rocks."
    items_to_check = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 
                      'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    
    # Default Y-axis elements
    DEFAULT_Y_ELEMENTS = ['TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def _create_main_frame(self):
        """Override to use a larger figure for subplots."""
        self.resize(1200, 900)
        self.main_frame = QWidget()
        self.dpi = 100
        
        # Larger figure for multiple subplots
        self.fig = Figure((14, 10), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.35, wspace=0.3, left=0.08, bottom=0.08, right=0.95, top=0.95)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        # Navigation toolbar
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Save button
        self.save_button = QPushButton('&Save Image')
        self.save_button.clicked.connect(self.save_image)
        
        # Layout
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.save_button)
        
        # Call subclass method to add custom controls
        self.create_controls()
        
        self.control_layout.addStretch()
        
        # Reference textbox
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        self.textbox.setReadOnly(True)
        
        # Main layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.control_layout)
        self.vbox.addWidget(self.textbox)
        
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_controls(self):
        """Add Harker-specific controls."""
        # X-axis element selector
        self.x_label = QLabel("X-axis:")
        self.x_combo = QComboBox()
        self.x_combo.addItems(['SiO2', 'MgO', 'FeO', 'CaO', 'Al2O3'])
        self.x_combo.currentIndexChanged.connect(self.plot)
        
        # Grid size
        self.cols_label = QLabel("Columns:")
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(2, 5)
        self.cols_spin.setValue(3)
        self.cols_spin.valueChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.regression_cb = QCheckBox("Regression")
        self.regression_cb.setChecked(False)
        self.regression_cb.stateChanged.connect(self.plot)
        
        # Add to layout
        self.control_layout.addWidget(self.x_label)
        self.control_layout.addWidget(self.x_combo)
        self.control_layout.addWidget(self.cols_label)
        self.control_layout.addWidget(self.cols_spin)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.regression_cb)

    def plot(self):
        """Draw Harker variation diagrams."""
        self.fig.clear()
        
        if self._df.empty:
            return
        
        df = self._df
        x_element = self.x_combo.currentText()
        
        if x_element not in df.columns:
            return
        
        # Find available Y elements
        y_elements = [el for el in self.DEFAULT_Y_ELEMENTS 
                     if el in df.columns and el != x_element]
        
        if not y_elements:
            return
        
        # Calculate grid dimensions
        n_cols = self.cols_spin.value()
        n_rows = (len(y_elements) + n_cols - 1) // n_cols
        
        # Create subplots
        seen_labels = set()
        
        for i, y_element in enumerate(y_elements):
            ax = self.fig.add_subplot(n_rows, n_cols, i + 1)
            
            # Plot data by label groups
            for label in df['Label'].unique():
                group = df[df['Label'] == label]
                
                x_data = group[x_element].values
                y_data = group[y_element].values
                
                # Filter valid data
                valid = ~(np.isnan(x_data) | np.isnan(y_data))
                x_valid = x_data[valid]
                y_valid = y_data[valid]
                
                if len(x_valid) == 0:
                    continue
                
                # Get styling from first row
                row = group.iloc[0]
                color = row.get('Color', 'red')
                marker = row.get('Marker', 'o')
                size = row.get('Size', 20)
                alpha = row.get('Alpha', 0.7)
                
                # Only add to legend once
                if label not in seen_labels and self.legend_cb.isChecked():
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                ax.scatter(x_valid, y_valid, marker=marker, c=color, 
                          s=size, alpha=alpha, label=plot_label, edgecolors='none')
                
                # Regression line
                if self.regression_cb.isChecked() and len(x_valid) >= 3:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid, y_valid)
                    x_line = np.array([x_valid.min(), x_valid.max()])
                    y_line = slope * x_line + intercept
                    ax.plot(x_line, y_line, color=color, linewidth=1, alpha=0.5, linestyle='--')
            
            ax.set_xlabel(f'{x_element} (wt%)', fontsize=9)
            ax.set_ylabel(f'{y_element} (wt%)', fontsize=9)
            ax.tick_params(labelsize=8)
        
        # Add legend to first subplot
        if self.legend_cb.isChecked() and seen_labels:
            ax_first = self.fig.axes[0] if self.fig.axes else None
            if ax_first:
                ax_first.legend(fontsize=7, loc='best')
        
        self.canvas.draw()
