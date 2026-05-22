# -*- coding: utf-8 -*-
"""
Zircon Ce(IV)/Ce(III) Oxygen Fugacity Estimation

Implements the Ballard et al. (2002) method for estimating oxygen fugacity
from Ce(IV)/Ce(III) ratios in zircon.

Reference:
Ballard, J. R., Palin, M. J., and Campbell, I. H., 2002, Relative oxidation 
states of magmas inferred from Ce(IV)/Ce(III) in zircon: application to 
porphyry copper deposits of northern Chile: Contributions to Mineralogy and 
Petrology, v. 144, no. 3, p. 347-364.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableView, QMessageBox, QFileDialog, QTextEdit
)
from PySide6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from ..core.data_model import PandasModel
from ..resources.i18n import tr


REFERENCE = (
    'Ballard, J. R., Palin, M. J., and Campbell, I. H., 2002, '
    'Relative oxidation states of magmas inferred from Ce(IV)/Ce(III) in zircon: '
    'application to porphyry copper deposits of northern Chile: '
    'Contributions to Mineralogy and Petrology, v. 144, no. 3, p. 347-364.'
)

ELEMENTS_REE3 = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
ELEMENTS_OTHER = ['Th', 'U', 'Hf', 'Zr', 'Ce4']

RI_REE3 = [1.16, 1.143, 1.126, 1.109, 1.079, 1.066, 1.053, 1.04, 1.027, 1.015, 1.004, 0.994, 0.985, 0.977]
RO_REE3 = [0.84] * len(RI_REE3)

RI_OTHER = [1.05, 1.00, 0.83, 0.840, 0.97]
RO_OTHER = [0.84] * len(RI_OTHER)

ZIRCON_ZR = 497555


def compute_x_values(ri_list: List[float], ro_list: List[float]) -> List[float]:
    return [(ri / 3 + ro / 6) * (ri - ro) ** 2 for ri, ro in zip(ri_list, ro_list)]


class ZirconCeCalculator:
    """
    Zircon Ce(IV)/Ce(III) Oxygen Fugacity Calculator.
    
    Implements the lattice strain model of Ballard et al. (2002).
    """
    
    def __init__(self):
        self.x3 = compute_x_values(RI_REE3, RO_REE3)
        self.x4 = compute_x_values(RI_OTHER, RO_OTHER)
        
        self.x_ce3 = self.x3[ELEMENTS_REE3.index('Ce')]
        self.x_ce4 = self.x4[ELEMENTS_OTHER.index('Ce4')]
        
    def calculate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Calculate Ce4+/Ce3+ ratios for all zircon samples.
        """
        df_copy = df.copy()
        df_copy.columns = [str(c).strip() for c in df_copy.columns]
        
        base_idx = None
        base_ce = None
        base_zr = None
        zircon_indices = []
        
        for i in range(len(df_copy)):
            dtype = str(df_copy.iloc[i].get('DataType', '')).strip()
            if dtype == 'Base':
                base_idx = i
                base_ce = float(df_copy.iloc[i].get('Ce', 0))
                base_zr = float(df_copy.iloc[i].get('Zr', 0))
            elif dtype == 'Zircon':
                zircon_indices.append(i)
        
        if base_idx is None:
            raise ValueError("No row with DataType='Base' found in the data.")
        
        if not zircon_indices:
            raise ValueError("No rows with DataType='Zircon' found in the data.")
        
        columns = df_copy.columns.tolist()
        
        used_elements3 = []
        data_x3 = []
        ybase3 = []
        
        used_elements4 = []
        data_x4 = []
        ybase4 = []
        
        for col in columns:
            if col in ELEMENTS_REE3:
                used_elements3.append(col)
                data_x3.append(self.x3[ELEMENTS_REE3.index(col)])
                ybase3.append(float(df_copy.iloc[base_idx].get(col, 0)))
            elif col in ELEMENTS_OTHER:
                used_elements4.append(col)
                data_x4.append(self.x4[ELEMENTS_OTHER.index(col)])
                ybase4.append(float(df_copy.iloc[base_idx].get(col, 0)))
        
        results = []
        plot_data = {
            'scatter3': [],
            'scatter4': [],
            'line3': [],
            'line4': [],
            'labels3': [],
            'labels4': [],
        }
        
        for idx in zircon_indices:
            tmpy3 = []
            tmpy4 = []
            
            for j, elem in enumerate(used_elements3):
                val = float(df_copy.iloc[idx].get(elem, 0))
                base_val = ybase3[j]
                if base_val > 0 and val > 0:
                    tmpy3.append(np.log(val / base_val))
                else:
                    tmpy3.append(np.nan)
            
            for j, elem in enumerate(used_elements4):
                val = float(df_copy.iloc[idx].get(elem, 0))
                base_val = ybase4[j]
                if base_val > 0 and val > 0:
                    tmpy4.append(np.log(val / base_val))
                else:
                    tmpy4.append(np.nan)
            
            fit_data_x3 = []
            fit_tmpy3 = []
            for q_idx, q in enumerate(used_elements3):
                if q != 'Ce' and not np.isnan(tmpy3[q_idx]):
                    fit_data_x3.append(data_x3[q_idx])
                    fit_tmpy3.append(tmpy3[q_idx])
            
            fit_data_x4 = []
            fit_tmpy4 = []
            for q_idx, q in enumerate(used_elements4):
                if q != 'Ce4' and not np.isnan(tmpy4[q_idx]):
                    fit_data_x4.append(data_x4[q_idx])
                    fit_tmpy4.append(tmpy4[q_idx])
            
            if len(fit_data_x3) < 2 or len(fit_data_x4) < 2:
                continue
            
            tmpz3 = np.polyfit(fit_data_x3, fit_tmpy3, 1)
            tmpz4 = np.polyfit(fit_data_x4, fit_tmpy4, 1)
            
            p3 = np.poly1d(tmpz3)
            p4 = np.poly1d(tmpz4)
            
            xline3 = np.linspace(min(fit_data_x3), max(fit_data_x3), 30)
            yline3 = p3(xline3)
            
            xline4 = np.linspace(min(fit_data_x4), max(fit_data_x4), 30)
            yline4 = p4(xline4)
            
            ce3_test = np.exp(p3(self.x_ce3) + np.log(base_ce))
            d_ce3_test = np.exp(p3(self.x_ce3))
            ce4_test = np.exp(p4(self.x_ce4) + np.log(base_ce))
            d_ce4_test = np.exp(p4(self.x_ce4))
            
            plot_data['scatter3'].append((data_x3, tmpy3))
            plot_data['scatter4'].append((data_x4, tmpy4))
            plot_data['line3'].append((xline3, yline3))
            plot_data['line4'].append((xline4, yline4))
            plot_data['labels3'].append((data_x3, tmpy3, used_elements3))
            plot_data['labels4'].append((data_x4, tmpy4, used_elements4))
            
            zircon_label = str(df_copy.iloc[idx].get('Label', f'Sample {idx}'))
            zircon_ce_val = float(df_copy.iloc[idx].get('Ce', 0))
            
            if d_ce3_test > 0 and d_ce4_test > 0:
                zircon_ce4_3_ratio = (base_ce - zircon_ce_val / d_ce3_test) / (
                    zircon_ce_val / d_ce4_test - base_ce
                )
                melt_ce4_3_ratio = (zircon_ce_val - ce3_test) / ce3_test * d_ce3_test / d_ce4_test
            else:
                zircon_ce4_3_ratio = np.nan
                melt_ce4_3_ratio = np.nan
            
            d_ce_zircon_melt = zircon_ce_val / base_ce if base_ce > 0 else np.nan
            
            results.append({
                'Zircon Sample Label': zircon_label,
                'Zircon Ce4_3 Ratio': zircon_ce4_3_ratio,
                'Melt Ce4_3 Ratio': melt_ce4_3_ratio,
                'DCe4': d_ce4_test,
                'DCe3': d_ce3_test,
                'DCe Zircon/Melt': d_ce_zircon_melt,
            })
        
        result_df = pd.DataFrame(results)
        return result_df, plot_data


