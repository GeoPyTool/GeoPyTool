# -*- coding: utf-8 -*-
"""
QFL Diagram

Sandstone classification diagram based on Quartz, Feldspar, and 
Lithic fragment contents.

Reference:
- Dickinson, W.R. et al., 1983. Provenance of North American Phanerozoic 
  sandstones in relation to tectonic setting.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QLabel
from PySide6.QtCore import Qt

from ...core.base_widget import BasePlotWindow
from ...core.geometry import Tool


class QFL(BasePlotWindow, Tool):
    """
    QFL ternary diagram for sandstone provenance analysis.
    
    Components:
    - Q: Quartz (monocrystalline and polycrystalline)
    - F: Feldspar (K-feldspar and plagioclase)
    - L: Lithic fragments
    
    Tectonic fields:
    - Craton interior
    - Transitional continental
    - Basement uplift
    - Recycled orogen
    - Dissected arc
    - Transitional arc
    - Undissected arc
    
    Required columns: Q, F, L
    """
    
    title = "QFL Sandstone Provenance Diagram"
    reference = ("Reference: Dickinson, W.R. et al., 1983. Provenance of North American "
                 "Phanerozoic sandstones in relation to tectonic setting.")
    items_to_check = ['Q', 'F', 'L']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add QFL-specific controls."""
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.fields_cb = QCheckBox("Field Labels")
        self.fields_cb.setChecked(True)
        self.fields_cb.stateChanged.connect(self.plot)
        
        # Add to layout
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.fields_cb)

    def plot(self):
        """Draw the QFL diagram."""
        self.axes.clear()
        self.axes.set_aspect('equal')
        self.axes.axis('off')
        
        # Draw triangle outline
        self._draw_triangle()
        
        # Draw internal divisions
        self._draw_divisions()
        
        # Plot data
        if not self._df.empty:
            self._plot_data()
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(loc='upper right', fontsize=8)
        
        self.canvas.draw()

    def _draw_triangle(self):
        """Draw the triangle outline and vertex labels."""
        vertices = [(50, 86.6), (0, 0), (100, 0)]  # Q, F, L
        x = [v[0] for v in vertices] + [vertices[0][0]]
        y = [v[1] for v in vertices] + [vertices[0][1]]
        self.axes.plot(x, y, 'k-', linewidth=1.5)
        
        # Vertex labels
        self.axes.text(50, 90, 'Q', fontsize=12, ha='center', va='bottom', fontweight='bold')
        self.axes.text(-3, 0, 'F', fontsize=12, ha='right', va='center', fontweight='bold')
        self.axes.text(103, 0, 'L', fontsize=12, ha='left', va='center', fontweight='bold')

    def _draw_divisions(self):
        """Draw Dickinson provenance field boundaries."""
        # Field boundaries (Q%, F%, L%)
        boundaries = [
            # Craton interior boundary
            [(97, 0, 3), (75, 25, 0)],
            [(75, 25, 0), (75, 0, 25)],
            # Transitional continental boundary
            [(75, 25, 0), (46, 54, 0)],
            [(75, 0, 25), (46, 0, 54)],
            # Basement uplift boundary
            [(46, 54, 0), (18, 82, 0)],
            [(46, 0, 54), (18, 0, 82)],
            # Recycled orogen
            [(25, 25, 50), (50, 0, 50)],
            # Arc boundaries
            [(0, 77, 23), (18, 82, 0)],
            [(18, 82, 0), (45, 40, 15)],
            [(0, 53, 47), (45, 40, 15)],
        ]
        
        for boundary in boundaries:
            start = boundary[0]
            end = boundary[1]
            
            x1, y1 = self.TriToBin(start[1], start[2], start[0])
            x2, y2 = self.TriToBin(end[1], end[2], end[0])
            
            self.axes.plot([x1, x2], [y1, y2], 'k-', linewidth=0.8, alpha=0.7)
        
        # Field labels
        if self.fields_cb.isChecked():
            labels = [
                ((88, 6, 6), 'Craton\nInterior', 8),
                ((70, 15, 15), 'Transitional\nContinental', 7),
                ((45, 30, 25), 'Basement\nUplift', 7),
                ((35, 15, 50), 'Recycled\nOrogen', 7),
                ((10, 65, 25), 'Arc', 8),
            ]
            
            for pos, label, fontsize in labels:
                x, y = self.TriToBin(pos[1], pos[2], pos[0])
                self.axes.text(x, y, label, fontsize=fontsize, ha='center', va='center', alpha=0.7)

    def _plot_data(self):
        """Plot data points on the QFL diagram."""
        df = self._df
        
        # Check required columns
        if not all(col in df.columns for col in ['Q', 'F', 'L']):
            return
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            try:
                q = row.get('Q', 0)
                f = row.get('F', 0)
                l = row.get('L', 0)
                
                if pd.isna(q) or pd.isna(f) or pd.isna(l):
                    continue
                
                # Normalize to Q+F+L = 100
                total = q + f + l
                if total == 0:
                    continue
                
                q_norm = 100 * q / total
                f_norm = 100 * f / total
                l_norm = 100 * l / total
                
                # Convert to x, y coordinates
                x, y = self.TriToBin(f_norm, l_norm, q_norm)
                
                # Plot
                label = str(row.get('Label', ''))
                if label and label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                self.axes.scatter(
                    x, y,
                    marker=row.get('Marker', 'o'),
                    c=row.get('Color', 'red'),
                    s=row.get('Size', 40),
                    alpha=row.get('Alpha', 0.7),
                    label=plot_label,
                    edgecolors='none'
                )
                
            except Exception:
                pass
