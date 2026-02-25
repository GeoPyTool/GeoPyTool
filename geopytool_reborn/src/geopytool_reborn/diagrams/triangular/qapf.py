# -*- coding: utf-8 -*-
"""
QAPF Diagram

Classification diagram for plutonic and volcanic rocks based on modal
mineralogy (Quartz, Alkali feldspar, Plagioclase, Feldspathoid).

Reference:
- Streckeisen, A., 1976. To each plutonic rock its proper name.
  Earth-Science Reviews, 12(1), pp.1-33.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QLabel, QComboBox
from PySide6.QtCore import Qt

from ...core.base_widget import BasePlotWindow
from ...core.geometry import Tool


class QAPF(BasePlotWindow, Tool):
    """
    QAPF classification diagram for igneous rocks.
    
    A double-triangle diagram for classifying rocks based on:
    - Q: Quartz
    - A: Alkali feldspar
    - P: Plagioclase
    - F: Feldspathoid (Foid)
    
    Required columns: Q, A, P, F (or modal percentages)
    """
    
    title = "QAPF Classification Diagram"
    reference = ("Reference: Streckeisen, A., 1976. To each plutonic rock its proper name. "
                 "Earth-Science Reviews, 12(1), 1-33.")
    items_to_check = ['Q', 'A', 'P', 'F']
    
    # Field definitions for QAPF (upper triangle: Q-A-P)
    UPPER_FIELDS = {
        'Quartzolite': [[90, 0, 10], [90, 10, 0], [100, 0, 0]],
        'Quartz-rich Granitoid': [[60, 0, 40], [60, 40, 0], [90, 10, 0], [90, 0, 10]],
        'Alkali Feldspar Granite': [[20, 0, 80], [20, 80, 0], [60, 40, 0], [60, 0, 40]],
        'Granite': [[20, 0, 80], [20, 45, 35], [60, 22.5, 17.5], [60, 0, 40]],
        'Granodiorite': [[20, 45, 35], [20, 80, 0], [60, 40, 0], [60, 22.5, 17.5]],
        'Tonalite': [[5, 90, 5], [5, 0, 95], [20, 0, 80], [20, 80, 0]],
        'Syenite': [[0, 10, 90], [0, 90, 10], [5, 90, 5], [5, 0, 95]],
    }
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add QAPF-specific controls."""
        # Rock type selector
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Plutonic", "Volcanic"])
        self.type_combo.currentIndexChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.fields_cb = QCheckBox("Field Labels")
        self.fields_cb.setChecked(True)
        self.fields_cb.stateChanged.connect(self.plot)
        
        # Add to layout
        self.control_layout.addWidget(self.type_label)
        self.control_layout.addWidget(self.type_combo)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.fields_cb)

    def plot(self):
        """Draw the QAPF diagram."""
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
        # Upper triangle (Q-A-P)
        vertices = [(50, 86.6), (0, 0), (100, 0)]  # Q, A, P
        x = [v[0] for v in vertices] + [vertices[0][0]]
        y = [v[1] for v in vertices] + [vertices[0][1]]
        self.axes.plot(x, y, 'k-', linewidth=1.5)
        
        # Vertex labels
        self.axes.text(50, 90, 'Q', fontsize=12, ha='center', va='bottom', fontweight='bold')
        self.axes.text(-3, 0, 'A', fontsize=12, ha='right', va='center', fontweight='bold')
        self.axes.text(103, 0, 'P', fontsize=12, ha='left', va='center', fontweight='bold')
        
        # Lower triangle (F-A-P) - inverted below
        lower_vertices = [(50, -86.6), (0, 0), (100, 0)]  # F, A, P
        x_lower = [v[0] for v in lower_vertices] + [lower_vertices[0][0]]
        y_lower = [v[1] for v in lower_vertices] + [lower_vertices[0][1]]
        self.axes.plot(x_lower, y_lower, 'k-', linewidth=1.5)
        
        self.axes.text(50, -90, 'F', fontsize=12, ha='center', va='top', fontweight='bold')

    def _draw_divisions(self):
        """Draw internal field divisions."""
        # 5% and 10% Q lines
        for q_val in [5, 10, 20, 60, 90]:
            y = q_val * 0.866  # Convert to triangle height
            x_left = q_val / 2
            x_right = 100 - q_val / 2
            self.axes.plot([x_left, x_right], [y, y], 'k-', linewidth=0.5, alpha=0.7)
        
        # A-P division lines
        for ratio in [10, 35, 65, 90]:  # A percentages
            # Upper triangle
            x_bottom = ratio
            self.axes.plot([50, x_bottom], [86.6, 0], 'k-', linewidth=0.5, alpha=0.5)

    def _plot_data(self):
        """Plot data points on the QAPF diagram."""
        df = self._df
        
        # Check required columns
        if not all(col in df.columns for col in ['Q', 'A', 'P']):
            return
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            try:
                q = row.get('Q', 0)
                a = row.get('A', 0)
                p = row.get('P', 0)
                f = row.get('F', 0)
                
                if pd.isna(q) or pd.isna(a) or pd.isna(p):
                    continue
                
                # Normalize to Q+A+P = 100 for upper triangle (Q-bearing)
                # or F+A+P = 100 for lower triangle (F-bearing)
                total = q + a + p + f
                if total == 0:
                    continue
                
                if q > 0 and f == 0:
                    # Upper triangle
                    total_qap = q + a + p
                    if total_qap == 0:
                        continue
                    q_norm = 100 * q / total_qap
                    a_norm = 100 * a / total_qap
                    p_norm = 100 * p / total_qap
                    
                    # Convert to x, y coordinates
                    x, y = self.TriToBin(a_norm, p_norm, q_norm)
                    
                elif f > 0:
                    # Lower triangle
                    total_fap = f + a + p
                    if total_fap == 0:
                        continue
                    f_norm = 100 * f / total_fap
                    a_norm = 100 * a / total_fap
                    p_norm = 100 * p / total_fap
                    
                    # Convert to x, y (inverted for lower triangle)
                    x_temp, y_temp = self.TriToBin(a_norm, p_norm, f_norm)
                    x = x_temp
                    y = -y_temp  # Invert for lower triangle
                else:
                    continue
                
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
