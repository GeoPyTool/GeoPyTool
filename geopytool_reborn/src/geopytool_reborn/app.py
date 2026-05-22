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
from PySide6.QtGui import QIcon, QAction, QActionGroup

from . import __version__, __date__
from .core.data_model import PandasModel, DataCleaner
from .ui.table_viewer import TableViewer, CustomTableView
from .ui.widgets import FileDropTableView
from .resources.i18n import tr, set_language, get_language, Translator, get_available_languages

from .diagrams.tas import TAS
from .diagrams.ree import REE
from .diagrams.trace import Trace
from .diagrams.harker import Harker
from .diagrams.pearce import Pearce
from .diagrams.triangular.qapf import QAPF
from .diagrams.triangular.qfl import QFL

from .diagrams.isotopes.rbsr import RbSrIsotope
from .diagrams.isotopes.smnd import SmNdIsotope
from .diagrams.isotopes.kca import KArIsotope
from .diagrams.isotopes.arar import ArArIsotope

from .analysis.pca import PCA
from .analysis.cluster import Cluster
from .analysis.statistics import Statistics
from .analysis.ml import SVMAnalysis, LDAAnalysis, MLPAnalysis, PCAAnalysis

from .tools.cipw import CIPWWindow
from .tools.combine import CombineWindow
from .tools.flatten import FlattenWindow
from .tools.zircon_ce import ZirconCeWindow


