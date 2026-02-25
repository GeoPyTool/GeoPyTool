# -*- coding: utf-8 -*-
"""
Statistics Module

Basic statistical analysis and visualization for geochemical data.
"""

import numpy as np
import pandas as pd
from scipy import stats

from PySide6.QtWidgets import (
    QCheckBox, QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..ui.table_viewer import TableViewer


class Statistics(BasePlotWindow):
    """
    Statistical analysis and visualization.
    
    Features:
    - Descriptive statistics
    - Histogram and box plots
    - Normality tests
    - Correlation matrix
    """
    
    title = "Statistical Analysis"
    reference = "Descriptive statistics and distribution analysis."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.stats_df = pd.DataFrame()
        super().__init__(df, parent)
        
        if not df.empty:
            self._calculate_stats()
            self.plot()
    
    def create_controls(self):
        """Add Statistics-specific controls."""
        # Plot type
        self.plot_type_label = QLabel("Plot:")
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Histogram", "Box Plot", "Correlation"])
        self.plot_type_combo.currentIndexChanged.connect(self.plot)
        
        # Element selector
        self.element_label = QLabel("Element:")
        self.element_combo = QComboBox()
        self.element_combo.currentIndexChanged.connect(self.plot)
        
        # Results button
        self.stats_button = QPushButton("Statistics Table")
        self.stats_button.clicked.connect(self.show_stats)
        
        # Add to layout
        self.control_layout.addWidget(self.plot_type_label)
        self.control_layout.addWidget(self.plot_type_combo)
        self.control_layout.addWidget(self.element_label)
        self.control_layout.addWidget(self.element_combo)
        self.control_layout.addWidget(self.stats_button)
        
        # Populate element combo
        self._update_element_combo()

    def _update_element_combo(self):
        """Update element combo with numeric columns."""
        self.element_combo.clear()
        if self._df.empty:
            return
        
        df_slim = self.data_cleaner.slim(self._df.copy())
        self.element_combo.addItems(df_slim.columns.tolist())

    def _calculate_stats(self):
        """Calculate descriptive statistics."""
        if self._df.empty:
            return
        
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty:
            return
        
        stats_list = []
        for col in df_slim.columns:
            data = df_slim[col].dropna()
            if len(data) == 0:
                continue
            
            stat_row = {
                'Element': col,
                'Count': len(data),
                'Mean': round(data.mean(), 4),
                'Std': round(data.std(), 4),
                'Min': round(data.min(), 4),
                'Q1': round(data.quantile(0.25), 4),
                'Median': round(data.median(), 4),
                'Q3': round(data.quantile(0.75), 4),
                'Max': round(data.max(), 4),
                'Skewness': round(data.skew(), 4),
                'Kurtosis': round(data.kurtosis(), 4),
            }
            
            # Normality test (Shapiro-Wilk)
            if len(data) >= 3 and len(data) <= 5000:
                try:
                    _, p_value = stats.shapiro(data)
                    stat_row['Shapiro-Wilk p'] = round(p_value, 4)
                except:
                    stat_row['Shapiro-Wilk p'] = np.nan
            else:
                stat_row['Shapiro-Wilk p'] = np.nan
            
            stats_list.append(stat_row)
        
        self.stats_df = pd.DataFrame(stats_list)

    def plot(self):
        """Draw the statistical plot."""
        self.axes.clear()
        
        if self._df.empty:
            return
        
        plot_type = self.plot_type_combo.currentText()
        
        if plot_type == "Histogram":
            self._plot_histogram()
        elif plot_type == "Box Plot":
            self._plot_boxplot()
        elif plot_type == "Correlation":
            self._plot_correlation()
        
        self.canvas.draw()

    def _plot_histogram(self):
        """Plot histogram of selected element."""
        element = self.element_combo.currentText()
        if not element:
            return
        
        df_slim = self.data_cleaner.slim(self._df.copy())
        if element not in df_slim.columns:
            return
        
        data = df_slim[element].dropna()
        if len(data) == 0:
            return
        
        self.axes.hist(data, bins='auto', edgecolor='black', alpha=0.7)
        self.axes.set_xlabel(element)
        self.axes.set_ylabel('Frequency')
        self.axes.set_title(f'Histogram of {element}')
        
        # Add statistics annotations
        mean_val = data.mean()
        median_val = data.median()
        self.axes.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        self.axes.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.2f}')
        self.axes.legend(fontsize=8)

    def _plot_boxplot(self):
        """Plot box plots for all numeric columns."""
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty:
            return
        
        # Standardize for comparable box plots
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        data_scaled = pd.DataFrame(
            scaler.fit_transform(df_slim),
            columns=df_slim.columns
        )
        
        data_scaled.boxplot(ax=self.axes)
        self.axes.set_ylabel('Standardized Value')
        self.axes.set_title('Box Plot (Standardized)')
        self.axes.tick_params(axis='x', rotation=45)

    def _plot_correlation(self):
        """Plot correlation matrix heatmap."""
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty:
            return
        
        corr_matrix = df_slim.corr()
        
        im = self.axes.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
        
        # Labels
        self.axes.set_xticks(range(len(corr_matrix.columns)))
        self.axes.set_yticks(range(len(corr_matrix.columns)))
        self.axes.set_xticklabels(corr_matrix.columns, fontsize=7, rotation=45, ha='right')
        self.axes.set_yticklabels(corr_matrix.columns, fontsize=7)
        
        # Colorbar
        self.fig.colorbar(im, ax=self.axes, shrink=0.8)
        
        self.axes.set_title('Correlation Matrix')

    def show_stats(self):
        """Show statistics table."""
        if self.stats_df.empty:
            self._calculate_stats()
        
        if not self.stats_df.empty:
            viewer = TableViewer(self.stats_df, "Descriptive Statistics", self)
            viewer.show()
