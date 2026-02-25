# -*- coding: utf-8 -*-
"""
Pearce Tectonic Discrimination Diagrams

Trace element discrimination diagrams for determining tectonic settings
of granitic rocks.

Reference:
- Pearce, J.A., Harris, N.B.W. and Tindle, A.G., 1984. Trace element 
  discrimination diagrams for the tectonic interpretation of granitic rocks.
  Journal of Petrology, 25(4), pp.956-983.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import (
    QCheckBox, QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..resources.constants import PEARCE_DIAGRAMS


class Pearce(BasePlotWindow):
    """
    Pearce tectonic discrimination diagrams for granites.
    
    Available diagrams:
    - Y+Nb vs Rb
    - Yb+Ta vs Rb
    - Y vs Nb
    - Yb vs Ta
    
    Tectonic fields:
    - WPG: Within-Plate Granites
    - VAG: Volcanic Arc Granites
    - syn-COLG: Syn-Collision Granites
    - ORG: Ocean Ridge Granites
    """
    
    title = "Pearce Tectonic Discrimination Diagram"
    reference = ("Reference: Pearce, J.A. et al., 1984. Trace element discrimination "
                 "diagrams for the tectonic interpretation of granitic rocks. "
                 "Journal of Petrology, 25(4), 956-983.")
    items_to_check = ['Y', 'Nb', 'Rb', 'Yb', 'Ta']
    
    # Diagram types
    DIAGRAM_TYPES = ['Y+Nb vs Rb', 'Yb+Ta vs Rb', 'Y vs Nb', 'Yb vs Ta']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add Pearce diagram-specific controls."""
        # Diagram type selector
        self.diagram_label = QLabel("Diagram:")
        self.diagram_combo = QComboBox()
        self.diagram_combo.addItems(self.DIAGRAM_TYPES)
        self.diagram_combo.currentIndexChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.fields_cb = QCheckBox("Field Labels")
        self.fields_cb.setChecked(True)
        self.fields_cb.stateChanged.connect(self.plot)
        
        self.show_index_cb = QCheckBox("Show Index")
        self.show_index_cb.setChecked(False)
        self.show_index_cb.stateChanged.connect(self.plot)
        
        # Add to layout
        self.control_layout.addWidget(self.diagram_label)
        self.control_layout.addWidget(self.diagram_combo)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.fields_cb)
        self.control_layout.addWidget(self.show_index_cb)

    def plot(self):
        """Draw the Pearce discrimination diagram."""
        self.axes.clear()
        
        diagram_name = self.diagram_combo.currentText()
        
        if diagram_name == 'Y+Nb vs Rb':
            self._plot_y_nb_rb()
        elif diagram_name == 'Yb+Ta vs Rb':
            self._plot_yb_ta_rb()
        elif diagram_name == 'Y vs Nb':
            self._plot_y_nb()
        elif diagram_name == 'Yb vs Ta':
            self._plot_yb_ta()
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(loc='best', fontsize=8)
        
        self.canvas.draw()

    def _setup_log_axes(self, x_label, y_label, x_lim, y_lim):
        """Setup log-log axes."""
        self.axes.set_xscale('log')
        self.axes.set_yscale('log')
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.set_xlim(x_lim)
        self.axes.set_ylim(y_lim)
        self.axes.grid(True, which='both', linestyle='--', alpha=0.3)

    def _plot_y_nb_rb(self):
        """Plot Y+Nb vs Rb diagram."""
        self._setup_log_axes('Y + Nb (ppm)', 'Rb (ppm)', (1, 3000), (1, 3000))
        
        # Draw boundaries
        self._draw_y_nb_rb_boundaries()
        
        # Plot data
        if not self._df.empty:
            self._plot_data_log('Y', 'Nb', 'Rb', combine_x=True)

    def _plot_yb_ta_rb(self):
        """Plot Yb+Ta vs Rb diagram."""
        self._setup_log_axes('Yb + Ta (ppm)', 'Rb (ppm)', (0.1, 300), (1, 3000))
        
        # Draw boundaries
        self._draw_yb_ta_rb_boundaries()
        
        # Plot data
        if not self._df.empty:
            self._plot_data_log('Yb', 'Ta', 'Rb', combine_x=True)

    def _plot_y_nb(self):
        """Plot Y vs Nb diagram."""
        self._setup_log_axes('Y (ppm)', 'Nb (ppm)', (1, 3000), (1, 3000))
        
        # Draw boundaries
        self._draw_y_nb_boundaries()
        
        # Plot data
        if not self._df.empty:
            self._plot_data_log('Y', None, 'Nb', combine_x=False)

    def _plot_yb_ta(self):
        """Plot Yb vs Ta diagram."""
        self._setup_log_axes('Yb (ppm)', 'Ta (ppm)', (0.1, 100), (0.01, 100))
        
        # Draw boundaries
        self._draw_yb_ta_boundaries()
        
        # Plot data
        if not self._df.empty:
            self._plot_data_log('Yb', None, 'Ta', combine_x=False)

    def _draw_y_nb_rb_boundaries(self):
        """Draw Y+Nb vs Rb field boundaries."""
        # Boundaries as polylines
        boundaries = [
            [(2, 80), (55, 300)],
            [(55, 300), (400, 2000)],
            [(55, 300), (51.5, 8)],
            [(51.5, 8), (50, 1)],
            [(51.5, 8), (2000, 400)]
        ]
        
        for boundary in boundaries:
            x = [p[0] for p in boundary]
            y = [p[1] for p in boundary]
            self.axes.plot(x, y, 'k-', linewidth=1, alpha=0.7)
        
        # Field labels
        if self.fields_cb.isChecked():
            self.axes.text(10, 1000, 'syn-COLG', fontsize=9, ha='center')
            self.axes.text(10, 10, 'VAG', fontsize=9, ha='center')
            self.axes.text(250, 250, 'WPG', fontsize=9, ha='center')
            self.axes.text(1000, 10, 'ORG', fontsize=9, ha='center')

    def _draw_yb_ta_rb_boundaries(self):
        """Draw Yb+Ta vs Rb field boundaries."""
        boundaries = [
            [(0.5, 140), (6, 200)],
            [(6, 200), (50, 2000)],
            [(6, 200), (6, 8)],
            [(6, 8), (6, 1)],
            [(6, 8), (200, 400)]
        ]
        
        for boundary in boundaries:
            x = [p[0] for p in boundary]
            y = [p[1] for p in boundary]
            self.axes.plot(x, y, 'k-', linewidth=1, alpha=0.7)
        
        if self.fields_cb.isChecked():
            self.axes.text(1, 1000, 'syn-COLG', fontsize=9, ha='center')
            self.axes.text(1, 10, 'VAG', fontsize=9, ha='center')
            self.axes.text(30, 250, 'WPG', fontsize=9, ha='center')
            self.axes.text(100, 10, 'ORG', fontsize=9, ha='center')

    def _draw_y_nb_boundaries(self):
        """Draw Y vs Nb field boundaries."""
        boundaries = [
            [(1, 2000), (50, 10)],
            [(40, 1), (50, 10)],
            [(50, 10), (1000, 100)],
            [(25, 25), (1000, 400)]
        ]
        
        for boundary in boundaries:
            x = [p[0] for p in boundary]
            y = [p[1] for p in boundary]
            self.axes.plot(x, y, 'k-', linewidth=1, alpha=0.7)
        
        if self.fields_cb.isChecked():
            self.axes.text(100, 100, 'WPG', fontsize=9, ha='center')
            self.axes.text(150, 2, 'ORG', fontsize=9, ha='center')
            self.axes.text(10, 50, 'VAG+\nsyn-COLG', fontsize=8, ha='center')

    def _draw_yb_ta_boundaries(self):
        """Draw Yb vs Ta field boundaries."""
        boundaries = [
            [(0.55, 20), (3, 2)],
            [(0.1, 0.35), (3, 2)],
            [(3, 2), (5, 1)],
            [(5, 0.05), (5, 1)],
            [(5, 1), (100, 7)],
            [(3, 2), (100, 20)]
        ]
        
        for boundary in boundaries:
            x = [p[0] for p in boundary]
            y = [p[1] for p in boundary]
            self.axes.plot(x, y, 'k-', linewidth=1, alpha=0.7)
        
        if self.fields_cb.isChecked():
            self.axes.text(0.5, 1, 'syn-COLG', fontsize=9, ha='center')
            self.axes.text(0.5, 0.1, 'VAG', fontsize=9, ha='center')
            self.axes.text(10, 10, 'WPG', fontsize=9, ha='center')
            self.axes.text(30, 1, 'ORG', fontsize=9, ha='center')

    def _plot_data_log(self, x_el1, x_el2, y_el, combine_x=False):
        """Plot data points on log-log diagram."""
        df = self._df
        
        if x_el1 not in df.columns or y_el not in df.columns:
            return
        
        if combine_x and x_el2 and x_el2 not in df.columns:
            return
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            try:
                # Get x value
                if combine_x and x_el2:
                    x1 = row.get(x_el1, 0)
                    x2 = row.get(x_el2, 0)
                    if pd.isna(x1) or pd.isna(x2):
                        continue
                    x_val = x1 + x2
                else:
                    x_val = row.get(x_el1)
                    if pd.isna(x_val):
                        continue
                
                y_val = row.get(y_el)
                if pd.isna(y_val):
                    continue
                
                if x_val <= 0 or y_val <= 0:
                    continue
                
                # Plot
                label = str(row.get('Label', ''))
                if label and label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                self.axes.scatter(
                    x_val, y_val,
                    marker=row.get('Marker', 'o'),
                    c=row.get('Color', 'red'),
                    s=row.get('Size', 40),
                    alpha=row.get('Alpha', 0.7),
                    label=plot_label,
                    edgecolors='none'
                )
                
                if self.show_index_cb.isChecked():
                    self.axes.annotate(str(idx), (x_val, y_val), fontsize=6, alpha=0.7)
                
            except Exception:
                pass
