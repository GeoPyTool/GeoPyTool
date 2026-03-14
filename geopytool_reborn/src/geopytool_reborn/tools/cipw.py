# -*- coding: utf-8 -*-
"""
CIPW Norm Calculation Module

Implements the CIPW normative calculation for igneous rocks.
After calculation, results can be plotted on QAPF diagram.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTabWidget, QTableView, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt

from ..core.data_model import PandasModel


class CIPWCalculator:
    """
    CIPW Normative Calculation Engine.
    
    Calculates mineral norms from major element chemistry.
    """
    
    MINERALS = [
        'Quartz', 'Zircon', 'K2SiO3', 'Anorthite', 'Na2SiO3',
        'Acmite', 'Diopside', 'Sphene', 'Hypersthene', 'Albite',
        'Orthoclase', 'Wollastonite', 'Olivine', 'Perovskite',
        'Nepheline', 'Leucite', 'Larnite', 'Kalsilite', 'Apatite',
        'Halite', 'Fluorite', 'Anhydrite', 'Thenardite', 'Pyrite',
        'Magnesiochromite', 'Chromite', 'Ilmenite', 'Calcite',
        'Na2CO3', 'Corundum', 'Rutile', 'Magnetite', 'Hematite',
        'Q', 'A', 'P', 'F'
    ]
    
    CALC_PARAMS = [
        'Fe3+/(Total Fe) in rock (Mole)',
        'Mg/(Mg+Total Fe) in rock (Mole)',
        'Mg/(Mg+Fe2+) in rock (Mole)',
        'Mg/(Mg+Fe2+) in silicates',
        'Ca/(Ca+Na) in rock (Mole)',
        'Plagioclase An content',
        'Differentiation Index'
    ]
    
    OXIDES = [
        'SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 'MgO',
        'CaO', 'Na2O', 'K2O', 'P2O5', 'CO2', 'SO3', 'S', 'F',
        'Cl', 'Sr', 'Ba', 'Ni', 'Cr', 'Zr'
    ]
    
    MINERAL_MASS = {
        'Quartz': 60.084, 'Zircon': 183.31, 'Orthoclase': 278.336,
        'Albite': 262.247, 'Anorthite': 278.223, 'Diopside': 216.559,
        'Hypersthene': 100.389, 'Olivine': 140.708, 'Wollastonite': 116.16,
        'Apatite': 504.3, 'Halite': 58.44, 'Fluorite': 78.08,
        'Corundum': 101.96, 'K2SiO3': 154.28, 'Na2SiO3': 122.07,
        'Ilmenite': 151.73, 'Magnetite': 231.54, 'Hematite': 159.69,
        'Nepheline': 142.06, 'Leucite': 218.24, 'Q': 60.084,
        'A': 278.336, 'P': 278.223, 'F': 142.06
    }
    
    MINERAL_DENSITY = {
        'Quartz': 2.65, 'Zircon': 4.68, 'Orthoclase': 2.56,
        'Albite': 2.62, 'Anorthite': 2.76, 'Diopside': 3.28,
        'Hypersthene': 3.4, 'Olivine': 3.35, 'Wollastonite': 2.9,
        'Apatite': 3.15, 'Halite': 2.17, 'Fluorite': 3.18,
        'Corundum': 3.98, 'K2SiO3': 2.5, 'Na2SiO3': 2.5,
        'Ilmenite': 4.7, 'Magnetite': 5.2, 'Hematite': 5.3,
        'Nepheline': 2.6, 'Leucite': 2.48, 'Q': 2.65,
        'A': 2.56, 'P': 2.76, 'F': 2.6
    }
    
    OXIDE_MASS = {
        'SiO2': 60.084, 'TiO2': 79.8988, 'Al2O3': 101.961,
        'Fe2O3': 159.69, 'FeO': 71.846, 'MnO': 70.937,
        'MgO': 40.304, 'CaO': 56.079, 'Na2O': 61.979,
        'K2O': 94.196, 'P2O5': 141.945, 'CO2': 44.01,
        'SO3': 80.066, 'S': 32.065, 'F': 19.0,
        'Cl': 35.453, 'Sr': 87.62, 'Ba': 137.327,
        'Ni': 58.6934, 'Cr': 51.9961, 'Zr': 91.224
    }
    
    def calculate_single(self, row: Dict) -> Tuple[Dict, Dict, Dict, Dict]:
        """
        Calculate CIPW norm for a single sample.
        
        Args:
            row: Dictionary with oxide values and styling attributes
            
        Returns:
            tuple: (mole_result, weight_result, volume_result, calc_result)
        """
        mole_result = self._init_result_dict(row, ' Mole%')
        weight_result = self._init_result_dict(row, ' Weight%')
        volume_result = self._init_result_dict(row, ' Volume%')
        calc_result = self._init_result_dict(row, '')
        
        elements = self._get_element_moles(row)
        if not elements:
            return mole_result, weight_result, volume_result, calc_result
        
        Fe3, Fe2, Mg, Ca, Na = elements['Fe2O3'], elements['FeO'], elements['MgO'], elements['CaO'], elements['Na2O']
        
        try:
            calc_result['Fe3+/(Total Fe) in rock (Mole)'] = 100 * Fe3 * 2 / (Fe3 * 2 + Fe2) if (Fe3 * 2 + Fe2) > 0 else 0
        except ZeroDivisionError:
            calc_result['Fe3+/(Total Fe) in rock (Mole)'] = 0
        
        try:
            calc_result['Mg/(Mg+Total Fe) in rock (Mole)'] = 100 * Mg / (Mg + Fe3 * 2 + Fe2) if (Mg + Fe3 * 2 + Fe2) > 0 else 0
        except ZeroDivisionError:
            calc_result['Mg/(Mg+Total Fe) in rock (Mole)'] = 0
        
        try:
            calc_result['Mg/(Mg+Fe2+) in rock (Mole)'] = 100 * Mg / (Mg + Fe2) if (Mg + Fe2) > 0 else 0
        except ZeroDivisionError:
            calc_result['Mg/(Mg+Fe2+) in rock (Mole)'] = 0
        
        try:
            calc_result['Ca/(Ca+Na) in rock (Mole)'] = 100 * Ca / (Ca + Na * 2) if (Ca + Na * 2) > 0 else 0
        except ZeroDivisionError:
            calc_result['Ca/(Ca+Na) in rock (Mole)'] = 0
        
        minerals = self._calculate_minerals(elements)
        
        for mineral, value in minerals['mole'].items():
            mole_result[mineral] = round(value * 100, 4)
        
        for mineral, value in minerals['weight'].items():
            weight_result[mineral] = round(value, 4)
        
        for mineral, value in minerals['volume'].items():
            volume_result[mineral] = round(value, 4)
        
        return mole_result, weight_result, volume_result, calc_result
    
    def _init_result_dict(self, row: Dict, suffix: str) -> Dict:
        """Initialize result dictionary with styling attributes."""
        result = {}
        label = str(row.get('Label', ''))
        result['Label'] = label + suffix if label else ''
        for attr in ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker']:
            result[attr] = row.get(attr, {'Width': 1, 'Style': '-', 'Alpha': 0.5, 
                                          'Size': 10, 'Color': 'black', 'Marker': 'o'}[attr])
        return result
    
    def _get_element_moles(self, row: Dict) -> Optional[Dict]:
        """Calculate mole percentages for each element."""
        elements = {}
        total_mass = 0
        
        for oxide in self.OXIDES:
            value = row.get(oxide, 0)
            try:
                total_mass += float(value)
            except (ValueError, TypeError):
                pass
        
        if total_mass == 0:
            return None
        
        weight_correction = 100 / total_mass
        
        for oxide in self.OXIDES:
            value = row.get(oxide, 0)
            
            try:
                mole = float(value) / self.OXIDE_MASS.get(oxide, 1) * weight_correction
                elements[oxide] = mole
            except (ValueError, TypeError):
                elements[oxide] = 0
        
        return elements
    
    def _calculate_minerals(self, elements: Dict) -> Dict:
        """Calculate mineral proportions from element moles."""
        calc = elements.copy()
        
        if calc['CaO'] >= 10/3 * calc.get('P2O5', 0):
            calc['CaO'] -= 10/3 * calc.get('P2O5', 0)
        else:
            calc['CaO'] = 0
        
        apatite = calc.get('P2O5', 0) / 1.5
        halite = calc.get('Cl', 0)
        
        if calc.get('Na2O', 0) >= calc.get('Cl', 0):
            calc['Na2O'] -= calc.get('Cl', 0)
        else:
            calc['Na2O'] = 0
        
        if calc.get('CaO', 0) >= 0.5 * calc.get('F', 0):
            calc['CaO'] -= 0.5 * calc.get('F', 0)
        else:
            calc['CaO'] = 0
        
        fluorite = calc.get('F', 0) * 0.5
        
        quartz = calc.get('SiO2', 0)
        zircon = calc.get('Zr', 0)
        quartz -= zircon
        
        orthoclase = min(calc.get('K2O', 0), calc.get('Al2O3', 0))
        k2sio3 = max(0, calc.get('K2O', 0) - calc.get('Al2O3', 0))
        al2o3_remaining = calc.get('Al2O3', 0) - orthoclase
        
        albite = min(calc.get('Na2O', 0), al2o3_remaining)
        na2sio3 = max(0, calc.get('Na2O', 0) - al2o3_remaining)
        al2o3_remaining -= albite
        
        anorthite = min(calc.get('CaO', 0), al2o3_remaining)
        al2o3_remaining -= anorthite
        corundum = al2o3_remaining
        
        cao_remaining = calc.get('CaO', 0) - anorthite
        
        diopside = min(cao_remaining, calc.get('FeO', 0) + calc.get('MgO', 0))
        cao_remaining -= diopside
        wollastonite = cao_remaining
        
        hypersthene = calc.get('FeO', 0) + calc.get('MgO', 0) - diopside
        
        quartz = quartz - orthoclase * 6 - albite * 6 - anorthite * 2 - diopside * 2 - wollastonite
        
        if quartz < 0:
            olivine = abs(quartz) / 2
            hypersthene -= olivine
            quartz = 0
        else:
            olivine = 0
        
        nepheline = 0
        if quartz < 0 and albite > 0:
            nepheline = min(-quartz / 4, albite)
            albite -= nepheline
            quartz = 0
        
        Q = max(0, quartz)
        A = orthoclase
        P = anorthite + albite
        F = nepheline
        
        mole_result = {
            'Quartz': quartz, 'Zircon': zircon, 'Orthoclase': orthoclase,
            'Albite': albite, 'Anorthite': anorthite, 'Diopside': diopside,
            'Hypersthene': hypersthene, 'Olivine': olivine, 'Wollastonite': wollastonite,
            'Apatite': apatite, 'Halite': halite, 'Fluorite': fluorite,
            'Corundum': corundum, 'K2SiO3': k2sio3, 'Na2SiO3': na2sio3,
            'Nepheline': nepheline, 'Q': Q, 'A': A, 'P': P, 'F': F
        }
        
        weight_result = {}
        volume_result = {}
        
        for mineral, mole_val in mole_result.items():
            mass = self.MINERAL_MASS.get(mineral, 1)
            density = self.MINERAL_DENSITY.get(mineral, 1)
            weight_result[mineral] = mole_val * mass
            volume_result[mineral] = mole_val * mass / density if density > 0 else 0
        
        return {'mole': mole_result, 'weight': weight_result, 'volume': volume_result}


class CIPWWindow(QWidget):
    """
    CIPW Norm Calculation Window.
    
    Provides interface for calculating and viewing CIPW norms.
    Can open QAPF diagram with calculated results.
    """
    
    title = "CIPW Norm Calculation"
    items_to_check = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 
                      'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.title)
        self.df = df
        self.parent_window = parent
        self.calculator = CIPWCalculator()
        
        self.mole_results = []
        self.weight_results = []
        self.volume_results = []
        self.calc_results = []
        self.qapf_df = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        control_layout = QHBoxLayout()
        
        self.calc_button = QPushButton("Calculate CIPW Norm")
        self.calc_button.clicked.connect(self._calculate)
        control_layout.addWidget(self.calc_button)
        
        self.qapf_button = QPushButton("Open QAPF Diagram")
        self.qapf_button.clicked.connect(self._open_qapf)
        self.qapf_button.setEnabled(False)
        control_layout.addWidget(self.qapf_button)
        
        self.save_button = QPushButton("Save Results")
        self.save_button.clicked.connect(self._save_results)
        control_layout.addWidget(self.save_button)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        self.tabs = QTabWidget()
        
        self.mole_table = QTableView()
        self.mole_table.setSortingEnabled(True)
        self.weight_table = QTableView()
        self.weight_table.setSortingEnabled(True)
        self.volume_table = QTableView()
        self.volume_table.setSortingEnabled(True)
        self.calc_table = QTableView()
        self.calc_table.setSortingEnabled(True)
        
        self.tabs.addTab(self.mole_table, "Mole %")
        self.tabs.addTab(self.weight_table, "Weight %")
        self.tabs.addTab(self.volume_table, "Volume %")
        self.tabs.addTab(self.calc_table, "Calculated Parameters")
        
        layout.addWidget(self.tabs)
    
    def _calculate(self):
        if self.df.empty:
            QMessageBox.warning(self, "Warning", "No data to calculate.")
            return
        
        self.mole_results = []
        self.weight_results = []
        self.volume_results = []
        self.calc_results = []
        
        for i in range(len(self.df)):
            row = self.df.iloc[i].to_dict()
            try:
                mole, weight, volume, calc = self.calculator.calculate_single(row)
                self.mole_results.append(mole)
                self.weight_results.append(weight)
                self.volume_results.append(volume)
                self.calc_results.append(calc)
            except Exception as e:
                print(f"Error calculating row {i}: {e}")
        
        if self.mole_results:
            mole_df = pd.DataFrame(self.mole_results)
            weight_df = pd.DataFrame(self.weight_results)
            volume_df = pd.DataFrame(self.volume_results)
            calc_df = pd.DataFrame(self.calc_results)
            
            self.mole_table.setModel(PandasModel(mole_df))
            self.weight_table.setModel(PandasModel(weight_df))
            self.volume_table.setModel(PandasModel(volume_df))
            self.calc_table.setModel(PandasModel(calc_df))
            
            self._prepare_qapf_data()
            
            self.qapf_button.setEnabled(True)
            
            QMessageBox.information(self, "Success", f"Calculated CIPW norms for {len(self.mole_results)} samples.")
    
    def _prepare_qapf_data(self):
        """Prepare QAPF data from CIPW results."""
        if not self.weight_results:
            return
        
        qapf_data = []
        
        for i, result in enumerate(self.weight_results):
            Q = result.get('Q', 0)
            A = result.get('A', 0)
            P = result.get('P', 0)
            F = result.get('F', 0)
            
            row_data = {
                'Label': result.get('Label', f'Sample {i+1}'),
                'Q': Q,
                'A': A,
                'P': P,
                'F': F,
                'Color': self.df.iloc[i].get('Color', 'red') if i < len(self.df) else 'red',
                'Marker': self.df.iloc[i].get('Marker', 'o') if i < len(self.df) else 'o',
                'Size': self.df.iloc[i].get('Size', 40) if i < len(self.df) else 40,
                'Alpha': self.df.iloc[i].get('Alpha', 0.7) if i < len(self.df) else 0.7
            }
            qapf_data.append(row_data)
        
        self.qapf_df = pd.DataFrame(qapf_data)
    
    def _open_qapf(self):
        """Open QAPF diagram with calculated data."""
        if self.qapf_df is None or self.qapf_df.empty:
            QMessageBox.warning(self, "Warning", "Calculate CIPW first.")
            return
        
        try:
            from ..diagrams.triangular.qapf import QAPF
            
            qapf_window = QAPF(df=self.qapf_df, parent=self.parent_window)
            qapf_window.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open QAPF diagram:\n{str(e)}")
    
    def _save_results(self):
        if not self.mole_results:
            QMessageBox.warning(self, "Warning", "No results to save. Calculate first.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save CIPW Results", "", "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        
        if filepath:
            try:
                mole_df = pd.DataFrame(self.mole_results)
                weight_df = pd.DataFrame(self.weight_results)
                volume_df = pd.DataFrame(self.volume_results)
                calc_df = pd.DataFrame(self.calc_results)
                
                if filepath.endswith('.csv'):
                    base = filepath.rsplit('.', 1)[0]
                    mole_df.to_csv(f"{base}_mole.csv", index=False)
                    weight_df.to_csv(f"{base}_weight.csv", index=False)
                    volume_df.to_csv(f"{base}_volume.csv", index=False)
                    calc_df.to_csv(f"{base}_calc.csv", index=False)
                else:
                    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                        mole_df.to_excel(writer, sheet_name='Mole%', index=False)
                        weight_df.to_excel(writer, sheet_name='Weight%', index=False)
                        volume_df.to_excel(writer, sheet_name='Volume%', index=False)
                        calc_df.to_excel(writer, sheet_name='Parameters', index=False)
                
                QMessageBox.information(self, "Success", f"Results saved to {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def update_data(self, df):
        self.df = df