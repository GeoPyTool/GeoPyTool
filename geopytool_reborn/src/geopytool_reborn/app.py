# -*- coding: utf-8 -*-
"""
GeoPyTool Reborn - Main Application Window

The main application window that provides access to all geochemistry
analysis tools and diagrams.
"""

import sys
import os
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QStatusBar, QFileDialog, QMessageBox,
    QTableView, QLabel, QToolBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction

from . import __version__, __date__
from .core.data_model import PandasModel, DataCleaner
from .ui.table_viewer import TableViewer, CustomTableView
from .ui.widgets import FileDropTableView

# Import diagram modules
from .diagrams.tas import TAS
from .diagrams.ree import REE
from .diagrams.trace import Trace
from .diagrams.harker import Harker
from .diagrams.pearce import Pearce
from .diagrams.triangular.qapf import QAPF
from .diagrams.triangular.qfl import QFL

# Import isotope diagram modules
from .diagrams.isotopes.rbsr import RbSrIsotope
from .diagrams.isotopes.smnd import SmNdIsotope
from .diagrams.isotopes.kca import KArIsotope
from .diagrams.isotopes.arar import ArArIsotope

# Import analysis modules
from .analysis.pca import PCA
from .analysis.cluster import Cluster
from .analysis.statistics import Statistics
from .analysis.ml import SVMAnalysis, LDAAnalysis, MLPAnalysis, PCAAnalysis

# Import tool modules
from .tools.cipw import CIPWWindow
from .tools.combine import CombineWindow
from .tools.flatten import FlattenWindow


