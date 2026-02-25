# -*- coding: utf-8 -*-
"""
Data model module - Pandas model for Qt table views and data cleaning utilities.
"""

import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


class PandasModel(QAbstractTableModel):
    """
    A Qt model for displaying pandas DataFrames in QTableView.
    
    Supports:
    - Display of DataFrame contents
    - Editing of cells
    - Sorting by columns
    """

    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df
        self._changed = False

    @property
    def dataframe(self):
        """Get the underlying DataFrame."""
        return self._df

    @dataframe.setter
    def dataframe(self, df):
        """Set a new DataFrame."""
        self.beginResetModel()
        self._df = df
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except IndexError:
                return None
        elif orientation == Qt.Vertical:
            try:
                return str(self._df.index.tolist()[section])
            except IndexError:
                return None
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._df.iloc[index.row(), index.column()]
            return str(value) if pd.notna(value) else ""
        
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        
        if role == Qt.EditRole:
            row = self._df.index[index.row()]
            col = self._df.columns[index.column()]
            
            # Try to convert to appropriate type
            dtype = self._df[col].dtype
            if dtype != object:
                try:
                    value = None if value == '' else dtype.type(value)
                except (ValueError, TypeError):
                    pass
            
            self._df.at[row, col] = value
            self._changed = True
            self.dataChanged.emit(index, index, [role])
            return True
        
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def rowCount(self, parent=QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        """Sort by column."""
        if column < 0 or column >= len(self._df.columns):
            return
        
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        
        try:
            self._df.sort_values(
                colname, 
                ascending=(order == Qt.AscendingOrder), 
                inplace=True
            )
            self._df.reset_index(inplace=True, drop=True)
        except Exception:
            pass
        
        self.layoutChanged.emit()


class DataCleaner:
    """
    Utility class for cleaning and preparing geochemical data.
    
    Handles:
    - Column name normalization
    - Removal of non-numeric columns (except styling columns)
    - Handling of standard rows
    - Missing value handling
    """
    
    # Columns that should be preserved even if non-numeric
    STYLE_COLUMNS = ['Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width', 'Label']
    
    # Characters to strip from column names
    CLEAN_CHARS = ['质量', '分数', '百分比', ' ', 'ppm', 'ma', 'wt', '%', 
                   '(', ')', '（', '）', '[', ']', '【', '】']
    
    # Columns to exclude when slimming data
    EXCLUDE_COLUMNS = ['Number', 'Tag', 'Type', 'Index', 'Name', 'Author', 
                       'DataType', 'Marker', 'Color', 'Size', 'Alpha', 
                       'Style', 'Width']

    def __init__(self, items_to_check=None):
        """
        Initialize the data cleaner.
        
        Args:
            items_to_check: List of column names that should be preserved
        """
        self.items_to_check = items_to_check or []
        self.standard = None

    def clean(self, df, preserve_columns=None):
        """
        Clean a DataFrame for geochemical analysis.
        
        Args:
            df: Input DataFrame
            preserve_columns: Additional columns to preserve
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        raw = df.copy()
        preserve = set(self.STYLE_COLUMNS + self.items_to_check)
        if preserve_columns:
            preserve.update(preserve_columns)
        
        # Clean column names
        for char in self.CLEAN_CHARS:
            raw = raw.rename(columns=lambda x: x.replace(char, ''))
        
        # Remove non-numeric columns (except preserved ones)
        cols_to_drop = []
        for col in raw.columns:
            if col in preserve:
                continue
            if raw[col].dtype not in [float, int, 'float64', 'int64']:
                cols_to_drop.append(col)
        
        raw = raw.drop(columns=cols_to_drop, errors='ignore')
        
        # Remove empty-named columns
        raw = raw.loc[:, raw.columns != '']
        
        # Remove all-NaN columns
        raw = raw.dropna(axis=1, how='all')
        
        # Extract standard rows if present
        if 'Label' in raw.columns:
            standard_mask = raw['Label'].astype(str).str.contains('tandard', na=False)
            if standard_mask.any():
                self.standard = raw.loc[standard_mask].iloc[0]
                raw = raw.loc[~standard_mask]
        
        raw = raw.reset_index(drop=True)
        
        return raw

    def ensure_style_columns(self, df):
        """
        Ensure DataFrame has all required styling columns with defaults.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with style columns
        """
        defaults = {
            'Marker': 'o',
            'Color': 'red',
            'Size': 20,
            'Alpha': 0.7,
            'Style': '-',
            'Width': 1,
            'Label': ''
        }
        
        for col, default in defaults.items():
            if col not in df.columns:
                df[col] = default
        
        return df

    def slim(self, df):
        """
        Slim down a DataFrame to numeric data only, suitable for analysis.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Slimmed DataFrame with only numeric columns
        """
        if df.empty:
            return df
        
        result = df.copy()
        
        # Set Label as index if present
        if 'Label' in result.columns:
            result = result.set_index('Label')
        
        # Drop all-NaN columns
        result = result.dropna(axis=1, how='all')
        
        # Drop excluded columns
        for col in self.EXCLUDE_COLUMNS:
            if col in result.columns:
                result = result.drop(columns=[col])
        
        # Convert to numeric
        result = result.apply(pd.to_numeric, errors='coerce')
        
        # Drop rows with any NaN
        result = result.dropna(axis='rows')
        
        return result

    def check_columns(self, df, required_columns):
        """
        Check if DataFrame contains required columns.
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
            
        Returns:
            tuple: (bool success, list of missing columns)
        """
        cols = df.columns.tolist()
        missing = [c for c in required_columns if c not in cols]
        return len(missing) == 0, missing
