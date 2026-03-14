# -*- coding: utf-8 -*-
"""
MLP Analysis Module

Multi-Layer Perceptron neural network for classification.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QPushButton, QSpinBox, QLabel

from ...core.base_widget import BasePlotWindow
from ...ui.table_viewer import TableViewer

try:
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class MLPAnalysis(BasePlotWindow):
    """
    Multi-Layer Perceptron Classification.
    """
    
    title = "MLP Neural Network"
    reference = "Multi-Layer Perceptron for classification."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.model = None
        self.scaler = None
        self.label_encoder = None
    
    def create_controls(self):
        self.hidden_label = QLabel("Hidden Layers:")
        self.hidden_spin = QSpinBox()
        self.hidden_spin.setRange(1, 100)
        self.hidden_spin.setValue(10)
        
        self.train_btn = QPushButton("Train")
        self.train_btn.clicked.connect(self.plot)
        
        self.results_btn = QPushButton("Show Results")
        self.results_btn.clicked.connect(self._show_results)
        
        self.control_layout.addWidget(self.hidden_label)
        self.control_layout.addWidget(self.hidden_spin)
        self.control_layout.addWidget(self.train_btn)
        self.control_layout.addWidget(self.results_btn)
    
    def plot(self):
        self.axes.clear()
        self.axes.set_title("MLP Training Progress")
        
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
        
        hidden_size = self.hidden_spin.value()
        self.model = MLPClassifier(hidden_layer_sizes=(hidden_size,), max_iter=500)
        self.model.fit(X_scaled, y)
        
        if hasattr(self.model, 'loss_curve_'):
            self.axes.plot(self.model.loss_curve_)
            self.axes.set_xlabel("Iteration")
            self.axes.set_ylabel("Loss")
            self.textbox.setText(f"Final Loss: {self.model.loss_curve_[-1]:.4f}\n"
                               f"Iterations: {len(self.model.loss_curve_)}\n"
                               f"Accuracy: {self.model.score(X_scaled, y):.3f}")
        
        self.canvas.draw()
    
    def _show_results(self):
        if self.model is None:
            self.show_error("Train model first.")
            return
        
        df_slim = self.data_cleaner.slim(self.df)
        X_scaled = self.scaler.transform(df_slim.values)
        
        predictions = self.label_encoder.inverse_transform(self.model.predict(X_scaled))
        
        result_df = pd.DataFrame({
            'Sample': range(len(predictions)),
            'Prediction': predictions
        })
        TableViewer(result_df, "MLP Predictions", self).show()