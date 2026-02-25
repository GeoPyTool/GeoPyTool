# -*- coding: utf-8 -*-
"""
Trace Element Spider Diagram

Normalized trace element pattern diagram for displaying trace element 
abundances relative to a standard (typically primitive mantle).

Reference:
- Sun, S.S. and McDonough, W.F., 1989. Chemical and isotopic systematics 
  of oceanic basalts: implications for mantle composition and processes.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import (
    QCheckBox, QSlider, QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..ui.table_viewer import TableViewer
from ..resources.standards import TRACE_STANDARDS, TRACE_ELEMENTS_FULL, TRACE_ELEMENTS_SHORT
from ..resources.constants import OXIDE_TO_ELEMENT_FACTORS


class Trace(BasePlotWindow):
    """
    Trace Element spider diagram.
    
    Displays normalized trace element patterns with selectable normalization 
    standards. Supports both full (Cs-Lu) and abbreviated (Rb-Lu) element orders.
    """
    
    title = "Trace Element Spider Diagram"
    reference = ("Reference: Sun, S.S. and McDonough, W.F., 1989. Chemical and isotopic "
                 "systematics of oceanic basalts.")
    items_to_check = ['Rb', 'Ba', 'Th', 'U', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Sr', 'Nd', 
                      'Sm', 'Zr', 'Hf', 'Eu', 'Ti', 'Gd', 'Tb', 'Dy', 'Y', 'Ho', 
                      'Er', 'Tm', 'Yb', 'Lu']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.normalized_data = pd.DataFrame()
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add Trace-specific controls."""
        # Standard selector
        self.standard_label = QLabel("Standard:")
        self.standard_combo = QComboBox()
        self.standard_combo.addItems(list(TRACE_STANDARDS.keys()))
        self.standard_combo.currentIndexChanged.connect(self.plot)
        
        # Element range selector
        self.range_label = QLabel("Range:")
        self.range_combo = QComboBox()
        self.range_combo.addItems(["Full (Cs-Lu)", "Short (Rb-Lu)"])
        self.range_combo.currentIndexChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.show_index_cb = QCheckBox("Show Index")
        self.show_index_cb.setChecked(False)
        self.show_index_cb.stateChanged.connect(self.plot)
        
        # Results button
        self.result_button = QPushButton("Normalized Values")
        self.result_button.clicked.connect(self.show_normalized)
        
        # Add to layout
        self.control_layout.addWidget(self.standard_label)
        self.control_layout.addWidget(self.standard_combo)
        self.control_layout.addWidget(self.range_label)
        self.control_layout.addWidget(self.range_combo)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.show_index_cb)
        self.control_layout.addWidget(self.result_button)

    def plot(self):
        """Draw the trace element spider diagram."""
        self.axes.clear()
        
        # Get element list based on range selection
        use_full = "Full" in self.range_combo.currentText()
        elements = TRACE_ELEMENTS_FULL if use_full else TRACE_ELEMENTS_SHORT
        
        # Setup axes
        self.axes.set_ylabel('Sample / Standard')
        self.axes.set_yscale('log')
        self.axes.set_xlim(-0.5, len(elements) - 0.5)
        
        # X-axis labels
        x_positions = range(len(elements))
        self.axes.set_xticks(x_positions)
        self.axes.set_xticklabels(elements, rotation=-45, fontsize=7)
        
        # Grid
        self.axes.grid(True, which='both', linestyle='--', alpha=0.3)
        
        # Get normalization standard
        standard_name = self.standard_combo.currentText()
        standard = TRACE_STANDARDS.get(standard_name, {})
        
        if not standard:
            return
        
        # Plot data
        if not self._df.empty:
            self._plot_data(standard, elements)
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
                self.fig.subplots_adjust(right=0.75, bottom=0.2)
            else:
                self.fig.subplots_adjust(right=0.9, bottom=0.2)
        else:
            self.fig.subplots_adjust(right=0.9, bottom=0.2)
        
        self.canvas.draw()

    def _get_element_value(self, row, element, standard):
        """
        Get element value from row, converting from oxides if necessary.
        
        Some elements (K, Ti, P) may be reported as oxides (K2O, TiO2, P2O5).
        """
        # Direct value
        if element in row.index:
            val = row[element]
            if pd.notna(val) and val > 0:
                return val
        
        # Try oxide conversions
        oxide_map = {
            'K': ('K2O', OXIDE_TO_ELEMENT_FACTORS['K2O_to_K']),
            'Ti': ('TiO2', OXIDE_TO_ELEMENT_FACTORS['TiO2_to_Ti']),
            'P': ('P2O5', OXIDE_TO_ELEMENT_FACTORS['P2O5_to_P']),
        }
        
        if element in oxide_map:
            oxide, factor = oxide_map[element]
            if oxide in row.index:
                oxide_val = row[oxide]
                if pd.notna(oxide_val) and oxide_val > 0:
                    return oxide_val * factor
        
        return np.nan

    def _plot_data(self, standard, elements):
        """Plot normalized trace element patterns."""
        df = self._df
        
        # Prepare normalized data storage
        norm_data = {'Label': []}
        for el in elements:
            norm_data[el] = []
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            label = str(row.get('Label', f'Sample {idx}'))
            norm_data['Label'].append(label)
            
            x_vals = []
            y_vals = []
            
            # Calculate normalized values
            for i, el in enumerate(elements):
                val = self._get_element_value(row, el, standard)
                std_val = standard.get(el, np.nan)
                
                if pd.notna(val) and val > 0 and pd.notna(std_val) and std_val > 0:
                    normalized = val / std_val
                    x_vals.append(i)
                    y_vals.append(normalized)
                    norm_data[el].append(normalized)
                else:
                    norm_data[el].append(np.nan)
            
            # Plot if we have data
            if y_vals:
                # Legend handling
                if label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                color = row.get('Color', 'black')
                alpha = row.get('Alpha', 0.7)
                width = row.get('Width', 1)
                style = row.get('Style', '-')
                
                self.axes.plot(x_vals, y_vals, marker='o', markersize=4,
                              color=color, alpha=alpha, linewidth=width,
                              linestyle=style, label=plot_label)
                
                # Show index
                if self.show_index_cb.isChecked() and y_vals:
                    self.axes.annotate(str(idx), (x_vals[0], y_vals[0]),
                                      fontsize=6, alpha=0.7)
        
        # Store normalized data
        self.normalized_data = pd.DataFrame(norm_data)

    def show_normalized(self):
        """Show normalized values in a table."""
        if self.normalized_data.empty:
            return
        
        viewer = TableViewer(self.normalized_data, "Normalized Trace Element Values", self)
        viewer.show()
