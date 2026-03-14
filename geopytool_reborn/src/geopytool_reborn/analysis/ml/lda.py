# -*- coding: utf-8 -*-
"""
LDA Analysis Module

Linear Discriminant Analysis for classification and dimensionality reduction.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QPushButton

from ...core.base_widget import BasePlotWindow
from ...ui.table_viewer import TableViewer

try:
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from matplotlib.colors import ListedColormap
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class LDAAnalysis(BasePlotWindow):
    """
    Linear Discriminant Analysis.
    """
    
    title = "LDA Analysis"
    reference = "Linear Discriminant Analysis for classification."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.model = None
        self.scaler = None
        self.label_encoder = None
    
    def create_controls(self):
        self.predict_btn = QPushButton("Show Results")
        self.predict_btn.clicked.connect(self._show_results)
        self.control_layout.addWidget(self.predict_btn)
    
    def plot(self):
        self.axes.clear()
        self.axes.set_title("LDA Analysis")
        
        if not SKLEARN_AVAILABLE:
            self.axes.text(0.5, 0.5, "scikit-learn not available",
                          transform=self.axes.transAxes, ha='center')
            self.canvas.draw()
            return
        
        if self.df.empty or 'Label' not in self.df.columns:
            self.canvas.draw()
            return
        
        df_slim = self.data_cleaner.slim(self.df)
        if df_slim.empty:
            self.canvas.draw()
            return
        
        X = df_slim.values
        y_labels = self.df['Label'].values[:len(X)]
        
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y_labels)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        n_components = min(2, len(np.unique(y)) - 1, X.shape[1])
        self.model = LinearDiscriminantAnalysis(n_components=n_components)
        X_lda = self.model.fit_transform(X_scaled, y)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        seen_labels = set()
        for i in range(len(X_lda)):
            label = y_labels[i]
            plot_label = label if label and label not in seen_labels else "_nolegend_"
            if label:
                seen_labels.add(label)
            
            x = X_lda[i, 0] if X_lda.shape[1] >= 1 else 0
            y_val = X_lda[i, 1] if X_lda.shape[1] >= 2 else 0
            
            self.axes.scatter(x, y_val,
                            c=colors[y[i] % len(colors)],
                            s=self.df.iloc[i].get('Size', 20),
                            alpha=self.df.iloc[i].get('Alpha', 0.7),
                            label=plot_label)
        
        self.axes.legend(loc='best', fontsize='small')
        self.axes.set_xlabel("LD1")
        self.axes.set_ylabel("LD2")
        self.canvas.draw()
    
    def _show_results(self):
        if self.model is None:
            self.show_error("Run analysis first.")
            return
        
        result_df = pd.DataFrame({
            'Class': self.label_encoder.classes_,
            'Coefficient': self.model.coef_.flatten()[:len(self.label_encoder.classes_)]
        })
        TableViewer(result_df, "LDA Results", self).show()