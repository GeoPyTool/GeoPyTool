# -*- coding: utf-8 -*-
"""
Custom widgets module - Specialized Qt widgets for GeoPyTool.
"""

import pandas as pd
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt


class FileDropTableView(QTableView):
    """
    A QTableView that accepts file drops for loading data.
    
    Supported formats: CSV, Excel (xlsx, xls)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(
            QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked
        )
        
        self.last_file_path = ''

    def dragEnterEvent(self, event):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                filepath = url.toLocalFile()
                if self._is_supported_file(filepath):
                    event.accept()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        """Handle drag move events."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle drop events - load the file."""
        urls = event.mimeData().urls()
        for url in urls:
            filepath = url.toLocalFile()
            if self._is_supported_file(filepath):
                self._load_file(filepath)
                break

    def _is_supported_file(self, filepath):
        """Check if file is a supported format."""
        lower = filepath.lower()
        return lower.endswith('.csv') or lower.endswith('.xlsx') or lower.endswith('.xls')

    def _load_file(self, filepath):
        """Load data from file."""
        try:
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath, engine='python')
            else:
                df = pd.read_excel(filepath, engine='openpyxl')
            
            self.last_file_path = filepath
            
            # Notify parent if it has a method to receive data
            parent = self.parent()
            if parent and hasattr(parent, 'on_data_loaded'):
                parent.on_data_loaded(df, filepath)
            
        except Exception as e:
            print(f"Error loading file: {e}")

    def keyPressEvent(self, event):
        """Override to disable default key handling."""
        pass
