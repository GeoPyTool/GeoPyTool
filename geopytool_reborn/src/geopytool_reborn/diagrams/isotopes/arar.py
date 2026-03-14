# -*- coding: utf-8 -*-
"""
Ar-Ar Isotope Diagram Module

Implements Ar-Ar isochron diagram with age calculation.
"""

import numpy as np
import pandas as pd
from statistics import mean

from PySide6.QtWidgets import QCheckBox

from ...core.base_widget import BasePlotWindow


class ArArIsotope(BasePlotWindow):
    """
    Ar-Ar Isochron Diagram.
    
    Features:
    - 39Ar vs 40Ar plotting
    - Age calculation from Ar ratios
    - MSWD calculation
    """
    
    title = "Ar-Ar Isochron Diagram"
    reference = "Ludwig, K.R. (2003). Isoplot 3.75: A geochronological toolkit for Microsoft Excel."
    items_to_check = ['39Ar', '40Ar']
    
    x_name = '39Ar'
    y_name = '40Ar'
    x_label = r'$^{39}Ar$'
    y_label = r'$^{40}Ar$'
    
    lambda_k = 0.585e-10
    lambda_ar = 4.72e-10
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.age_result = None
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
            ages = []
            for x, y in zip(x_data, y_data):
                if x > 0:
                    age = 1 / self.lambda_k * np.log(y / x * self.lambda_k / self.lambda_ar + 1)
                    ages.append(age)
            
            if ages:
                age_ma = mean(ages) / 1e6
                self.age_result = age_ma
                
                n = len(x_data)
                f = n - 2
                mswd = 1 + 2 * np.sqrt(2/f) if f > 0 else 1
                mswd_err = np.sqrt(2/f) if f > 0 else 0
                self.mswd = mswd
                
                info_text = (f"Age = {age_ma:.2f} Ma\n"
                           f"MSWD = {mswd:.2f} ± {2*mswd_err:.2f}")
                self.textbox.setText(info_text + "\n\n" + self.reference)
        
        if self.legend_cb.isChecked() and seen_labels:
            self.axes.legend(loc='best', fontsize='small')
        
        self.canvas.draw()