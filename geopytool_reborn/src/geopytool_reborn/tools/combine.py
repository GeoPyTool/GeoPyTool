# -*- coding: utf-8 -*-
"""
Data Combine Module

Utility for combining and cleaning geochemical data.
"""

import pandas as pd

from PySide6.QtWidgets import (
    QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QTableView
)

from ..core.data_model import PandasModel
from ..core.base_widget import BasePlotWindow


class CombineWindow(BasePlotWindow):
    """
    Data Combination Window.
    
    Features:
    - Fill blanks with values
    - Remove columns/rows with blanks
    - Save modified data
    """
    
    title = "Combine Data"
    reference = "Data combination and cleaning utility."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.original_df = df.copy()
        self.result_df = df.copy()
    
    def create_controls(self):
        self.fill_btn = QPushButton("Fill Blanks with 0")
        self.fill_btn.clicked.connect(self._fill_nan)
        
        self.drop_cols_btn = QPushButton("Remove Columns with Blanks")
        self.drop_cols_btn.clicked.connect(self._drop_nan_columns)
        
        self.drop_rows_btn = QPushButton("Remove Rows with Blanks")
        self.drop_rows_btn.clicked.connect(self._drop_nan_rows)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._save_result)
        
        self.control_layout.addWidget(self.fill_btn)
        self.control_layout.addWidget(self.drop_cols_btn)
        self.control_layout.addWidget(self.drop_rows_btn)
        self.control_layout.addWidget(self.reset_btn)
        self.control_layout.addWidget(self.save_btn)
    
    def plot(self):
        self.axes.clear()
        self.axes.text(0.5, 0.5, f"Data: {len(self.result_df)} rows, {len(self.result_df.columns)} columns",
                      transform=self.axes.transAxes, ha='center', fontsize=12)
        self.axes.axis('off')
        self.canvas.draw()
        
        self.textbox.setText(f"Original: {len(self.original_df)} rows\n"
                            f"Current: {len(self.result_df)} rows, {len(self.result_df.columns)} columns")
    
    def _fill_nan(self):
        self.result_df = self.result_df.fillna(0)
        self.plot()
    
    def _drop_nan_columns(self):
        self.result_df = self.result_df.dropna(axis='columns')
        self.plot()
    
    def _drop_nan_rows(self):
        self.result_df = self.result_df.dropna(axis='index')
        self.plot()
    
    def _reset(self):
        self.result_df = self.original_df.copy()
        self.plot()
    
    def _save_result(self):
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