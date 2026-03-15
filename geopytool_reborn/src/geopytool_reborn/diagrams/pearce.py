# -*- coding: utf-8 -*-
"""
Pearce Tectonic Discrimination Diagrams

Trace element discrimination diagrams for determining tectonic settings
of granitic rocks. Displays all four diagrams in a 2x2 grid.

Reference:
- Pearce, J.A., Harris, N.B.W. and Tindle, A.G., 1984. Trace element 
  discrimination diagrams for the tectonic interpretation of granitic rocks.
  Journal of Petrology, 25(4), pp.956-983.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox

from ..core.base_widget import BasePlotWindow
from ..resources.i18n import tr


class Pearce(BasePlotWindow):
    """
    Pearce tectonic discrimination diagrams for granites.
    
    Displays all four diagrams in a 2x2 grid with square aspect ratio.
    """
    
    title = "Pearce Tectonic Discrimination Diagram"
    reference = ("Pearce, J.A. et al., 1984. Trace element discrimination "
                 "diagrams for the tectonic interpretation of granitic rocks. "
                 "Journal of Petrology, 25(4), 956-983.")
    items_to_check = ['Y', 'Nb', 'Rb', 'Yb', 'Ta']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.axes_array = None
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add Pearce diagram-specific controls."""
        self.legend_cb = QCheckBox(tr('cb_legend'))
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        self.control_layout.addWidget(self.legend_cb)
        
        self.fields_cb = QCheckBox(tr('cb_fields'))
        self.fields_cb.setChecked(True)
        self.fields_cb.stateChanged.connect(self.plot)
        self.control_layout.addWidget(self.fields_cb)
    
    def plot(self):
        """Draw all four Pearce diagrams in 2x2 grid."""
        self.fig.clear()
        
        self.axes_array = self.fig.subplots(2, 2)
        
        self._plot_ynb_rb(self.axes_array[0, 0])
        self._plot_ybta_rb(self.axes_array[0, 1])
        self._plot_y_nb(self.axes_array[1, 0])
        self._plot_yb_ta(self.axes_array[1, 1])
        
        self.fig.tight_layout()
        
        if self.legend_cb.isChecked() and not self._df.empty:
            handles, labels = self.axes_array[0, 0].get_legend_handles_labels()
            if handles:
                self.axes_array[0, 0].legend(loc='upper left', fontsize=7)
        
        self.canvas.draw()
    
    def _setup_log_axes(self, ax, x_label, y_label, x_lim, y_lim):
        """Setup log-log axes with square aspect ratio."""
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel(x_label, fontsize=9)
        ax.set_ylabel(y_label, fontsize=9)
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.grid(True, which='both', linestyle='--', alpha=0.3)
        ax.set_aspect('equal', adjustable='box')
    
    def _plot_ynb_rb(self, ax):
        """Plot Y+Nb vs Rb diagram."""
        self._setup_log_axes(ax, 'Y + Nb (ppm)', 'Rb (ppm)', (1, 3000), (1, 3000))
        ax.set_title('Y+Nb vs Rb', fontsize=10)
        self._draw_ynb_rb_boundaries(ax)
        if not self._df.empty:
            self._plot_data_log(ax, 'Y', 'Nb', 'Rb', combine_x=True)
    
    def _plot_ybta_rb(self, ax):
        """Plot Yb+Ta vs Rb diagram."""
        self._setup_log_axes(ax, 'Yb + Ta (ppm)', 'Rb (ppm)', (0.1, 300), (1, 3000))
        ax.set_title('Yb+Ta vs Rb', fontsize=10)
        self._draw_ybta_rb_boundaries(ax)
        if not self._df.empty:
            self._plot_data_log(ax, 'Yb', 'Ta', 'Rb', combine_x=True)
    
    def _plot_y_nb(self, ax):
        """Plot Y vs Nb diagram."""
        self._setup_log_axes(ax, 'Y (ppm)', 'Nb (ppm)', (1, 3000), (1, 3000))
        ax.set_title('Y vs Nb', fontsize=10)
        self._draw_y_nb_boundaries(ax)
        if not self._df.empty:
            self._plot_data_log(ax, 'Y', None, 'Nb', combine_x=False)
    
    def _plot_yb_ta(self, ax):
        """Plot Yb vs Ta diagram."""
        self._setup_log_axes(ax, 'Yb (ppm)', 'Ta (ppm)', (0.1, 100), (0.01, 100))
        ax.set_title('Yb vs Ta', fontsize=10)
        self._draw_yb_ta_boundaries(ax)
        if not self._df.empty:
            self._plot_data_log(ax, 'Yb', None, 'Ta', combine_x=False)
    
    def _draw_ynb_rb_boundaries(self, ax):
        boundaries = [
            [(2, 80), (55, 300)], [(55, 300), (400, 2000)],
            [(55, 300), (51.5, 8)], [(51.5, 8), (50, 1)], [(51.5, 8), (2000, 400)]
        ]
        for boundary in boundaries:
            ax.plot([p[0] for p in boundary], [p[1] for p in boundary], 'k-', linewidth=1, alpha=0.7)
        if self.fields_cb.isChecked():
            ax.text(10, 1000, 'syn-COLG', fontsize=8, ha='center')
            ax.text(10, 10, 'VAG', fontsize=8, ha='center')
            ax.text(250, 250, 'WPG', fontsize=8, ha='center')
            ax.text(1000, 10, 'ORG', fontsize=8, ha='center')
    
    def _draw_ybta_rb_boundaries(self, ax):
        boundaries = [
            [(0.5, 140), (6, 200)], [(6, 200), (50, 2000)],
            [(6, 200), (6, 8)], [(6, 8), (6, 1)], [(6, 8), (200, 400)]
        ]
        for boundary in boundaries:
            ax.plot([p[0] for p in boundary], [p[1] for p in boundary], 'k-', linewidth=1, alpha=0.7)
        if self.fields_cb.isChecked():
            ax.text(1, 1000, 'syn-COLG', fontsize=8, ha='center')
            ax.text(1, 10, 'VAG', fontsize=8, ha='center')
            ax.text(30, 250, 'WPG', fontsize=8, ha='center')
            ax.text(100, 10, 'ORG', fontsize=8, ha='center')
    
    def _draw_y_nb_boundaries(self, ax):
        boundaries = [
            [(1, 2000), (50, 10)], [(40, 1), (50, 10)],
            [(50, 10), (1000, 100)], [(25, 25), (1000, 400)]
        ]
        for boundary in boundaries:
            ax.plot([p[0] for p in boundary], [p[1] for p in boundary], 'k-', linewidth=1, alpha=0.7)
        if self.fields_cb.isChecked():
            ax.text(100, 100, 'WPG', fontsize=8, ha='center')
            ax.text(150, 2, 'ORG', fontsize=8, ha='center')
            ax.text(10, 50, 'VAG+\nsyn-COLG', fontsize=7, ha='center')
    
    def _draw_yb_ta_boundaries(self, ax):
        boundaries = [
            [(0.55, 20), (3, 2)], [(0.1, 0.35), (3, 2)],
            [(3, 2), (5, 1)], [(5, 0.05), (5, 1)],
            [(5, 1), (100, 7)], [(3, 2), (100, 20)]
        ]
        for boundary in boundaries:
            ax.plot([p[0] for p in boundary], [p[1] for p in boundary], 'k-', linewidth=1, alpha=0.7)
        if self.fields_cb.isChecked():
            ax.text(0.5, 1, 'syn-COLG', fontsize=8, ha='center')
            ax.text(0.5, 0.1, 'VAG', fontsize=8, ha='center')
            ax.text(10, 10, 'WPG', fontsize=8, ha='center')
            ax.text(30, 1, 'ORG', fontsize=8, ha='center')
    
    def _plot_data_log(self, ax, x_el1, x_el2, y_el, combine_x=False):
        """Plot data points on log-log diagram."""
        if x_el1 not in self._df.columns or y_el not in self._df.columns:
            return
        if combine_x and x_el2 and x_el2 not in self._df.columns:
            return
        
        seen_labels = set()
        for idx, row in self._df.iterrows():
            try:
                if combine_x and x_el2:
                    x1, x2 = row.get(x_el1, 0), row.get(x_el2, 0)
                    if pd.isna(x1) or pd.isna(x2):
                        continue
                    x_val = x1 + x2
                else:
                    x_val = row.get(x_el1)
                    if pd.isna(x_val):
                        continue
                
                y_val = row.get(y_el)
                if pd.isna(y_val) or x_val <= 0 or y_val <= 0:
                    continue
                
                label = str(row.get('Label', ''))
                plot_label = label if label and label not in seen_labels else "_nolegend_"
                if label and label not in seen_labels:
                    seen_labels.add(label)
                
                ax.scatter(x_val, y_val, marker=row.get('Marker', 'o'),
                          c=row.get('Color', 'red'), s=row.get('Size', 40),
                          alpha=row.get('Alpha', 0.7), label=plot_label,
                          edgecolors='black', linewidths=0.5)
            except Exception:
                pass