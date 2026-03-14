# -*- coding: utf-8 -*-
"""
Data Flatten Module

Utility for flattening 2D data to 1D list.
"""

import pandas as pd
from itertools import product

from PySide6.QtWidgets import QPushButton, QFileDialog

from ..core.base_widget import BasePlotWindow


class FlattenWindow(BasePlotWindow):
    """
    Data Flattening Window.
    
    Features:
    - Flatten 2D data to 1D list
    - Save flattened data
    """
    
    title = "Flatten Data"
    reference = "Flatten 2D geochemical data to 1D list."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.original_df = None
        self.result_df = None
    
    def create_controls(self):
        self.flatten_btn = QPushButton("Flatten")
        self.flatten_btn.clicked.connect(self._flatten)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._save_result)
        
        self.control_layout.addWidget(self.flatten_btn)
        self.control_layout.addWidget(self.reset_btn)
        self.control_layout.addWidget(self.save_btn)
    
    def plot(self):
        self.axes.clear()
        
        if self.df.empty:
            self.axes.text(0.5, 0.5, "No data loaded",
                          transform=self.axes.transAxes, ha='center')
        else:
            df_work = self.df.copy()
            
            if 'Label' in df_work.columns:
                df_work = df_work.set_index('Label')
            
            df_work = df_work.dropna(axis=1, how='all')
            
            exclude_cols = ['Number', 'Tag', 'Name', 'Author', 'DataType',
                           'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
            for col in exclude_cols:
                if col in df_work.columns:
                    df_work = df_work.drop(col, axis=1)
            
            df_work = df_work.apply(pd.to_numeric, errors='coerce')
            df_work = df_work.dropna(axis='columns')
            
            self.original_df = df_work.copy()
            self.result_df = df_work.copy()
            
            self.axes.text(0.5, 0.5, f"Data shape: {df_work.shape[0]} x {df_work.shape[1]}",
                          transform=self.axes.transAxes, ha='center', fontsize=12)
        
        self.axes.axis('off')
        self.canvas.draw()
        
        if self.original_df is not None:
            self.textbox.setText(f"Original shape: {self.original_df.shape}")
    
    def _flatten(self):
        if self.original_df is None:
            return
        
        self.result_df = pd.DataFrame(self.original_df.values.flatten())
        self.axes.clear()
        self.axes.text(0.5, 0.5, f"Flattened: {len(self.result_df)} values",
                      transform=self.axes.transAxes, ha='center', fontsize=12)
        self.axes.axis('off')
        self.canvas.draw()
        
        self.textbox.setText(f"Flattened: {len(self.result_df)} values")
    
    def _reset(self):
        if self.original_df is None:
            return
        
        self.result_df = self.original_df.copy()
        self.axes.clear()
        self.axes.text(0.5, 0.5, f"Data shape: {self.original_df.shape[0]} x {self.original_df.shape[1]}",
                      transform=self.axes.transAxes, ha='center', fontsize=12)
        self.axes.axis('off')
        self.canvas.draw()
        
        self.textbox.setText(f"Original shape: {self.original_df.shape}")
    
    def _save_result(self):
        if self.result_df is None:
            self.show_error("No data to save.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        
        if filepath:
            try:
                if filepath.endswith('.csv'):
                    self.result_df.to_csv(filepath, index=False)
                else:
                    self.result_df.to_excel(filepath, index=False)
                self.textbox.setText(f"Saved to: {filepath}")
            except Exception as e:
                self.show_error(str(e))