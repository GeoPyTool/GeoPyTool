# -*- coding: utf-8 -*-
"""
SVM Analysis Module

Support Vector Machine classification and visualization.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton

from ...core.base_widget import BasePlotWindow
from ...ui.table_viewer import TableViewer

try:
    from sklearn import svm
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from matplotlib.colors import ListedColormap
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class SVMAnalysis(BasePlotWindow):
    """
    SVM Classification Analysis.
    
    Features:
    - Multiple kernel options
    - Decision boundary visualization
    - Classification probability output
    """
    
    title = "SVM Classification"
    reference = "Support Vector Machine classification for geochemical data."
    items_to_check = []
    
    kernel_list = ['linear', 'rbf', 'poly', 'sigmoid']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.test_data = None
    
    def create_controls(self):
        self.kernel_label = QLabel("Kernel:")
        self.kernel_combo = QComboBox()
        self.kernel_combo.addItems(self.kernel_list)
        self.kernel_combo.currentIndexChanged.connect(self.plot)
        
        self.load_btn = QPushButton("Load Test Data")
        self.load_btn.clicked.connect(self._load_test_data)
        
        self.predict_btn = QPushButton("Predict")
        self.predict_btn.clicked.connect(self._predict)
        
        self.control_layout.addWidget(self.kernel_label)
        self.control_layout.addWidget(self.kernel_combo)
        self.control_layout.addWidget(self.load_btn)
        self.control_layout.addWidget(self.predict_btn)
    
    def plot(self):
        self.axes.clear()
        self.axes.set_title("SVM Classification")
        
        if not SKLEARN_AVAILABLE:
            self.axes.text(0.5, 0.5, "scikit-learn not available", 
                          transform=self.axes.transAxes, ha='center')
            self.canvas.draw()
            return
        
        if self.df.empty:
            self.canvas.draw()
            return
        
        df_slim = self.data_cleaner.slim(self.df)
        if df_slim.empty:
            self.canvas.draw()
            return
        
        if 'Label' not in self.df.columns:
            self.axes.text(0.5, 0.5, "Label column required for classification",
                          transform=self.axes.transAxes, ha='center')
            self.canvas.draw()
            return
        
        X = df_slim.values
        y_labels = self.df['Label'].values[:len(X)]
        
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y_labels)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        if X_scaled.shape[1] >= 2:
            self._plot_2d(X_scaled, y)
        else:
            self.axes.text(0.5, 0.5, "Need at least 2 features for visualization",
                          transform=self.axes.transAxes, ha='center')
        
        self.canvas.draw()
    
    def _plot_2d(self, X, y):
        kernel = self.kernel_combo.currentText()
        self.model = svm.SVC(C=1.0, kernel=kernel, probability=True)
        self.model.fit(X[:, :2], y)
        
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                            np.linspace(y_min, y_max, 100))
        
        Z = self.model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        cmap = ListedColormap(colors[:len(np.unique(y))])
        
        self.axes.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)
        
        seen_labels = set()
        for i in range(len(X)):
            label = y_labels[i] if i < len(y_labels) else ''
            plot_label = label if label and label not in seen_labels else "_nolegend_"
            if label:
                seen_labels.add(label)
            
            self.axes.scatter(X[i, 0], X[i, 1], 
                            c=colors[y[i] % len(colors)],
                            s=self.df.iloc[i].get('Size', 20),
                            alpha=self.df.iloc[i].get('Alpha', 0.7),
                            label=plot_label)
        
        self.axes.legend(loc='best', fontsize='small')
        self.axes.set_xlabel("PC1")
        self.axes.set_ylabel("PC2")
    
    def _load_test_data(self):
        from PySide6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Load Test Data", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        
        if filepath:
            try:
                if filepath.endswith('.csv'):
                    self.test_data = pd.read_csv(filepath)
                else:
                    self.test_data = pd.read_excel(filepath)
                self.textbox.setText(f"Loaded test data: {len(self.test_data)} samples")
            except Exception as e:
                self.show_error(str(e))
    
    def _predict(self):
        if self.model is None:
            self.show_error("Train model first by plotting.")
            return
        
        if self.test_data is None:
            self.show_error("Load test data first.")
            return
        
        df_slim = self.data_cleaner.slim(self.test_data)
        X_test = self.scaler.transform(df_slim.values[:, :2])
        
        predictions = self.label_encoder.inverse_transform(self.model.predict(X_test))
        probabilities = self.model.predict_proba(X_test)
        
        result_df = pd.DataFrame({
            'Label': self.test_data['Label'].values[:len(predictions)] if 'Label' in self.test_data.columns else range(len(predictions)),
            'Prediction': predictions
        })
        
        for i, cls in enumerate(self.label_encoder.classes_):
            result_df[f'Prob_{cls}'] = probabilities[:, i]
        
        TableViewer(result_df, "SVM Predictions", self).show()