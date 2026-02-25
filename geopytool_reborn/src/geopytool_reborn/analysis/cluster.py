# -*- coding: utf-8 -*-
"""
Cluster Analysis Module

Hierarchical and k-means clustering for geochemical data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

from PySide6.QtWidgets import (
    QCheckBox, QLabel, QPushButton, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt

from ..core.base_widget import BasePlotWindow
from ..ui.table_viewer import TableViewer


class Cluster(BasePlotWindow):
    """
    Cluster Analysis visualization.
    
    Features:
    - Hierarchical clustering (dendrogram)
    - K-means clustering
    - Multiple linkage methods
    - Distance metrics
    """
    
    title = "Cluster Analysis"
    reference = "Hierarchical and K-means clustering for sample grouping."
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        self.cluster_labels = None
        self.linkage_matrix = None
        super().__init__(df, parent)
        
        if not df.empty:
            self.plot()
    
    def create_controls(self):
        """Add Cluster-specific controls."""
        # Cluster type
        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Dendrogram", "K-Means"])
        self.type_combo.currentIndexChanged.connect(self.plot)
        
        # Number of clusters (for K-means)
        self.n_clusters_label = QLabel("Clusters:")
        self.n_clusters_spin = QSpinBox()
        self.n_clusters_spin.setRange(2, 20)
        self.n_clusters_spin.setValue(3)
        self.n_clusters_spin.valueChanged.connect(self.plot)
        
        # Linkage method
        self.linkage_label = QLabel("Linkage:")
        self.linkage_combo = QComboBox()
        self.linkage_combo.addItems(["ward", "complete", "average", "single"])
        self.linkage_combo.currentIndexChanged.connect(self.plot)
        
        # Distance metric
        self.metric_label = QLabel("Distance:")
        self.metric_combo = QComboBox()
        self.metric_combo.addItems(["euclidean", "manhattan", "cosine"])
        self.metric_combo.currentIndexChanged.connect(self.plot)
        
        # Results button
        self.result_button = QPushButton("Cluster Labels")
        self.result_button.clicked.connect(self.show_results)
        
        # Add to layout
        self.control_layout.addWidget(self.type_label)
        self.control_layout.addWidget(self.type_combo)
        self.control_layout.addWidget(self.n_clusters_label)
        self.control_layout.addWidget(self.n_clusters_spin)
        self.control_layout.addWidget(self.linkage_label)
        self.control_layout.addWidget(self.linkage_combo)
        self.control_layout.addWidget(self.metric_label)
        self.control_layout.addWidget(self.metric_combo)
        self.control_layout.addWidget(self.result_button)

    def plot(self):
        """Draw the cluster analysis plot."""
        self.axes.clear()
        
        if self._df.empty:
            return
        
        cluster_type = self.type_combo.currentText()
        
        if cluster_type == "Dendrogram":
            self._plot_dendrogram()
        else:
            self._plot_kmeans()
        
        self.canvas.draw()

    def _plot_dendrogram(self):
        """Plot hierarchical clustering dendrogram."""
        # Get numeric data
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty or len(df_slim) < 2:
            return
        
        # Scale data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(df_slim)
        
        # Get linkage method and metric
        method = self.linkage_combo.currentText()
        metric = self.metric_combo.currentText()
        
        # Ward method requires euclidean distance
        if method == 'ward':
            metric = 'euclidean'
        
        # Compute linkage
        self.linkage_matrix = linkage(data_scaled, method=method, metric=metric)
        
        # Get labels
        if 'Label' in self._df.columns:
            labels = self._df['Label'].iloc[:len(df_slim)].tolist()
        else:
            labels = [str(i) for i in range(len(df_slim))]
        
        # Plot dendrogram
        dendrogram(
            self.linkage_matrix,
            labels=labels,
            ax=self.axes,
            leaf_rotation=90,
            leaf_font_size=8
        )
        
        self.axes.set_ylabel('Distance')
        self.axes.set_title('Hierarchical Clustering Dendrogram')

    def _plot_kmeans(self):
        """Plot K-means clustering results."""
        # Get numeric data
        df_slim = self.data_cleaner.slim(self._df.copy())
        if df_slim.empty or len(df_slim) < 2:
            return
        
        # Scale data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(df_slim)
        
        n_clusters = min(self.n_clusters_spin.value(), len(df_slim))
        
        # Run K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = kmeans.fit_predict(data_scaled)
        
        # Use first two principal components for visualization
        if data_scaled.shape[1] >= 2:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            data_2d = pca.fit_transform(data_scaled)
            
            # Plot with cluster colors
            colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))
            
            for cluster_id in range(n_clusters):
                mask = self.cluster_labels == cluster_id
                self.axes.scatter(
                    data_2d[mask, 0], data_2d[mask, 1],
                    c=[colors[cluster_id]],
                    label=f'Cluster {cluster_id + 1}',
                    s=40, alpha=0.7, edgecolors='none'
                )
            
            # Plot centers
            centers_2d = pca.transform(kmeans.cluster_centers_)
            self.axes.scatter(
                centers_2d[:, 0], centers_2d[:, 1],
                c='black', marker='x', s=100, linewidths=2,
                label='Centers'
            )
            
            self.axes.set_xlabel('PC1')
            self.axes.set_ylabel('PC2')
            self.axes.legend(loc='best', fontsize=8)
        
        self.axes.set_title(f'K-Means Clustering (k={n_clusters})')

    def show_results(self):
        """Show cluster assignments."""
        if self.cluster_labels is None:
            return
        
        data = {
            'Sample': list(range(len(self.cluster_labels))),
            'Cluster': [f'Cluster {c+1}' for c in self.cluster_labels]
        }
        
        if 'Label' in self._df.columns:
            data['Label'] = self._df['Label'].iloc[:len(self.cluster_labels)].tolist()
        
        df = pd.DataFrame(data)
        viewer = TableViewer(df, "Cluster Assignments", self)
        viewer.show()
