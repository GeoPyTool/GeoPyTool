# -*- coding: utf-8 -*-
"""
TAS (Total Alkali-Silica) Diagram

Classification diagram for volcanic and plutonic rocks based on 
SiO2 vs Na2O + K2O contents.

Reference: 
- Le Maitre, R.W. et al., 2002. Igneous Rocks: A Classification and 
  Glossary of Terms, Cambridge University Press.
- Wilson, M., 1989. Igneous Petrogenesis.
"""

import numpy as np
import pandas as pd
from matplotlib import patches, path

from PySide6.QtWidgets import (
    QCheckBox, QSlider, QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..ui.table_viewer import TableViewer
from ..resources.standards import TAS_FIELDS, TAS_LABELS_VOLCANIC, TAS_LABELS_PLUTONIC, TAS_LABEL_POSITIONS


class TAS(BasePlotWindow):
    """
    TAS (Total Alkali-Silica) diagram for volcanic/plutonic rock classification.
    
    Required columns: SiO2, Na2O, K2O
    """
    
    title = "TAS Diagram (Total Alkali-Silica)"
    reference = ("Reference: Le Maitre, R.W. et al., 2002. Igneous Rocks: "
                 "A Classification and Glossary of Terms. Cambridge University Press.")
    items_to_check = ['SiO2', 'K2O', 'Na2O']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.type_list = []  # Classification results
        super().__init__(df, parent)
        
        # Initialize field paths for classification
        self._init_field_paths()
        
        # Initial plot
        if not df.empty:
            self.plot()
    
    def _init_field_paths(self):
        """Initialize matplotlib paths for each field for point-in-polygon tests."""
        self.field_paths = {}
        for name, vertices in TAS_FIELDS.items():
            closed_vertices = vertices + [vertices[0]]  # Close the polygon
            self.field_paths[name] = path.Path(closed_vertices)

    def create_controls(self):
        """Add TAS-specific controls."""
        # Rock type selector
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Volcanic", "Plutonic"])
        self.type_combo.currentIndexChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        self.detail_cb = QCheckBox("Field Labels")
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.plot)
        
        self.irvine_cb = QCheckBox("Irvine Line")
        self.irvine_cb.setChecked(True)
        self.irvine_cb.stateChanged.connect(self.plot)
        
        self.show_index_cb = QCheckBox("Show Index")
        self.show_index_cb.setChecked(False)
        self.show_index_cb.stateChanged.connect(self.plot)
        
        # Classification result button
        self.result_button = QPushButton("Classification")
        self.result_button.clicked.connect(self.show_classification)
        
        # Add to layout
        self.control_layout.addWidget(self.type_label)
        self.control_layout.addWidget(self.type_combo)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.detail_cb)
        self.control_layout.addWidget(self.irvine_cb)
        self.control_layout.addWidget(self.show_index_cb)
        self.control_layout.addWidget(self.result_button)

    def plot(self):
        """Draw the TAS diagram."""
        self.axes.clear()
        
        # Setup axes
        self.axes.set_xlabel(r'$SiO_2$ (wt%)')
        self.axes.set_ylabel(r'$Na_2O + K_2O$ (wt%)')
        self.axes.set_xlim(35, 90)
        self.axes.set_ylim(0, 18)
        
        # Get labels based on rock type
        is_volcanic = self.type_combo.currentText() == "Volcanic"
        labels = TAS_LABELS_VOLCANIC if is_volcanic else TAS_LABELS_PLUTONIC
        
        # Draw field boundaries
        for name, vertices in TAS_FIELDS.items():
            closed_vertices = vertices + [vertices[0]]
            x = [v[0] for v in closed_vertices]
            y = [v[1] for v in closed_vertices]
            self.axes.plot(x, y, color='gray', linewidth=0.5, alpha=0.7)
            
            # Add field labels
            if self.detail_cb.isChecked() and name in TAS_LABEL_POSITIONS:
                pos = TAS_LABEL_POSITIONS[name]
                label = labels.get(name, name)
                self.axes.text(pos[0], pos[1], label, fontsize=7, 
                              ha='center', va='center', color='gray')
        
        # Draw Irvine & Baragar alkaline-subalkaline boundary
        if self.irvine_cb.isChecked():
            self._draw_irvine_line()
        
        # Plot data
        if not self._df.empty:
            self._plot_data()
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels_list = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(loc='upper left', fontsize=8)
        
        self.canvas.draw()

    def _draw_irvine_line(self):
        """Draw the Irvine & Baragar (1971) alkaline-subalkaline boundary."""
        # Polynomial coefficients for the boundary
        def irvine(y):
            a, b, c, d, e, f, g = 39.0, 3.9492, -2.1111, 0.86096, -0.15188, 0.012030, -3.3539e-4
            return (a + b*y + c*y**2 + d*y**3 + e*y**4 + f*y**5 + g*y**6)
        
        y_vals = np.arange(0, 10.2, 0.1)
        x_vals = irvine(y_vals)
        
        self.axes.plot(x_vals, y_vals, 'b:', linewidth=1, alpha=0.7, 
                      label='Irvine & Baragar 1971')

    def _plot_data(self):
        """Plot the data points."""
        df = self._df
        
        # Check required columns
        has_sio2 = 'SiO2' in df.columns
        has_na2o = 'Na2O' in df.columns
        has_k2o = 'K2O' in df.columns
        
        if not (has_sio2 and has_na2o and has_k2o):
            self.axes.text(0.5, 0.5, "Missing SiO2, Na2O, or K2O columns",
                          transform=self.axes.transAxes, ha='center', color='red')
            return
        
        # Calculate total alkali
        df = df.copy()
        df['TotalAlkali'] = df['Na2O'] + df['K2O']
        
        # Classify and store results
        self.type_list = []
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            try:
                sio2 = row['SiO2']
                total_alkali = row['TotalAlkali']
                
                if pd.isna(sio2) or pd.isna(total_alkali):
                    self.type_list.append('')
                    continue
                
                # Classify the point
                rock_type = self._classify_point(sio2, total_alkali)
                self.type_list.append(rock_type)
                
                # Plot
                label = str(row.get('Label', ''))
                if label and label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                self.axes.scatter(
                    sio2, total_alkali,
                    marker=row.get('Marker', 'o'),
                    c=row.get('Color', 'red'),
                    s=row.get('Size', 40),
                    alpha=row.get('Alpha', 0.7),
                    label=plot_label,
                    edgecolors='none'
                )
                
                # Show index if requested
                if self.show_index_cb.isChecked():
                    self.axes.annotate(str(idx), (sio2, total_alkali), 
                                      fontsize=6, alpha=0.7)
                
            except Exception:
                self.type_list.append('')

    def _classify_point(self, sio2, total_alkali):
        """Classify a point based on its position in the TAS diagram."""
        point = (sio2, total_alkali)
        
        is_volcanic = self.type_combo.currentText() == "Volcanic"
        labels = TAS_LABELS_VOLCANIC if is_volcanic else TAS_LABELS_PLUTONIC
        
        for name, field_path in self.field_paths.items():
            if field_path.contains_point(point):
                return labels.get(name, name)
        
        return "Unclassified"

    def show_classification(self):
        """Show classification results in a table."""
        if self._df.empty:
            return
        
        # Build results DataFrame
        results = []
        df = self._df
        
        for i, row in df.iterrows():
            result = {
                'Label': row.get('Label', ''),
                'SiO2': row.get('SiO2', ''),
                'Na2O': row.get('Na2O', ''),
                'K2O': row.get('K2O', ''),
                'Total Alkali': row.get('Na2O', 0) + row.get('K2O', 0),
                'Classification': self.type_list[i] if i < len(self.type_list) else ''
            }
            results.append(result)
        
        result_df = pd.DataFrame(results)
        
        viewer = TableViewer(result_df, "TAS Classification Results", self)
        viewer.show()
