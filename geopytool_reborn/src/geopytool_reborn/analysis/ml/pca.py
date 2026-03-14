# -*- coding: utf-8 -*-
"""
PCA Analysis Module

Principal Component Analysis for geochemical data.
"""

import numpy as np
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QLabel, QSlider, QPushButton

from ...core.base_widget import BasePlotWindow
from ...ui.table_viewer import TableViewer

try:
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from matplotlib.colors import ListedColormap
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class PCAAnalysis(BasePlotWindow):
    """
    PCA Analysis Window.
    
    Features:
    - Principal component analysis
    - 2D/3D score plots
    - Component selection via sliders
    - Loadings display
    """
    
    title = "Principal Component Analysis"
    reference = "Jolliffe, I.T. (2002). Principal Component Analysis."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.pca = None
        self.scaler = None
        self.scores = None
        self.n_components = 0
        self.x_component = 0
        self.y_component = 1
    
    def create_controls(self):
        self.x_label = QLabel("PC1")
        self.x_slider = QSlider()
        self.x_slider.setOrientation(1)
        self.x_slider.setRange(0, 10)
        self.x_slider.setValue(0)
        self.x_slider.valueChanged.connect(self._on_slider_change)
        
        self.y_label = QLabel("PC2")
        self.y_slider = QSlider()
        self.y_slider.setOrientation(1)
        self.y_slider.setRange(0, 10)
        self.y_slider.setValue(1)
        self.y_slider.valueChanged.connect(self._on_slider_change)
        
        self.show_labels_cb = QCheckBox("Show Labels")
        self.show_labels_cb.setChecked(False)
        self.show_labels_cb.stateChanged.connect(self.plot)
        
        self.result_btn = QPushButton("Show Result")
        self.result_btn.clicked.connect(self._show_result)
        
        self.control_layout.addWidget(self.x_label)
        self.control_layout.addWidget(self.x_slider)
        self.control_layout.addWidget(self.y_label)
        self.control_layout.addWidget(self.y_slider)
        self.control_layout.addWidget(self.show_labels_cb)
        self.control_layout.addWidget(self.result_btn)
    
    def _on_slider_change(self):
        self.x_component = self.x_slider.value()
        self.y_component = self.y_slider.value()
        self.x_label.setText(f"PC{self.x_component + 1}")
        self.y_label.setText(f"PC{self.y_component + 1}")
        self.plot()
    
    def plot(self):
        self.axes.clear()
        self.axes.set_title("PCA Score Plot")
        
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
        
        X = df_slim.values
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        n_comp = min(X_scaled.shape[0], X_scaled.shape[1])
        self.pca = PCA(n_components=n_comp)
        self.scores = self.pca.fit_transform(X_scaled)
        self.n_components = self.pca.n_components_
        
        self.x_slider.setRange(0, self.n_components - 1)
        self.y_slider.setRange(0, self.n_components - 1)
        
        pc_x = min(self.x_component, self.n_components - 1)
        pc_y = min(self.y_component, self.n_components - 1)
        
        evr = self.pca.explained_variance_ratio_
        x_var = evr[pc_x] * 100 if pc_x < len(evr) else 0
        y_var = evr[pc_y] * 100 if pc_y < len(evr) else 0
        
        self.axes.set_xlabel(f"PC{pc_x + 1} ({x_var:.1f}%)")
        self.axes.set_ylabel(f"PC{pc_y + 1} ({y_var:.1f}%)")
        
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        if 'Label' in self.df.columns:
            labels = self.df['Label'].values[:len(self.scores)]
            unique_labels = list(dict.fromkeys(labels))
            label_colors = {lbl: colors[i % len(colors)] for i, lbl in enumerate(unique_labels)}
            
            seen = set()
            for i, (score, label) in enumerate(zip(self.scores, labels)):
                color = label_colors.get(label, 'red')
                plot_label = label if label and label not in seen else "_nolegend_"
                if label and label not in seen:
                    seen.add(label)
                
                self.axes.scatter(
                    score[pc_x], score[pc_y],
                    c=color,
                    s=self.df.iloc[i].get('Size', 20),
                    alpha=self.df.iloc[i].get('Alpha', 0.7),
                    label=plot_label
                )
                
                if self.show_labels_cb.isChecked():
                    idx_label = self.df.iloc[i].get('Index', str(i))
                    self.axes.annotate(str(idx_label), (score[pc_x], score[pc_y]), fontsize=6)
            
            if seen:
                self.axes.legend(loc='best', fontsize='small')
        else:
            self.axes.scatter(
                self.scores[:, pc_x], self.scores[:, pc_y],
                c='red', s=20, alpha=0.7
            )
        
        total_var = sum(evr[:max(pc_x, pc_y)+1]) * 100
        info_text = f"Total variance explained: {total_var:.1f}%\n"
        info_text += f"Number of components: {self.n_components}"
        self.textbox.setText(info_text)
        
        self.canvas.draw()
    
    def _show_result(self):
        if self.pca is None:
            self.show_error("Run PCA first by plotting.")
            return
        
        loadings = pd.DataFrame(
            self.pca.components_.T,
            columns=[f'PC{i+1}' for i in range(self.n_components)],
            index=self.data_cleaner.slim(self.df).columns
        )
        
        evr_df = pd.DataFrame({
            'Explained Variance': self.pca.explained_variance_,
            'Explained Variance Ratio': self.pca.explained_variance_ratio_
        }, index=[f'PC{i+1}' for i in range(self.n_components)])
        
        result_text = "=== Loadings ===\n" + loadings.to_string() + "\n\n"
        result_text += "=== Explained Variance ===\n" + evr_df.to_string()
        
        TableViewer(loadings, "PCA Loadings", self).show()