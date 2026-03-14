# -*- coding: utf-8 -*-
"""
Sm-Nd Isotope Diagram Module

Implements Sm-Nd isochron diagram with age calculation.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox

from ...core.base_widget import BasePlotWindow


class SmNdIsotope(BasePlotWindow):
    """
    Sm-Nd Isochron Diagram.
    """
    
    title = "Sm-Nd Isochron Diagram"
    reference = "Ludwig, K.R. (2003). Isoplot 3.75: A geochronological toolkit for Microsoft Excel."
    items_to_check = ['147Sm/144Nd', '143Nd/144Nd']
    
    x_name = '147Sm/144Nd'
    y_name = '143Nd/144Nd'
    x_label = r'$^{147}Sm/^{144}Nd$'
    y_label = r'$^{143}Nd/^{144}Nd$'
    lambda_sm = 6.54e-12
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
    
    def create_controls(self):
        self.legend_cb = QCheckBox("Show Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        self.control_layout.addWidget(self.legend_cb)
    
    def plot(self):
        self.axes.clear()
        self.axes.set_xlabel(self.x_label)
        self.axes.set_ylabel(self.y_label)
        
        if self.df.empty:
            self.canvas.draw()
            return
        
        x_data, y_data = [], []
        seen_labels = set()
        
        for idx, row in self.df.iterrows():
            x, y = row.get(self.x_name), row.get(self.y_name)
            if pd.isna(x) or pd.isna(y):
                continue
            
            x_data.append(x)
            y_data.append(y)
            
            label = str(row.get('Label', ''))
            plot_label = label if label and label not in seen_labels else "_nolegend_"
            if label:
                seen_labels.add(label)
            
            self.axes.scatter(x, y, marker=row.get('Marker', 'o'),
                            c=row.get('Color', 'red'), s=row.get('Size', 20),
                            alpha=row.get('Alpha', 0.7), label=plot_label)
        
        if len(x_data) >= 2:
            coeffs = np.polyfit(x_data, y_data, 1)
            x_line = np.linspace(min(x_data), max(x_data), 100)
            self.axes.plot(x_line, np.polyval(coeffs, x_line), 'k--', alpha=0.5)
            
            age_ma = np.log(coeffs[0] + 1) / self.lambda_sm / 1e6
            self.textbox.setText(f"Age = {age_ma:.1f} Ma\nInitial = {coeffs[1]:.5f}\n\n{self.reference}")
        
        if self.legend_cb.isChecked() and seen_labels:
            self.axes.legend(loc='best', fontsize='small')
        
        self.canvas.draw()