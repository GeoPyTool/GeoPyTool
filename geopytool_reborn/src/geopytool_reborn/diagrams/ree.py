# -*- coding: utf-8 -*-
"""
REE (Rare Earth Elements) Spider Diagram

Normalized REE pattern diagram for displaying rare earth element abundances
relative to a standard (typically chondrite).

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
from ..resources.standards import REE_STANDARDS, REE_ELEMENTS, LREE, MREE, HREE


class REE(BasePlotWindow):
    """
    REE (Rare Earth Elements) spider diagram.
    
    Displays normalized REE patterns with selectable normalization standards.
    Calculates various REE ratios and anomalies.
    
    Required columns: La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu
    """
    
    title = "REE Spider Diagram"
    reference = ("Reference: Sun, S.S. and McDonough, W.F., 1989. Chemical and isotopic "
                 "systematics of oceanic basalts.")
    items_to_check = REE_ELEMENTS.copy()
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.normalized_data = pd.DataFrame()
        self.ratios = pd.DataFrame()
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add REE-specific controls."""
        # Standard selector
        self.standard_label = QLabel("Standard:")
        self.standard_combo = QComboBox()
        self.standard_combo.addItems(list(REE_STANDARDS.keys()))
        self.standard_combo.currentIndexChanged.connect(self.plot)
        
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
        
        self.ratio_button = QPushButton("REE Ratios")
        self.ratio_button.clicked.connect(self.show_ratios)
        
        # Add to layout
        self.control_layout.addWidget(self.standard_label)
        self.control_layout.addWidget(self.standard_combo)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.show_index_cb)
        self.control_layout.addWidget(self.result_button)
        self.control_layout.addWidget(self.ratio_button)

    def plot(self):
        """Draw the REE spider diagram."""
        self.axes.clear()
        
        # Setup axes
        self.axes.set_ylabel('Sample / Standard')
        self.axes.set_yscale('log')
        self.axes.set_xlim(0, len(REE_ELEMENTS))
        
        # X-axis labels
        x_positions = range(len(REE_ELEMENTS))
        self.axes.set_xticks(x_positions)
        self.axes.set_xticklabels(REE_ELEMENTS)
        
        # Grid
        self.axes.grid(True, which='both', linestyle='--', alpha=0.3)
        
        # Get normalization standard
        standard_name = self.standard_combo.currentText()
        standard = REE_STANDARDS.get(standard_name, {})
        
        if not standard:
            return
        
        # Plot data
        if not self._df.empty:
            self._plot_data(standard)
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
                self.fig.subplots_adjust(right=0.75)
            else:
                self.fig.subplots_adjust(right=0.9)
        else:
            self.fig.subplots_adjust(right=0.9)
        
        self.canvas.draw()

    def _plot_data(self, standard):
        """Plot normalized REE patterns."""
        df = self._df
        
        # Prepare normalized data storage
        norm_data = {'Label': []}
        for el in REE_ELEMENTS:
            norm_data[el] = []
        
        # Prepare ratio data storage
        ratio_data = []
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            label = str(row.get('Label', f'Sample {idx}'))
            norm_data['Label'].append(label)
            
            x_vals = []
            y_vals = []
            
            # Calculate normalized values
            norm_row = {}
            for i, el in enumerate(REE_ELEMENTS):
                if el in df.columns and el in standard:
                    val = row.get(el)
                    std_val = standard.get(el, 1)
                    
                    if pd.notna(val) and val > 0 and std_val > 0:
                        normalized = val / std_val
                        x_vals.append(i)
                        y_vals.append(normalized)
                        norm_row[el] = normalized
                        norm_data[el].append(normalized)
                    else:
                        norm_data[el].append(np.nan)
                        norm_row[el] = np.nan
                else:
                    norm_data[el].append(np.nan)
                    norm_row[el] = np.nan
            
            # Calculate ratios and anomalies
            ratios = self._calculate_ratios(norm_row, label)
            ratio_data.append(ratios)
            
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
        self.ratios = pd.DataFrame(ratio_data)

    def _calculate_ratios(self, norm_row, label):
        """Calculate REE ratios and anomalies."""
        result = {'Label': label}
        
        # Get values
        la = norm_row.get('La', np.nan)
        ce = norm_row.get('Ce', np.nan)
        pr = norm_row.get('Pr', np.nan)
        nd = norm_row.get('Nd', np.nan)
        sm = norm_row.get('Sm', np.nan)
        eu = norm_row.get('Eu', np.nan)
        gd = norm_row.get('Gd', np.nan)
        yb = norm_row.get('Yb', np.nan)
        lu = norm_row.get('Lu', np.nan)
        
        # La/Yb ratio
        if pd.notna(la) and pd.notna(yb) and yb > 0:
            result['(La/Yb)N'] = round(la / yb, 4)
        else:
            result['(La/Yb)N'] = np.nan
        
        # La/Sm ratio
        if pd.notna(la) and pd.notna(sm) and sm > 0:
            result['(La/Sm)N'] = round(la / sm, 4)
        else:
            result['(La/Sm)N'] = np.nan
        
        # Gd/Yb ratio
        if pd.notna(gd) and pd.notna(yb) and yb > 0:
            result['(Gd/Yb)N'] = round(gd / yb, 4)
        else:
            result['(Gd/Yb)N'] = np.nan
        
        # Eu anomaly (Eu/Eu*) - geometric mean method
        if pd.notna(sm) and pd.notna(gd) and sm > 0 and gd > 0 and pd.notna(eu):
            eu_star = np.sqrt(sm * gd)
            result['Eu/Eu*'] = round(eu / eu_star, 4)
        else:
            result['Eu/Eu*'] = np.nan
        
        # Ce anomaly (Ce/Ce*) - using La and Pr
        if pd.notna(la) and pd.notna(pr) and la > 0 and pr > 0 and pd.notna(ce):
            ce_star = np.sqrt(la * pr)
            result['Ce/Ce*'] = round(ce / ce_star, 4)
        else:
            result['Ce/Ce*'] = np.nan
        
        # Sum of LREE, MREE, HREE
        lree_vals = [norm_row.get(el, np.nan) for el in LREE]
        mree_vals = [norm_row.get(el, np.nan) for el in MREE]
        hree_vals = [norm_row.get(el, np.nan) for el in HREE]
        
        result['LREE'] = round(np.nansum(lree_vals), 4)
        result['MREE'] = round(np.nansum(mree_vals), 4)
        result['HREE'] = round(np.nansum(hree_vals), 4)
        result['Total REE'] = round(np.nansum(lree_vals + mree_vals + hree_vals), 4)
        
        # LREE/HREE
        if result['HREE'] > 0:
            result['LREE/HREE'] = round(result['LREE'] / result['HREE'], 4)
        else:
            result['LREE/HREE'] = np.nan
        
        return result

    def show_normalized(self):
        """Show normalized values in a table."""
        if self.normalized_data.empty:
            return
        
        viewer = TableViewer(self.normalized_data, "Normalized REE Values", self)
        viewer.show()

    def show_ratios(self):
        """Show REE ratios in a table."""
        if self.ratios.empty:
            return
        
        viewer = TableViewer(self.ratios, "REE Ratios and Anomalies", self)
        viewer.show()
