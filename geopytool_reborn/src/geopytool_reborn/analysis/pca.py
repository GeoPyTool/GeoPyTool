# -*- coding: utf-8 -*-
"""
PCA (Principal Component Analysis) Module

Dimensionality reduction and visualization tool for geochemical data.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearn_PCA

from PySide6.QtWidgets import (
    QCheckBox, QLabel, QPushButton, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..ui.table_viewer import TableViewer


class PCA(BasePlotWindow):
    """
    Principal Component Analysis visualization.
    
    Features:
    - Automatic data scaling
    - Selectable number of components
    - Score and loading plots
    - Variance explained table
    """
    
    title = "Principal Component Analysis (PCA)"
    reference = "PCA reduces dimensionality while preserving variance structure."
    items_to_check = []  # Will use all numeric columns
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.pca_model = None
        self.scores = None
        self.loadings = None
        self.explained_variance = None
        self.feature_names = []
        super().__init__(df, parent)
        
        if not df.empty:
            self._run_pca()
            self.plot()
    
    def create_controls(self):
        """Add PCA-specific controls."""
        # Number of components
        self.n_components_label = QLabel("Components:")
        self.n_components_spin = QSpinBox()
        self.n_components_spin.setRange(2, 10)
        self.n_components_spin.setValue(2)
        self.n_components_spin.valueChanged.connect(self._run_pca)
        self.n_components_spin.valueChanged.connect(self.plot)
        
        # Plot type
        self.plot_type_label = QLabel("Plot:")
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Scores", "Loadings", "Biplot"])
        self.plot_type_combo.currentIndexChanged.connect(self.plot)
        
        # PC axes selection
        self.pc_x_label = QLabel("PC X:")
        self.pc_x_spin = QSpinBox()
        self.pc_x_spin.setRange(1, 10)
        self.pc_x_spin.setValue(1)
        self.pc_x_spin.valueChanged.connect(self.plot)
        
        self.pc_y_label = QLabel("PC Y:")
        self.pc_y_spin = QSpinBox()
        self.pc_y_spin.setRange(1, 10)
        self.pc_y_spin.setValue(2)
        self.pc_y_spin.valueChanged.connect(self.plot)
        
        # Checkboxes
        self.legend_cb = QCheckBox("Legend")
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.plot)
        
        # Results buttons
        self.variance_button = QPushButton("Variance")
        self.variance_button.clicked.connect(self.show_variance)
        
        self.loadings_button = QPushButton("Loadings")
        self.loadings_button.clicked.connect(self.show_loadings)
        
        # Add to layout
        self.control_layout.addWidget(self.n_components_label)
        self.control_layout.addWidget(self.n_components_spin)
        self.control_layout.addWidget(self.plot_type_label)
        self.control_layout.addWidget(self.plot_type_combo)
        self.control_layout.addWidget(self.pc_x_label)
        self.control_layout.addWidget(self.pc_x_spin)
        self.control_layout.addWidget(self.pc_y_label)
        self.control_layout.addWidget(self.pc_y_spin)
        self.control_layout.addWidget(self.legend_cb)
        self.control_layout.addWidget(self.variance_button)
        self.control_layout.addWidget(self.loadings_button)

    def _run_pca(self):
        """Run PCA on the data."""
        if self._df.empty:
            return
        
        # Get numeric columns only
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty:
            return
        
        self.feature_names = df_slim.columns.tolist()
        n_samples = len(df_slim)
        n_features = len(self.feature_names)
        
        # Limit components
        max_components = min(n_samples, n_features, self.n_components_spin.value())
        if max_components < 2:
            return
        
        # Scale data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(df_slim)
        
        # Run PCA
        self.pca_model = sklearn_PCA(n_components=max_components)
        self.scores = self.pca_model.fit_transform(data_scaled)
        self.loadings = self.pca_model.components_.T
        self.explained_variance = self.pca_model.explained_variance_ratio_
        
        # Update spinbox ranges
        self.pc_x_spin.setRange(1, max_components)
        self.pc_y_spin.setRange(1, max_components)

    def plot(self):
        """Draw the PCA plot."""
        self.axes.clear()
        
        if self.scores is None:
            return
        
        plot_type = self.plot_type_combo.currentText()
        pc_x = self.pc_x_spin.value() - 1
        pc_y = self.pc_y_spin.value() - 1
        
        if pc_x >= self.scores.shape[1] or pc_y >= self.scores.shape[1]:
            return
        
        if plot_type == "Scores":
            self._plot_scores(pc_x, pc_y)
        elif plot_type == "Loadings":
            self._plot_loadings(pc_x, pc_y)
        elif plot_type == "Biplot":
            self._plot_biplot(pc_x, pc_y)
        
        # Labels with variance
        var_x = self.explained_variance[pc_x] * 100 if pc_x < len(self.explained_variance) else 0
        var_y = self.explained_variance[pc_y] * 100 if pc_y < len(self.explained_variance) else 0
        
        self.axes.set_xlabel(f'PC{pc_x+1} ({var_x:.1f}%)')
        self.axes.set_ylabel(f'PC{pc_y+1} ({var_y:.1f}%)')
        self.axes.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        self.axes.axvline(x=0, color='gray', linestyle='--', linewidth=0.5)
        
        # Legend
        if self.legend_cb.isChecked():
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(loc='best', fontsize=8)
        
        self.canvas.draw()

    def _plot_scores(self, pc_x, pc_y):
        """Plot PCA scores."""
        seen_labels = set()
        
        for i, row in self._df.iterrows():
            if i >= len(self.scores):
                continue
            
            label = str(row.get('Label', ''))
            if label and label not in seen_labels:
                plot_label = label
                seen_labels.add(label)
            else:
                plot_label = "_nolegend_"
            
            self.axes.scatter(
                self.scores[i, pc_x], self.scores[i, pc_y],
                marker=row.get('Marker', 'o'),
                c=row.get('Color', 'blue'),
                s=row.get('Size', 40),
                alpha=row.get('Alpha', 0.7),
                label=plot_label,
                edgecolors='none'
            )

    def _plot_loadings(self, pc_x, pc_y):
        """Plot PCA loadings."""
        for i, name in enumerate(self.feature_names):
            x = self.loadings[i, pc_x]
            y = self.loadings[i, pc_y]
            
            self.axes.arrow(0, 0, x, y, head_width=0.03, head_length=0.02, 
                           fc='red', ec='red', alpha=0.7)
            self.axes.text(x*1.1, y*1.1, name, fontsize=8, ha='center', alpha=0.8)

    def _plot_biplot(self, pc_x, pc_y):
        """Plot biplot (scores + loadings)."""
        self._plot_scores(pc_x, pc_y)
        
        # Scale loadings to fit with scores
        scale = np.max(np.abs(self.scores[:, [pc_x, pc_y]])) / np.max(np.abs(self.loadings[:, [pc_x, pc_y]]))
        
        for i, name in enumerate(self.feature_names):
            x = self.loadings[i, pc_x] * scale * 0.8
            y = self.loadings[i, pc_y] * scale * 0.8
            
            self.axes.arrow(0, 0, x, y, head_width=scale*0.02, head_length=scale*0.01,
                           fc='red', ec='red', alpha=0.5)
            self.axes.text(x*1.1, y*1.1, name, fontsize=7, ha='center', color='red', alpha=0.7)

    def show_variance(self):
        """Show explained variance table."""
        if self.explained_variance is None:
            return
        
        data = {
            'PC': [f'PC{i+1}' for i in range(len(self.explained_variance))],
            'Variance (%)': [f'{v*100:.2f}' for v in self.explained_variance],
            'Cumulative (%)': [f'{sum(self.explained_variance[:i+1])*100:.2f}' 
                              for i in range(len(self.explained_variance))]
        }
        
        df = pd.DataFrame(data)
        viewer = TableViewer(df, "PCA Explained Variance", self)
        viewer.show()

    def show_loadings(self):
        """Show loadings table."""
        if self.loadings is None:
            return
        
        data = {'Feature': self.feature_names}
        for i in range(self.loadings.shape[1]):
            data[f'PC{i+1}'] = [f'{v:.4f}' for v in self.loadings[:, i]]
        
        df = pd.DataFrame(data)
        viewer = TableViewer(df, "PCA Loadings", self)
        viewer.show()