class MainWindow(QMainWindow):
    """
    Main application window for GeoPyTool Reborn.
    
    Provides:
    - File loading (CSV, Excel)
    - Data viewing and editing
    - Access to all diagram and analysis tools
    - Multi-language support (English/Chinese)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.translator = Translator.instance()
        self.translator.add_callback(self._update_ui_texts)
        
        self.setWindowTitle(f"{tr('win_main')} v{__version__}")
        self.setMinimumSize(1024, 768)
        
        self.raw_data = pd.DataFrame()
        self.data_cleaner = DataCleaner()
        
        self.open_windows = []
        
        self._setup_ui()
        self._setup_menus()
        self._setup_toolbar()
        self._setup_statusbar()
        
        self.setAcceptDrops(True)

    def _setup_ui(self):
        """Setup the main UI."""
        central = QWidget()
        layout = QVBoxLayout(central)
        
        self.info_label = QLabel(tr('info_load_file'))
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        self.table_view = FileDropTableView(self)
        self.model = PandasModel()
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        self.data_info_label = QLabel()
        layout.addWidget(self.data_info_label)
        
        self.setCentralWidget(central)

    def _setup_menus(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        self.file_menu = menubar.addMenu(tr('menu_file'))
        
        self.open_action = QAction(tr('action_open'), self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)
        
        self.save_action = QAction(tr('action_save'), self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_action)
        
        self.file_menu.addSeparator()
        
        self.quit_action = QAction(tr('action_quit'), self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.quit_action)
        
        self.geochem_menu = menubar.addMenu(tr('menu_geochemistry'))
        
        self.tas_action = QAction(tr('action_tas'), self)
        self.tas_action.triggered.connect(lambda: self._open_diagram(TAS))
        self.geochem_menu.addAction(self.tas_action)
        
        self.ree_action = QAction(tr('action_ree'), self)
        self.ree_action.triggered.connect(lambda: self._open_diagram(REE))
        self.geochem_menu.addAction(self.ree_action)
        
        self.trace_action = QAction(tr('action_trace'), self)
        self.trace_action.triggered.connect(lambda: self._open_diagram(Trace))
        self.geochem_menu.addAction(self.trace_action)
        
        self.harker_action = QAction(tr('action_harker'), self)
        self.harker_action.triggered.connect(lambda: self._open_diagram(Harker))
        self.geochem_menu.addAction(self.harker_action)
        
        self.geochem_menu.addSeparator()
        
        self.pearce_action = QAction(tr('action_pearce'), self)
        self.pearce_action.triggered.connect(lambda: self._open_diagram(Pearce))
        self.geochem_menu.addAction(self.pearce_action)
        
        self.tri_menu = self.geochem_menu.addMenu(tr('menu_triangular'))
        
        self.qapf_action = QAction(tr('action_qapf'), self)
        self.qapf_action.triggered.connect(lambda: self._open_diagram(QAPF))
        self.tri_menu.addAction(self.qapf_action)
        
        self.qfl_action = QAction(tr('action_qfl'), self)
        self.qfl_action.triggered.connect(lambda: self._open_diagram(QFL))
        self.tri_menu.addAction(self.qfl_action)
        
        self.analysis_menu = menubar.addMenu(tr('menu_analysis'))
        
        self.pca_action = QAction(tr('action_pca'), self)
        self.pca_action.triggered.connect(lambda: self._open_diagram(PCA))
        self.analysis_menu.addAction(self.pca_action)
        
        self.cluster_action = QAction(tr('action_cluster'), self)
        self.cluster_action.triggered.connect(lambda: self._open_diagram(Cluster))
        self.analysis_menu.addAction(self.cluster_action)
        
        self.stats_action = QAction(tr('action_statistics'), self)
        self.stats_action.triggered.connect(lambda: self._open_diagram(Statistics))
        self.analysis_menu.addAction(self.stats_action)
        
        self.analysis_menu.addSeparator()
        
        self.ml_menu = self.analysis_menu.addMenu(tr('menu_ml'))
        
        self.pca_ml_action = QAction(tr('action_pca_ml'), self)
        self.pca_ml_action.triggered.connect(lambda: self._open_diagram(PCAAnalysis))
        self.ml_menu.addAction(self.pca_ml_action)
        
        self.svm_action = QAction(tr('action_svm'), self)
        self.svm_action.triggered.connect(lambda: self._open_diagram(SVMAnalysis))
        self.ml_menu.addAction(self.svm_action)
        
        self.lda_action = QAction(tr('action_lda'), self)
        self.lda_action.triggered.connect(lambda: self._open_diagram(LDAAnalysis))
        self.ml_menu.addAction(self.lda_action)
        
        self.mlp_action = QAction(tr('action_mlp'), self)
        self.mlp_action.triggered.connect(lambda: self._open_diagram(MLPAnalysis))
        self.ml_menu.addAction(self.mlp_action)
        
        self.isotope_menu = menubar.addMenu(tr('menu_isotopes'))
        
        self.rbsr_action = QAction(tr('action_rbsr'), self)
        self.rbsr_action.triggered.connect(lambda: self._open_diagram(RbSrIsotope))
        self.isotope_menu.addAction(self.rbsr_action)
        
        self.smnd_action = QAction(tr('action_smnd'), self)
        self.smnd_action.triggered.connect(lambda: self._open_diagram(SmNdIsotope))
        self.isotope_menu.addAction(self.smnd_action)
        
        self.kar_action = QAction(tr('action_kar'), self)
        self.kar_action.triggered.connect(lambda: self._open_diagram(KArIsotope))
        self.isotope_menu.addAction(self.kar_action)
        
        self.arar_action = QAction(tr('action_arar'), self)
        self.arar_action.triggered.connect(lambda: self._open_diagram(ArArIsotope))
        self.isotope_menu.addAction(self.arar_action)
        
        self.tools_menu = menubar.addMenu(tr('menu_tools'))
        
        self.cipw_action = QAction(tr('action_cipw'), self)
        self.cipw_action.triggered.connect(lambda: self._open_diagram(CIPWWindow))
        self.tools_menu.addAction(self.cipw_action)
        
        self.tools_menu.addSeparator()
        
        self.combine_action = QAction(tr('action_combine'), self)
        self.combine_action.triggered.connect(lambda: self._open_diagram(CombineWindow))
        self.tools_menu.addAction(self.combine_action)
        
        self.flatten_action = QAction(tr('action_flatten'), self)
        self.flatten_action.triggered.connect(lambda: self._open_diagram(FlattenWindow))
        self.tools_menu.addAction(self.flatten_action)
        
        self.tools_menu.addSeparator()
        
        self.zircon_ce_action = QAction(tr('action_zircon_ce'), self)
        self.zircon_ce_action.triggered.connect(lambda: self._open_diagram(ZirconCeWindow))
        self.tools_menu.addAction(self.zircon_ce_action)
        
        self.help_menu = menubar.addMenu(tr('menu_help'))
        
        self.lang_menu = self.help_menu.addMenu(tr('menu_language'))
        
        self.lang_group = QActionGroup(self)
        self.lang_group.setExclusive(True)
        
        self.lang_en_action = QAction(tr('lang_en'), self)
        self.lang_en_action.setCheckable(True)
        self.lang_en_action.setChecked(get_language() == 'en')
        self.lang_en_action.triggered.connect(lambda: self._change_language('en'))
        self.lang_menu.addAction(self.lang_en_action)
        self.lang_group.addAction(self.lang_en_action)
        
        self.lang_zh_action = QAction(tr('lang_zh'), self)
        self.lang_zh_action.setCheckable(True)
        self.lang_zh_action.setChecked(get_language() == 'zh')
        self.lang_zh_action.triggered.connect(lambda: self._change_language('zh'))
        self.lang_menu.addAction(self.lang_zh_action)
        self.lang_group.addAction(self.lang_zh_action)
        
        self.help_menu.addSeparator()
        
        self.about_action = QAction(tr('action_about'), self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

    def _setup_toolbar(self):
        """Setup toolbar."""
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)
        
        self.open_btn = QAction(tr('toolbar_open'), self)
        self.open_btn.triggered.connect(self.open_file)
        self.toolbar.addAction(self.open_btn)
        
        self.save_btn = QAction(tr('toolbar_save'), self)
        self.save_btn.triggered.connect(self.save_file)
        self.toolbar.addAction(self.save_btn)
        
        self.toolbar.addSeparator()
        
        self.tas_btn = QAction(tr('toolbar_tas'), self)
        self.tas_btn.triggered.connect(lambda: self._open_diagram(TAS))
        self.toolbar.addAction(self.tas_btn)
        
        self.ree_btn = QAction(tr('toolbar_ree'), self)
        self.ree_btn.triggered.connect(lambda: self._open_diagram(REE))
        self.toolbar.addAction(self.ree_btn)
        
        self.trace_btn = QAction(tr('toolbar_trace'), self)
        self.trace_btn.triggered.connect(lambda: self._open_diagram(Trace))
        self.toolbar.addAction(self.trace_btn)
        
        self.harker_btn = QAction(tr('toolbar_harker'), self)
        self.harker_btn.triggered.connect(lambda: self._open_diagram(Harker))
        self.toolbar.addAction(self.harker_btn)

    def _setup_statusbar(self):
        """Setup status bar."""
        self.statusBar().showMessage(tr('status_ready'))

    def _change_language(self, lang: str):
        """Change the application language."""
        set_language(lang)
        self._update_ui_texts()

    def _update_ui_texts(self):
        """Update all UI texts after language change."""
        self.setWindowTitle(f"{tr('win_main')} v{__version__}")
        
        self.file_menu.setTitle(tr('menu_file'))
        self.open_action.setText(tr('action_open'))
        self.save_action.setText(tr('action_save'))
        self.quit_action.setText(tr('action_quit'))
        
        self.geochem_menu.setTitle(tr('menu_geochemistry'))
        self.tas_action.setText(tr('action_tas'))
        self.ree_action.setText(tr('action_ree'))
        self.trace_action.setText(tr('action_trace'))
        self.harker_action.setText(tr('action_harker'))
        self.pearce_action.setText(tr('action_pearce'))
        self.tri_menu.setTitle(tr('menu_triangular'))
        self.qapf_action.setText(tr('action_qapf'))
        self.qfl_action.setText(tr('action_qfl'))
        
        self.analysis_menu.setTitle(tr('menu_analysis'))
        self.pca_action.setText(tr('action_pca'))
        self.cluster_action.setText(tr('action_cluster'))
        self.stats_action.setText(tr('action_statistics'))
        self.ml_menu.setTitle(tr('menu_ml'))
        self.pca_ml_action.setText(tr('action_pca_ml'))
        self.svm_action.setText(tr('action_svm'))
        self.lda_action.setText(tr('action_lda'))
        self.mlp_action.setText(tr('action_mlp'))
        
        self.isotope_menu.setTitle(tr('menu_isotopes'))
        self.rbsr_action.setText(tr('action_rbsr'))
        self.smnd_action.setText(tr('action_smnd'))
        self.kar_action.setText(tr('action_kar'))
        self.arar_action.setText(tr('action_arar'))
        
        self.tools_menu.setTitle(tr('menu_tools'))
        self.cipw_action.setText(tr('action_cipw'))
        self.combine_action.setText(tr('action_combine'))
        self.flatten_action.setText(tr('action_flatten'))
        self.zircon_ce_action.setText(tr('action_zircon_ce'))
        
        self.help_menu.setTitle(tr('menu_help'))
        self.lang_menu.setTitle(tr('menu_language'))
        self.lang_en_action.setText(tr('lang_en'))
        self.lang_zh_action.setText(tr('lang_zh'))
        self.about_action.setText(tr('action_about'))
        
        self.open_btn.setText(tr('toolbar_open'))
        self.save_btn.setText(tr('toolbar_save'))
        self.tas_btn.setText(tr('toolbar_tas'))
        self.ree_btn.setText(tr('toolbar_ree'))
        self.trace_btn.setText(tr('toolbar_trace'))
        self.harker_btn.setText(tr('toolbar_harker'))
        
        if self.raw_data.empty:
            self.info_label.setText(tr('info_load_file'))
        
        self.statusBar().showMessage(tr('status_ready'))

    def open_file(self):
        """Open a data file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, tr('dialog_open_file'), "",
            f"{tr('filter_all')};;{tr('filter_csv')};;{tr('filter_excel')}"
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
            
            df = self.data_cleaner.ensure_style_columns(df)
            
            self.raw_data = df
            self.model = PandasModel(df)
            self.table_view.setModel(self.model)
            
            self.info_label.setText(f"{tr('info_loaded')} {os.path.basename(filepath)}")
            self.data_info_label.setText(f"{tr('label_rows')} {len(df)}, {tr('label_columns')} {len(df.columns)}")
            self.statusBar().showMessage(f"{tr('status_loaded')} {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, tr('msg_error'), f"Failed to load file:\n{str(e)}")

    def save_file(self):
        """Save data to file."""
        if self.raw_data.empty:
            QMessageBox.warning(self, tr('msg_warning'), tr('msg_no_data'))
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, tr('dialog_save_file'), "",
            f"{tr('filter_excel')};;{tr('filter_csv')}"
        )
        
        if filepath:
            try:
                if filepath.lower().endswith('.csv'):
                    self.raw_data.to_csv(filepath, index=False, encoding='utf-8')
                else:
                    self.raw_data.to_excel(filepath, index=False)
                
                self.statusBar().showMessage(f"{tr('msg_save_success')} {filepath}")
                
            except Exception as e:
                QMessageBox.critical(self, tr('msg_error'), f"Failed to save file:\n{str(e)}")

    def _open_diagram(self, diagram_class):
        """Open a diagram window with current data."""
        if self.raw_data.empty:
            QMessageBox.warning(self, tr('msg_warning'), tr('msg_load_first'))
            return
        
        try:
            window = diagram_class(df=self.raw_data.copy(), parent=self)
            window.show()
            self.open_windows.append(window)
        except Exception as e:
            QMessageBox.critical(self, tr('msg_error'), f"Failed to open diagram:\n{str(e)}")

    def on_data_loaded(self, df, filepath):
        """Callback when data is loaded via drag-drop."""
        df = self.data_cleaner.ensure_style_columns(df)
        self.raw_data = df
        self.model = PandasModel(df)
        self.table_view.setModel(self.model)
        
        self.info_label.setText(f"{tr('info_loaded')} {os.path.basename(filepath)}")
        self.data_info_label.setText(f"{tr('label_rows')} {len(df)}, {tr('label_columns')} {len(df.columns)}")
        self.statusBar().showMessage(f"{tr('status_loaded')} {filepath}")

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
            self, tr('about_title'),
            f"<h2>GeoPyTool Reborn</h2>"
            f"<p>{tr('about_version')} {__version__}</p>"
            f"<p>{tr('about_date')} {__date__}</p>"
            f"<p>{tr('about_desc')}</p>"
            f"<p>{tr('about_restructured')}</p>"
            f"<p>{tr('about_website')} <a href='https://github.com/GeoPyTool/GeoPyTool'>GitHub</a></p>"
        )

    def closeEvent(self, event):
        """Handle close event."""
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