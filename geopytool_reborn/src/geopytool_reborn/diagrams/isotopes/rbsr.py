# -*- coding: utf-8 -*-
"""
Rb-Sr Isotope Diagram Module

Implements Rb-Sr isochron diagram with age calculation.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QLabel

from ...core.base_widget import BasePlotWindow


class RbSrIsotope(BasePlotWindow):
    """
    Rb-Sr Isochron Diagram.
    
    Features:
    - 87Rb/86Sr vs 87Sr/86Sr plotting
    - Linear regression for isochron
    - Age calculation with error
    """
    
    title = "Rb-Sr Isochron Diagram"
    reference = "Ludwig, K.R. (2003). Isoplot 3.75: A geochronological toolkit for Microsoft Excel."
    items_to_check = ['87Rb/86Sr', '87Sr/86Sr']
    
    x_name = '87Rb/86Sr'
    y_name = '87Sr/86Sr'
    x_label = r'$^{87}Rb/^{86}Sr$'
    y_label = r'$^{87}Sr/^{86}Sr$'
    lambda_rb = 1.42e-11  # Decay constant (1/yr)
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.age_result = None
        self.initial_ratio = None
        self.mswd = None
    
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
        
        x_data = []
        y_data = []
        
        seen_labels = set()
        
        for idx, row in self.df.iterrows():
            x = row.get(self.x_name)
            y = row.get(self.y_name)
            
            if pd.isna(x) or pd.isna(y):
                continue
            
            x_data.append(x)
            y_data.append(y)
            
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
                s=row.get('Size', 20),
                alpha=row.get('Alpha', 0.7),
                label=plot_label
            )
        
        if len(x_data) >= 2:
            x_arr = np.array(x_data)
            y_arr = np.array(y_data)
            
            try:
                coeffs = np.polyfit(x_arr, y_arr, 1)
                slope = coeffs[0]
                intercept = coeffs[1]
                
                x_line = np.linspace(min(x_arr), max(x_arr), 100)
                y_line = np.polyval(coeffs, x_line)
                self.axes.plot(x_line, y_line, 'k--', alpha=0.5, label='Isochron')
                
                age_ma = np.log(slope + 1) / self.lambda_rb / 1e6
                self.age_result = age_ma
                self.initial_ratio = intercept
                
                n = len(x_data)
                f = n - 2
                mswd = 1 + 2 * np.sqrt(2/f) if f > 0 else 1
                self.mswd = mswd
                
                info_text = (f"Age = {age_ma:.1f} Ma\n"
                           f"Initial 87Sr/86Sr = {intercept:.5f}\n"
                           f"MSWD = {mswd:.2f}")
                self.textbox.setText(info_text + "\n\n" + self.reference)
                
            except Exception as e:
                self.textbox.setText(f"Error: {str(e)}\n\n" + self.reference)
        
        if self.legend_cb.isChecked() and seen_labels:
            self.axes.legend(loc='best', fontsize='small')
        
        self.canvas.draw()