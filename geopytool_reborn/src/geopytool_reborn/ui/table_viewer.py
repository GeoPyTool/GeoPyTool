# -*- coding: utf-8 -*-
"""
Table viewer module - Table view dialogs for displaying data and results.
"""

import pandas as pd
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableView, QFileDialog, QMessageBox,
    QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt

from ..core.data_model import PandasModel


class CustomTableView(QTableView):
    """
    Custom QTableView with sorting enabled and improved styling.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(
            QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked
        )

    def keyPressEvent(self, event):
        """Override to disable default key handling."""
        pass


class TableViewer(QMainWindow):
    """
    A window for viewing and saving DataFrame data.
    
    Features:
    - Display DataFrame in sortable table
    - Save to Excel or CSV
    - Optional pie/bar chart visualization
    """

    def __init__(self, df=pd.DataFrame(), title='Data Viewer', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setAcceptDrops(True)
        
        self.df = df
        self.model = PandasModel(df)
        
        self._create_ui()

    def _create_ui(self):
        """Create the user interface."""
        self.resize(900, 600)
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton('&Save Data')
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Table view
        self.table_view = CustomTableView()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        # Status
        self.status_label = QLabel(f"Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
        layout.addWidget(self.status_label)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def save_data(self):
        """Save the DataFrame to file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save Data', '',
            'Excel Files (*.xlsx);;CSV Files (*.csv)'
        )
        
        if not filename:
            return
        
        try:
            df_to_save = self.model._df
            
            # Set Label as index if present
            if 'Label' in df_to_save.columns:
                df_to_save = df_to_save.set_index('Label')
            
            if filename.endswith('.csv'):
                df_to_save.to_csv(filename, encoding='utf-8')
            else:
                df_to_save.to_excel(filename)
            
            QMessageBox.information(self, "Success", f"Data saved to {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def update_data(self, df):
        """Update the displayed data."""
        self.df = df
        self.model = PandasModel(df)
        self.table_view.setModel(self.model)
        self.status_label.setText(f"Rows: {len(df)}, Columns: {len(df.columns)}")