class ZirconCeWindow(QMainWindow):
    """
    Zircon Ce(IV)/Ce(III) Oxygen Fugacity Estimation Window.
    
    Provides interface for calculating and visualizing Ce4+/Ce3+ ratios
    using the Ballard et al. (2002) lattice strain model.
    """
    
    title = "Zircon Ce Oxygen Fugacity"
    items_to_check = ['DataType', 'Ce', 'Zr'] + ELEMENTS_REE3 + ELEMENTS_OTHER
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('win_zircon_ce'))
        self.resize(1200, 800)
        self.df = df
        self.parent_window = parent
        self.calculator = ZirconCeCalculator()
        
        self.result_df = pd.DataFrame()
        self.plot_data = {}
        
        self._setup_ui()
        
        if not self.df.empty:
            self._calculate()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        control_layout = QHBoxLayout()
        
        self.calc_button = QPushButton(tr('btn_calc_zircon_ce'))
        self.calc_button.clicked.connect(self._calculate)
        control_layout.addWidget(self.calc_button)
        
        self.show_result_button = QPushButton(tr('btn_show_result'))
        self.show_result_button.clicked.connect(self._show_result)
        self.show_result_button.setEnabled(False)
        control_layout.addWidget(self.show_result_button)
        
        self.save_result_button = QPushButton(tr('btn_save_results'))
        self.save_result_button.clicked.connect(self._save_results)
        self.save_result_button.setEnabled(False)
        control_layout.addWidget(self.save_result_button)
        
        self.save_fig_button = QPushButton(tr('btn_save_figure'))
        self.save_fig_button.clicked.connect(self._save_figure)
        self.save_fig_button.setEnabled(False)
        control_layout.addWidget(self.save_fig_button)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        self.fig = Figure(figsize=(14, 6), dpi=100)
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3, left=0.1, bottom=0.15, right=0.95, top=0.95)
        self.axes = self.fig.subplots(1, 2)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.result_table = QTableView()
        self.result_table.setSortingEnabled(True)
        layout.addWidget(QLabel(tr('label_results')))
        layout.addWidget(self.result_table)
        
        self.ref_text = QTextEdit()
        self.ref_text.setReadOnly(True)
        self.ref_text.setMaximumHeight(60)
        self.ref_text.setText(REFERENCE)
        layout.addWidget(self.ref_text)
    
    def _calculate(self):
        if self.df.empty:
            QMessageBox.warning(self, tr('msg_warning'), tr('msg_no_data'))
            return
        
        try:
            self.result_df, self.plot_data = self.calculator.calculate(self.df)
            
            if self.result_df.empty:
                QMessageBox.warning(self, tr('msg_warning'), tr('msg_zircon_ce_no_result'))
                return
            
            self.result_table.setModel(PandasModel(self.result_df))
            
            self._plot_results()
            
            self.show_result_button.setEnabled(True)
            self.save_result_button.setEnabled(True)
            self.save_fig_button.setEnabled(True)
            
            QMessageBox.information(self, tr('msg_success'), 
                                   tr('msg_zircon_ce_calc_success').format(len(self.result_df)))
            
        except ValueError as e:
            QMessageBox.warning(self, tr('msg_warning'), str(e))
        except Exception as e:
            QMessageBox.critical(self, tr('msg_error'), f"Calculation failed:\n{str(e)}")
    
    def _plot_results(self):
        for ax in self.axes:
            ax.clear()
        
        xlabel = r'$(r_i/3+r_{Zr}/6)(r_i-r_{Zr})^2$'
        ylabel = r'$\log_e D_{Zircon/Base}$'
        
        for ax in self.axes:
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        
        if self.plot_data.get('scatter3'):
            for i, (x_data, y_data) in enumerate(self.plot_data['scatter3']):
                valid_x = [x for x, y in zip(x_data, y_data) if not np.isnan(y)]
                valid_y = [y for y in y_data if not np.isnan(y)]
                if valid_x and valid_y:
                    self.axes[0].scatter(valid_x, valid_y, s=10, color='blue', alpha=0.3)
            
            if self.plot_data.get('labels3') and len(self.plot_data['labels3']) > 0:
                x_data, y_data, elements = self.plot_data['labels3'][0]
                for k, (x, y) in enumerate(zip(x_data, y_data)):
                    if not np.isnan(y):
                        self.axes[0].annotate(elements[k], xy=(x, y), fontsize=6, 
                                            xytext=(8, 8), textcoords='offset points',
                                            ha='right', va='bottom',
                                            bbox=dict(boxstyle='round,pad=0.2', fc='blue', alpha=0.3),
                                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            if self.plot_data.get('line3'):
                for xline, yline in self.plot_data['line3']:
                    self.axes[0].plot(xline, yline, 'b-', alpha=0.3)
        
        if self.plot_data.get('scatter4'):
            for i, (x_data, y_data) in enumerate(self.plot_data['scatter4']):
                valid_x = [x for x, y in zip(x_data, y_data) if not np.isnan(y)]
                valid_y = [y for y in y_data if not np.isnan(y)]
                if valid_x and valid_y:
                    self.axes[1].scatter(valid_x, valid_y, s=10, color='red', alpha=0.3)
            
            if self.plot_data.get('labels4') and len(self.plot_data['labels4']) > 0:
                x_data, y_data, elements = self.plot_data['labels4'][0]
                for k, (x, y) in enumerate(zip(x_data, y_data)):
                    if not np.isnan(y):
                        self.axes[1].annotate(elements[k], xy=(x, y), fontsize=6,
                                            xytext=(8, 8), textcoords='offset points',
                                            ha='right', va='bottom',
                                            bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=0.3),
                                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            if self.plot_data.get('line4'):
                for xline, yline in self.plot_data['line4']:
                    self.axes[1].plot(xline, yline, 'r-', alpha=0.3)
        
        self.axes[0].set_title('REE3+ Partitioning')
        self.axes[1].set_title('4+ Cations Partitioning')
        
        self.canvas.draw()
    
    def _show_result(self):
        if self.result_df.empty:
            QMessageBox.warning(self, tr('msg_warning'), tr('msg_no_results'))
            return
        
        from ..ui.table_viewer import TableViewer
        self.table_viewer = TableViewer(df=self.result_df, title='Zircon Ce4+/Ce3+ Results')
        self.table_viewer.show()
    
    def _save_results(self):
        if self.result_df.empty:
            QMessageBox.warning(self, tr('msg_warning'), tr('msg_no_results'))
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, tr('dialog_save_zircon_ce'), "",
            f"{tr('filter_excel')};;{tr('filter_csv')}"
        )
        
        if filepath:
            try:
                if filepath.endswith('.csv'):
                    self.result_df.to_csv(filepath, index=False, encoding='utf-8')
                else:
                    self.result_df.to_excel(filepath, index=False, engine='openpyxl')
                
                QMessageBox.information(self, tr('msg_success'), f"{tr('msg_save_success')} {filepath}")
            except Exception as e:
                QMessageBox.critical(self, tr('msg_error'), f"Failed to save: {str(e)}")
    
    def _save_figure(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, tr('dialog_save_figure'), "",
            "PDF Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)"
        )
        
        if filepath:
            try:
                self.fig.savefig(filepath, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, tr('msg_success'), f"{tr('msg_save_success')} {filepath}")
            except Exception as e:
                QMessageBox.critical(self, tr('msg_error'), f"Failed to save figure: {str(e)}")
    
    def update_data(self, df):
        self.df = df
        if not self.df.empty:
            self._calculate()