class MainWindow(QMainWindow):
    """
    Main application window for GeoPyTool Reborn.
    
    Provides:
    - File loading (CSV, Excel)
    - Data viewing and editing
    - Access to all diagram and analysis tools
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"GeoPyTool Reborn v{__version__}")
        self.setMinimumSize(1024, 768)
        
        # Data storage
        self.raw_data = pd.DataFrame()
        self.data_cleaner = DataCleaner()
        
        # Track open windows
        self.open_windows = []
        
        # Setup UI
        self._setup_ui()
        self._setup_menus()
        self._setup_toolbar()
        self._setup_statusbar()
        
        # Accept file drops
        self.setAcceptDrops(True)

    def _setup_ui(self):
        """Setup the main UI."""
        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)
        
        # Info label
        self.info_label = QLabel("Load a data file to begin (CSV or Excel)")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        # Data table
        self.table_view = FileDropTableView(self)
        self.model = PandasModel()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        # Status info
        self.data_info_label = QLabel()
        layout.addWidget(self.data_info_label)
        
        self.setCentralWidget(central)

    def _setup_menus(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save...", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Geochemistry menu
        geochem_menu = menubar.addMenu("&Geochemistry")
        
        tas_action = QAction("TAS Diagram", self)
        tas_action.triggered.connect(lambda: self._open_diagram(TAS))
        geochem_menu.addAction(tas_action)
        
        ree_action = QAction("REE Spider Diagram", self)
        ree_action.triggered.connect(lambda: self._open_diagram(REE))
        geochem_menu.addAction(ree_action)
        
        trace_action = QAction("Trace Element Diagram", self)
        trace_action.triggered.connect(lambda: self._open_diagram(Trace))
        geochem_menu.addAction(trace_action)
        
        harker_action = QAction("Harker Diagram", self)
        harker_action.triggered.connect(lambda: self._open_diagram(Harker))
        geochem_menu.addAction(harker_action)
        
        geochem_menu.addSeparator()
        
        pearce_action = QAction("Pearce Tectonic Diagram", self)
        pearce_action.triggered.connect(lambda: self._open_diagram(Pearce))
        geochem_menu.addAction(pearce_action)
        
        # Triangular diagrams submenu
        tri_menu = geochem_menu.addMenu("Triangular Diagrams")
        
        qapf_action = QAction("QAPF Diagram", self)
        qapf_action.triggered.connect(lambda: self._open_diagram(QAPF))
        tri_menu.addAction(qapf_action)
        
        qfl_action = QAction("QFL Diagram", self)
        qfl_action.triggered.connect(lambda: self._open_diagram(QFL))
        tri_menu.addAction(qfl_action)
        
        # Analysis menu
        analysis_menu = menubar.addMenu("&Analysis")
        
        pca_action = QAction("PCA", self)
        pca_action.triggered.connect(lambda: self._open_diagram(PCA))
        analysis_menu.addAction(pca_action)
        
        cluster_action = QAction("Cluster Analysis", self)
        cluster_action.triggered.connect(lambda: self._open_diagram(Cluster))
        analysis_menu.addAction(cluster_action)
        
        stats_action = QAction("Statistics", self)
        stats_action.triggered.connect(lambda: self._open_diagram(Statistics))
        analysis_menu.addAction(stats_action)
        
        analysis_menu.addSeparator()
        
        # Machine Learning submenu
        ml_menu = analysis_menu.addMenu("Machine Learning")
        
        pca_ml_action = QAction("PCA Analysis", self)
        pca_ml_action.triggered.connect(lambda: self._open_diagram(PCAAnalysis))
        ml_menu.addAction(pca_ml_action)
        
        svm_action = QAction("SVM Classification", self)
        svm_action.triggered.connect(lambda: self._open_diagram(SVMAnalysis))
        ml_menu.addAction(svm_action)
        
        lda_action = QAction("LDA Analysis", self)
        lda_action.triggered.connect(lambda: self._open_diagram(LDAAnalysis))
        ml_menu.addAction(lda_action)
        
        mlp_action = QAction("MLP Neural Network", self)
        mlp_action.triggered.connect(lambda: self._open_diagram(MLPAnalysis))
        ml_menu.addAction(mlp_action)
        
        # Isotope menu
        isotope_menu = menubar.addMenu("&Isotopes")
        
        rbsr_action = QAction("Rb-Sr Isochron", self)
        rbsr_action.triggered.connect(lambda: self._open_diagram(RbSrIsotope))
        isotope_menu.addAction(rbsr_action)
        
        smnd_action = QAction("Sm-Nd Isochron", self)
        smnd_action.triggered.connect(lambda: self._open_diagram(SmNdIsotope))
        isotope_menu.addAction(smnd_action)
        
        kar_action = QAction("K-Ar Isochron", self)
        kar_action.triggered.connect(lambda: self._open_diagram(KArIsotope))
        isotope_menu.addAction(kar_action)
        
        arar_action = QAction("Ar-Ar Isochron", self)
        arar_action.triggered.connect(lambda: self._open_diagram(ArArIsotope))
        isotope_menu.addAction(arar_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        cipw_action = QAction("CIPW Norm Calculator", self)
        cipw_action.triggered.connect(lambda: self._open_diagram(CIPWWindow))
        tools_menu.addAction(cipw_action)
        
        tools_menu.addSeparator()
        
        combine_action = QAction("Combine Data", self)
        combine_action.triggered.connect(lambda: self._open_diagram(CombineWindow))
        tools_menu.addAction(combine_action)
        
        flatten_action = QAction("Flatten Data", self)
        flatten_action.triggered.connect(lambda: self._open_diagram(FlattenWindow))
        tools_menu.addAction(flatten_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self):
        """Setup toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Quick access buttons
        open_btn = QAction("Open", self)
        open_btn.triggered.connect(self.open_file)
        toolbar.addAction(open_btn)
        
        save_btn = QAction("Save", self)
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)
        
        toolbar.addSeparator()
        
        tas_btn = QAction("TAS", self)
        tas_btn.triggered.connect(lambda: self._open_diagram(TAS))
        toolbar.addAction(tas_btn)
        
        ree_btn = QAction("REE", self)
        ree_btn.triggered.connect(lambda: self._open_diagram(REE))
        toolbar.addAction(ree_btn)
        
        trace_btn = QAction("Trace", self)
        trace_btn.triggered.connect(lambda: self._open_diagram(Trace))
        toolbar.addAction(trace_btn)
        
        harker_btn = QAction("Harker", self)
        harker_btn.triggered.connect(lambda: self._open_diagram(Harker))
        toolbar.addAction(harker_btn)

    def _setup_statusbar(self):
        """Setup status bar."""
        self.statusBar().showMessage("Ready")

    def open_file(self):
        """Open a data file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Data File", "",
            "All Supported (*.csv *.xlsx *.xls);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        
        if filepath:
            self._load_file(filepath)

    def _load_file(self, filepath):
        """Load data from file."""
        try:
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath, engine='python')
            else:
                df = pd.read_excel(filepath, engine='openpyxl')
            
            # Ensure required columns
            df = self.data_cleaner.ensure_style_columns(df)
            
            self.raw_data = df
            self.model = PandasModel(df)
            self.table_view.setModel(self.model)
            
            # Update info
            self.info_label.setText(f"Loaded: {os.path.basename(filepath)}")
            self.data_info_label.setText(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            self.statusBar().showMessage(f"Loaded {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")

    def save_file(self):
        """Save data to file."""
        if self.raw_data.empty:
            QMessageBox.warning(self, "Warning", "No data to save.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Data File", "",
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        
        if filepath:
            try:
                if filepath.lower().endswith('.csv'):
                    self.raw_data.to_csv(filepath, index=False, encoding='utf-8')
                else:
                    self.raw_data.to_excel(filepath, index=False)
                
                self.statusBar().showMessage(f"Saved to {filepath}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def _open_diagram(self, diagram_class):
        """Open a diagram window with current data."""
        if self.raw_data.empty:
            QMessageBox.warning(self, "Warning", "Please load data first.")
            return
        
        try:
            window = diagram_class(df=self.raw_data.copy(), parent=self)
            window.show()
            self.open_windows.append(window)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open diagram:\n{str(e)}")

    def on_data_loaded(self, df, filepath):
        """Callback when data is loaded via drag-drop."""
        df = self.data_cleaner.ensure_style_columns(df)
        self.raw_data = df
        self.model = PandasModel(df)
        self.table_view.setModel(self.model)
        
        self.info_label.setText(f"Loaded: {os.path.basename(filepath)}")
        self.data_info_label.setText(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        self.statusBar().showMessage(f"Loaded {filepath}")

    def dragEnterEvent(self, event):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle drop events."""
        urls = event.mimeData().urls()
        for url in urls:
            filepath = url.toLocalFile()
            if filepath.lower().endswith(('.csv', '.xlsx', '.xls')):
                self._load_file(filepath)
                break

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About GeoPyTool Reborn",
            f"<h2>GeoPyTool Reborn</h2>"
            f"<p>Version: {__version__}</p>"
            f"<p>Date: {__date__}</p>"
            f"<p>A comprehensive geochemistry data analysis toolkit.</p>"
            f"<p>Restructured from the original GeoPyTool by cycleuser.</p>"
            f"<p>Website: <a href='https://github.com/GeoPyTool/GeoPyTool'>GitHub</a></p>"
        )

    def closeEvent(self, event):
        """Handle close event."""
        # Close all child windows
        for window in self.open_windows:
            try:
                window.close()
            except:
                pass
        event.accept()


def run():
    """Run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("GeoPyTool Reborn")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
