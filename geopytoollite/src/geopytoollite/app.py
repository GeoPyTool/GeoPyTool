"""
A Lite version of GeoPyTool
"""

import importlib.metadata
import sys

import sys
import os
import math
import numpy as np
import pandas as pd
import matplotlib
import platform
from scipy import stats as st
from scipy.optimize import leastsq

# Set Matplotlib backend to generic QtAgg which works with PySide6
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib import path as mpath
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.ft2font as ft2font

import pyqtgraph as pg

# Sklearn imports
try:
    from sklearn import svm
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.preprocessing import LabelEncoder
    from matplotlib.colors import ListedColormap
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                               QMessageBox, QTableView, QSplitter, QListWidget,
                               QStackedWidget, QFrame, QCheckBox, QSlider, 
                               QLineEdit, QSizePolicy, QHeaderView, QAbstractItemView,
                               QTextEdit, QComboBox, QScrollArea, QGridLayout, QDialog)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal, QSize
from PySide6.QtGui import QAction, QIcon, QColor, QFont, QPalette, QActionGroup
from PySide6.QtWidgets import QStyle

# ==========================================
# 1. Global Config & Resources
# ==========================================
VERSION = "Lite 1.0 "
DATE = "2026-01-19"
AUTHOR = "GeoPyTool Team"

# ==========================================
# 2. Helpers from CustomClass.py
# ==========================================

class GrowingTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.heightMin = 0
        self.heightMax = 100

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(int(docHeight))

class Tool():
    def CleanDataFile(self, raw=pd.DataFrame(), checklist=['质量', '分数', '百分比', ' ', 'ppm', 'ma', 'wt', '%', '(', ')', '（', '）', '[', ']', '【', '】']):
        for i in checklist:
            raw = raw.rename(columns=lambda x: x.replace(i, ''))

        for i in raw.dtypes.index:
            if raw.dtypes[i] != float and raw.dtypes[i] != int and i not in ['Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width', 'Label'] and i not in getattr(self, 'itemstocheck', []):
                # print(raw.dtypes[i], i, 'dropped')
                raw = raw.drop(i, axis=1)

        for i in raw.columns.values.tolist():
            if i == '':
                raw = raw.drop(i, axis=1)

        raw = raw.dropna(axis=1, how='all')

        for i in raw.index.values.tolist():
            if isinstance(raw.at[i, 'Label'], str):
                if 'tandard' in raw.at[i, 'Label']:
                    # print('Your Self Defined Standard is at the line No.', i)
                    # self.Standard = raw.loc[i] # Need to handle self.Standard if needed
                    raw = raw.drop(i)

        raw = raw.reset_index(drop=True)
        return raw

    def TriToBin(self, x, y, z):
        if (z >= 0):
            if (x + y + z == 0): return (0, 0)
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if (X + Y != 0):
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * (np.sqrt(3))
            return (a, b)
        else:
            z = abs(z)
            if (x + y + z == 0): return (0, 0)
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if (X + Y != 0):
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * (np.sqrt(3))
            return (a, -b)

    def BinToTri(self, a, b):
        if (b >= 0):
            y = a - b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a + b / np.sqrt(3))
            return (x, y, z)
        else:
            y = a + b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a - b / np.sqrt(3))
            return (x, y, z)

    def TriCross(self, A=[(100, 0, 0), (0, 50, 60)], B=[(50, 50, 0), (0, 0, 100)]):
        x0, y0 = self.TriToBin(A[0][0], A[0][1], A[0][2])
        x1, y1 = self.TriToBin(A[1][0], A[1][1], A[1][2])
        x2, y2 = self.TriToBin(B[0][0], B[0][1], B[0][2])
        x3, y3 = self.TriToBin(B[1][0], B[1][1], B[1][2])

        if (x1 - x0) == 0: b1 = 1e9
        else: b1 = (y1 - y0) / (x1 - x0)
        
        if (x3 - x2) == 0: b2 = 1e9
        else: b2 = (y3 - y2) / (x3 - x2)
        
        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        if (b1 - b2) == 0: x = 0
        else: x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        result = self.BinToTri(x, y)
        return (result)

class Point():
    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        self.X = X
        self.Y = Y
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

class Tag():
    def __init__(self, Label=u'Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=8):
        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class Line():
    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label
        self.Points = Points
        if (len(Points) == 2):
            self.X = [Points[0][0], Points[1][0]]
            self.Y = [Points[0][1], Points[1][1]]
        elif (len(Points) > 2):
            self.X = [p[0] for p in Points]
            self.Y = [p[1] for p in Points]

class TriPoint(Point, Tool):
    def __init__(self, P=(10, 20, 70), Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        Point.__init__(self, Size=Size, Color=Color, Alpha=Alpha, Marker=Marker, Label=Label)
        self.sum = P[0] + P[1] + abs(P[2])
        if self.sum == 0: self.sum = 1
        self.x = P[0] * 100 / self.sum
        self.y = P[1] * 100 / self.sum
        self.z = P[2] * 100 / self.sum
        self.Location = P
        self.X, self.Y = self.TriToBin(self.x, self.y, self.z)

class TriLine(Line, Tool):
    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
        Line.__init__(self, Sort=Sort, Width=Width, Color=Color, Style=Style, Alpha=Alpha, Label=Label)
        self.x = []
        self.y = []
        self.z = []
        self.Points = Points
        for i in Points:
            self.x.append(i[0])
            self.y.append(i[1])
            self.z.append(i[2])
        self.tritrans()

    def tritrans(self):
        self.X = []
        self.Y = []
        for i in range(len(self.x)):
            self.X.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[0])
            self.Y.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[1])

# ==========================================
# 3. Data Models
# ==========================================

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._df = df

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole: return None
        if orientation == Qt.Horizontal:
            try: return self._df.columns.tolist()[section]
            except: return None
        elif orientation == Qt.Vertical:
            try: return str(self._df.index.tolist()[section])
            except: return None
        return None

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if not index.isValid(): return None
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def rowCount(self, parent=QModelIndex()): return len(self._df.index)
    def columnCount(self, parent=QModelIndex()): return len(self._df.columns)

class TableViewer(QDialog):
    def __init__(self, df=pd.DataFrame(), title='Result', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)
        self.df = df
        
        layout = QVBoxLayout(self)
        
        # Controls
        hbox = QHBoxLayout()
        self.btn_save = QPushButton("Save Data")
        self.btn_save.clicked.connect(self.save_data)
        hbox.addWidget(self.btn_save)
        hbox.addStretch()
        layout.addLayout(hbox)
        
        # Table
        self.table = CustomQTableView()
        self.table.setModel(PandasModel(self.df))
        layout.addWidget(self.table)
        
    def save_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if filename:
            try:
                if filename.endswith('.csv'):
                    self.df.to_csv(filename, index=True)
                else:
                    self.df.to_excel(filename, index=True)
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    
    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class CustomQTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setStretchLastSection(True)

# ==========================================
# 4. Base Plot Window
# ==========================================

class BasePlotWindow(QWidget, Tool):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.df = df
        self.itemstocheck = []
        self.dpi = 100
        self.fig = Figure((10.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.mpl_toolbar)
        self.main_layout.addWidget(self.canvas)
        
        self.control_layout = QHBoxLayout()
        self.main_layout.addLayout(self.control_layout)
        
        self.info_box = GrowingTextEdit()
        self.info_box.setReadOnly(True)
        self.main_layout.addWidget(self.info_box)

    def update_data(self, df):
        self.df = self.clean_data(df)
        self.plot()

    def plot(self): pass

    def clean_data(self, df):
        if df.empty: return df
        # Use robust cleaning from Tool (original CleanDataFile logic)
        df_clean = self.CleanDataFile(df.copy())
        
        # Ensure styling columns exist (needed for this app's plotting)
        if 'Marker' not in df_clean.columns: df_clean['Marker'] = 'o'
        if 'Color' not in df_clean.columns: df_clean['Color'] = 'red'
        if 'Size' not in df_clean.columns: df_clean['Size'] = 20
        if 'Alpha' not in df_clean.columns: df_clean['Alpha'] = 0.7
        if 'Label' not in df_clean.columns: df_clean['Label'] = ''
        if 'Width' not in df_clean.columns: df_clean['Width'] = 1
        if 'Style' not in df_clean.columns: df_clean['Style'] = '-'
        return df_clean

    def plot_points(self, ax, x_col, y_col, df=None):
        if df is None: df = self.df
        if df.empty: return
        
        seen_labels = set()
        
        # Determine if this is the first plot to handle labels for figure-wide legend
        # This helper is generic, so we rely on the caller to manage legends usually.
        # But for Harker, we passed 'Linear' etc only for i==0.
        # Here we can just plot everything. The caller (HarkerWindow) will extract handles from ax[0].
        
        for idx, row in df.iterrows():
            # Get values safely
            try:
                x = row.get(x_col)
                y = row.get(y_col)
                if pd.isna(x) or pd.isna(y): continue
                
                lbl = str(row.get('Label', ''))
                # For Harker (and others), we want to tag data points so they appear in the legend
                # We simply use the label. Duplicates are handled by Matplotlib automatically if we want
                # BUT we want to filter them to avoid "Label, Label, Label" in the legend list.
                # So we use seen_labels logic locally for this axis.
                
                if not lbl or lbl in seen_labels:
                    final_label = "_nolegend_"
                else:
                    final_label = lbl
                    seen_labels.add(lbl)
                
                ax.scatter(x, y, 
                           label=final_label,
                           marker=row.get('Marker', 'o'),
                           c=row.get('Color', 'red'),
                           s=row.get('Size', 20),
                           alpha=row.get('Alpha', 0.7),
                           edgecolors='none')
            except Exception as e:
                pass

# ==========================================
# 5. Modules
# ==========================================

class TASWindow(BasePlotWindow):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.itemstocheck = ['SiO2', 'Na2O', 'K2O']
        self.axes = self.fig.add_subplot(111)
        self.cb_regions = QCheckBox("Show Fields"); self.cb_regions.setChecked(True); self.cb_regions.stateChanged.connect(self.plot)
        self.cb_irvine = QCheckBox("Irvine Line"); self.cb_irvine.setChecked(True); self.cb_irvine.stateChanged.connect(self.plot)
        self.cb_mode = QComboBox(); self.cb_mode.addItems(["Volcanic", "Plutonic"]); self.cb_mode.currentIndexChanged.connect(self.plot)
        self.control_layout.addWidget(QLabel("Mode:")); self.control_layout.addWidget(self.cb_mode)
        self.control_layout.addWidget(self.cb_regions); self.control_layout.addWidget(self.cb_irvine)
        self.control_layout.addStretch()
        self.info_box.setText("TAS Diagram (Total Alkali-Silica) - Wilson et al. 1989")
        self.fields = [
            ([[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]], "F"),
            ([[41, 0], [41, 3], [45, 3], [45, 0]], "Pc"),
            ([[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]], "U1"),
            ([[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]], "U2"),
            ([[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]], "U3"),
            ([[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]], "Ph"),
            ([[45, 0], [45, 2], [52, 5], [52, 0]], "Ba"),
            ([[45, 2], [45, 5], [52, 5]], "Bs"),
            ([[45, 5], [49.4, 7.3], [52, 5]], "S1"),
            ([[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]], "S2"),
            ([[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]], "S3"),
            ([[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]], "T"),
            ([[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]], "Td"),
            ([[52, 0], [52, 5], [57, 5.9], [57, 0]], "O1"),
            ([[57, 0], [57, 5.9], [63, 7], [63, 0]], "O2"),
            ([[63, 0], [63, 7], [69, 8], [77.3, 0]], "O3"),
            ([[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]], "R"),
            ([[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]], "Q")
        ]
        self.field_labels_volcanic = {"F": "Foidite", "Pc": "Picrobasalt", "U1": "Tephrite\nBasanite", "U2": "Phono-\ntephrite", "U3": "Tephri-\nphonolite", "Ph": "Phonolite", "Ba": "Alkalic\nBasalt", "Bs": "Subalkalic\nBasalt", "S1": "Trachybasalt", "S2": "Basaltic\nTrachyandesite", "S3": "Trachy-\nandesite", "T": "Trachyte", "Td": "Trachydacite", "O1": "Basaltic\nAndesite", "O2": "Andesite", "O3": "Dacite", "R": "Rhyolite", "Q": "Silexite"}
        self.field_labels_plutonic = {"F": "Foidolite", "Pc": "Peridotgabbro", "U1": "Foid Gabbro", "U2": "Foid\nMonzodiorite", "U3": "Foid\nMonzosyenite", "Ph": "Foid Syenite", "Ba": "Alkalic\nGabbro", "Bs": "Subalkalic\nGabbro", "S1": "Monzogabbro", "S2": "Monzodiorite", "S3": "Monzonite", "T": "Syenite", "Td": "Quartz\nMonzonite", "O1": "Gabbroic\nDiorite", "O2": "Diorite", "O3": "Granodiorite", "R": "Granite", "Q": "Quartzolite"}
        self.field_text_locs = {"F": (39, 10), "Pc": (43, 1.5), "U1": (44, 6), "U2": (47.5, 3.5), "U3": (49.5, 12), "Ph": (55, 16), "Ba": (48, 1), "Bs": (49, 4), "S1": (49, 6), "S2": (53, 7), "S3": (57, 9), "T": (59, 13), "Td": (65, 10), "O1": (54, 2), "O2": (59, 3), "O3": (67, 3), "R": (75, 9), "Q": (85, 2)}

    def Irvine(self, x):
        a = 39.0; b = 3.9492; c = -2.1111; d = 0.86096; e = -0.15188; f = 0.012030; g = -(3.3539 / 10000)
        return(a+ b*np.power(x,1) +c*np.power(x,2) +d*np.power(x,3) +e*np.power(x,4) +f*np.power(x,5) +g*np.power(x,6))

    def plot(self):
        self.axes.clear()
        self.axes.set_xlabel(r'$SiO_2$ (wt%)'); self.axes.set_ylabel(r'$Na_2O + K_2O$ (wt%)')
        self.axes.set_xlim(30, 90); self.axes.set_ylim(0, 20)
        
        # Draw fields
        if self.cb_regions.isChecked():
            is_volcanic = self.cb_mode.currentText() == "Volcanic"
            labels_map = self.field_labels_volcanic if is_volcanic else self.field_labels_plutonic
            for coords, code in self.fields:
                poly = patches.Polygon(coords, closed=True, fill=False, edgecolor='gray', linewidth=1, linestyle='-')
                self.axes.add_patch(poly)
                if code in self.field_text_locs:
                    lx, ly = self.field_text_locs[code]
                    txt = labels_map.get(code, code)
                    self.axes.text(lx, ly, txt, fontsize=8, color='gray', ha='center', va='center')
        
        # Irvine line
        if self.cb_irvine.isChecked():
            y_irvine = np.arange(0, 10.2, 0.1)
            x_irvine = self.Irvine(y_irvine)
            self.axes.plot(x_irvine, y_irvine, color='blue', linewidth=1, linestyle=':', alpha=0.6, label='Irvine & Barragar 1971')
            
        # Plot data
        if not self.df.empty:
            df = self.clean_data(self.df)
            has_sio2 = any(col.lower() == 'sio2' for col in df.columns)
            has_na2o = any(col.lower() == 'na2o' for col in df.columns)
            has_k2o = any(col.lower() == 'k2o' for col in df.columns)
            
            if has_sio2 and has_na2o and has_k2o:
                sio2_col = next(col for col in df.columns if col.lower() == 'sio2')
                na2o_col = next(col for col in df.columns if col.lower() == 'na2o')
                k2o_col = next(col for col in df.columns if col.lower() == 'k2o')
                
                # Temp add sum column for plotting
                df['__sum_alkali__'] = df[na2o_col] + df[k2o_col]
                
                # Use smart plotting
                self.plot_points(self.axes, sio2_col, '__sum_alkali__', df)
                
            else: 
                self.axes.text(0.5, 0.5, "Missing SiO2, Na2O or K2O columns", transform=self.axes.transAxes, ha='center', color='red')
        
        # Legend (Irvine line + Data points)
        self.axes.legend(loc='upper right', fontsize='small', frameon=True)
        self.canvas.draw()

class REEWindow(BasePlotWindow):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.axes = self.fig.add_subplot(111)
        self.elements = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        self.standards = {
            'C1 Chondrite Sun and McDonough,1989': {'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
                                                'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
                                                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
            'Chondrite Taylor and McLennan,1985': {'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
                                               'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
                                               'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381},
            'Chondrite Haskin et al.,1966': {'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185, 'Eu': 0.071,
                                         'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                         'Yb': 0.186, 'Lu': 0.034},
            'Chondrite Nakamura,1977': {'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203, 'Eu': 0.077,
                                    'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                    'Yb': 0.22,
                                    'Lu': 0.034},
            'MORB Sun and McDonough,1989': {'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63, 'Eu': 1.02, 'Gd': 3.68,
                                        'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052, 'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05,
                                        'Lu': 0.46},
            'UCC_Rudnick & Gao2003':{'K':23244.13776,'Ti':3835.794545,'P':654.6310022,'Li':24,'Be':2.1,'B':17,'N':83,'F':557,'S':62,'Cl':370,'Sc':14,'V':97,'Cr':92,
                                 'Co':17.3,'Ni':47,'Cu':28,'Zn':67,'Ga':17.5,'Ge':1.4,'As':4.8,'Se':0.09,
                                 'Br':1.6,'Rb':84,'Sr':320,'Y':21,'Zr':193,'Nb':12,'Mo':1.1,'Ru':0.34,
                                 'Pd':0.52,'Ag':53,'Cd':0.09,'In':0.056,'Sn':2.1,'Sb':0.4,'I':1.4,'Cs':4.9,
                                 'Ba':628,'La':31,'Ce':63,'Pr':7.1,'Nd':27,'Sm':4.7,'Eu':1,'Gd':4,'Tb':0.7,
                                 'Dy':3.9,'Ho':0.83,'Er':2.3,'Tm':0.3,'Yb':1.96,'Lu':0.31,'Hf':5.3,'Ta':0.9,
                                 'W':1.9,'Re':0.198,'Os':0.031,'Ir':0.022,'Pt':0.5,'Au':1.5,'Hg':0.05,'Tl':0.9,
                                 'Pb':17,'Bi':0.16,'Th':10.5,'U':2.7}
        }
        self.combo_standard = QComboBox(); self.combo_standard.addItems(self.standards.keys()); self.combo_standard.currentIndexChanged.connect(self.plot)
        self.cb_legend = QCheckBox("Show Legend"); self.cb_legend.setChecked(True); self.cb_legend.stateChanged.connect(self.plot)
        self.control_layout.addWidget(QLabel("Normalization:")); self.control_layout.addWidget(self.combo_standard)
        self.control_layout.addWidget(self.cb_legend); self.control_layout.addStretch()
        self.info_box.setText("REE Diagram")

    def plot(self):
        self.axes.clear()
        self.axes.set_ylabel('Sample / Standard'); self.axes.set_yscale('log')
        std_name = self.combo_standard.currentText(); std_vals = self.standards[std_name]
        self.axes.set_xticks(range(len(self.elements))); self.axes.set_xticklabels(self.elements)
        if not self.df.empty:
            df = self.clean_data(self.df)
            
            seen_labels = set()
            
            for idx, row in df.iterrows():
                y_vals = []; x_vals = []
                for i, el_name in enumerate(self.elements):
                    col = next((c for c in df.columns if c.lower() == el_name.lower()), None)
                    if col and pd.notna(row[col]) and row[col] > 0:
                        y_vals.append(row[col] / std_vals.get(el_name, 1)); x_vals.append(i)
                if y_vals:
                    # Smart Legend Logic
                    lbl = str(row.get('Label', ''))
                    if not lbl or lbl in seen_labels:
                        final_label = "_nolegend_"
                    else:
                        final_label = lbl
                        seen_labels.add(lbl)
                    
                    self.axes.plot(x_vals, y_vals, marker='o', markersize=4, color=row.get('Color','black'), label=final_label, alpha=0.7)
            
            if self.cb_legend.isChecked() and seen_labels: 
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                self.fig.subplots_adjust(right=0.7)
            else: 
                self.fig.subplots_adjust(right=0.9)
        self.canvas.draw()

class TraceWindow(BasePlotWindow):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.axes = self.fig.add_subplot(111)
        
        # Element Sets
        self.elements_36 = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                            u'Pr', u'Mo', u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti',
                            u'Gd', u'Tb', u'Dy', u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
                            
        self.elements_26 = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd',
                            u'Zr', u'Hf', u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
        
        self.elements = self.elements_36  # Default

        self.standards = {
            'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
                   'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
                   'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
                   'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.736, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
                   'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
            'OIB': {'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                    'K': 12000, 'La': 36, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                    'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200,
                    'Gd': 7.62,
                    'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16,
                    'Lu': 0.3},
            'EMORB': {'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                      'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155,
                      'P': 620,
                      'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                      'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                      'Yb': 2.36, 'Lu': 0.354},
            'C1': {'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
                   'Ta': 0.014, 'K': 545, 'La': 0.236, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
                   'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
                   'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0364, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
                   'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
            'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                      'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90,
                      'P': 510,
                      'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01,
                      'Ti': 7600,
                      'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                      'Yb': 3.05, 'Lu': 0.455},
            'UCC_Rudnick & Gao2003': {'K': 23244.13676, 'Ti': 3835.794545, 'P': 654.6310022, 'Li': 24, 'Be': 2.1,
                                      'B': 17, 'N': 83, 'F': 557, 'S': 62, 'Cl': 360, 'Sc': 14, 'V': 97, 'Cr': 92,
                                      'Co': 17.3, 'Ni': 47, 'Cu': 28, 'Zn': 67, 'Ga': 17.5, 'Ge': 1.4, 'As': 4.8,
                                      'Se': 0.09,
                                      'Br': 1.6, 'Rb': 84, 'Sr': 320, 'Y': 21, 'Zr': 193, 'Nb': 12, 'Mo': 1.1,
                                      'Ru': 0.34,
                                      'Pd': 0.52, 'Ag': 53, 'Cd': 0.09, 'In': 0.056, 'Sn': 2.1, 'Sb': 0.4, 'I': 1.4,
                                      'Cs': 4.9,
                                      'Ba': 628, 'La': 31, 'Ce': 63, 'Pr': 7.1, 'Nd': 27, 'Sm': 4.7, 'Eu': 1, 'Gd': 4,
                                      'Tb': 0.7,
                                      'Dy': 3.9, 'Ho': 0.83, 'Er': 2.3, 'Tm': 0.3, 'Yb': 1.96, 'Lu': 0.31, 'Hf': 5.3,
                                      'Ta': 0.9,
                                      'W': 1.9, 'Re': 0.198, 'Os': 0.031, 'Ir': 0.022, 'Pt': 0.5, 'Au': 1.5,
                                      'Hg': 0.05, 'Tl': 0.9,
                                      'Pb': 17, 'Bi': 0.16, 'Th': 10.5, 'U': 2.7}
        }
        
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Cs-Lu (36 Elements)", "Rb-Lu (26 Elements)"])
        self.combo_type.currentIndexChanged.connect(self.change_type)
        
        self.combo_standard = QComboBox()
        self.combo_standard.addItems(self.standards.keys())
        self.combo_standard.currentIndexChanged.connect(self.plot)
        
        self.control_layout.addWidget(QLabel("Type:")); self.control_layout.addWidget(self.combo_type)
        self.control_layout.addWidget(QLabel("Normalization:")); self.control_layout.addWidget(self.combo_standard)
        self.control_layout.addStretch()
        self.info_box.setText("Trace Element Spider Diagram")

    def change_type(self):
        if self.combo_type.currentIndex() == 0:
            self.elements = self.elements_36
        else:
            self.elements = self.elements_26
        self.plot()

    def plot(self):
        self.axes.clear()
        self.axes.set_ylabel('Sample / Standard'); self.axes.set_yscale('log')
        std_name = self.combo_standard.currentText(); std_vals = self.standards[std_name]
        self.axes.set_xticks(range(len(self.elements))); self.axes.set_xticklabels(self.elements, rotation=-45, fontsize=8)
        if not self.df.empty:
            df = self.clean_data(self.df)
            
            seen_labels = set()
            
            for idx, row in df.iterrows():
                y_vals = []; x_vals = []
                for i, el_name in enumerate(self.elements):
                    val = None
                    if el_name in df.columns and pd.notna(row[el_name]): val = row[el_name]
                    elif el_name == 'K' and 'K2O' in df.columns and pd.notna(row['K2O']): val = row['K2O'] * 8301.6
                    elif el_name == 'Ti' and 'TiO2' in df.columns and pd.notna(row['TiO2']): val = row['TiO2'] * 5995
                    if val is not None and val > 0: y_vals.append(val / std_vals.get(el_name, 1)); x_vals.append(i)
                if y_vals:
                    # Smart Legend
                    lbl = str(row.get('Label', ''))
                    if not lbl or lbl in seen_labels:
                        final_label = "_nolegend_"
                    else:
                        final_label = lbl
                        seen_labels.add(lbl)
                    
                    self.axes.plot(x_vals, y_vals, marker='o', markersize=4, color=row.get('Color','black'), label=final_label, alpha=0.7)
            
            # Show legend if we have labels
            if seen_labels:
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                self.fig.subplots_adjust(right=0.7)
            else:
                self.fig.subplots_adjust(right=0.9)
                
        self.canvas.draw()

class PearceWindow(BasePlotWindow):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.itemstocheck = ['Y', 'Yb', 'Nb', 'Rb', 'Ta']
        
        # Classification Data (from original Pearce.py)
        self.LocationAreas = [
            # 0: Y+Nb vs Rb
            [ [[2, 80], [55, 300],[400,2000],[2,2000]],
              [[400, 2000],[55, 300],[51.5,8],[2000,400],[2000,2000]],
              [[2, 80], [55, 300], [51.5, 8], [50, 1],[2,1]],
              [[50, 1],[51.5, 8],[2000,400],[2000,1]] ],
            # 1: Yb+Ta vs Rb
            [ [[0.5, 140], [6, 200], [50, 2000],[0.5,2000]],
              [[50, 2000],[6, 200], [6, 8],[200, 400],[200,2000]],
              [[0.5, 140],[6, 200], [6,8],[6,1],[0.5,1]],
              [[6, 1], [6, 8],[200, 400],[200,1]] ],
            # 2: Y vs Nb
            [ [[1, 2000], [25, 25],[1000, 400],[1000,2000]],
              [[1000,400],[25, 25], [50, 10], [1000, 100]],
              [[40, 1],[50,10], [1000, 100],[1000,1]] ],
            # 3: Yb vs Ta
            [ [[0.55, 20], [3, 2],[0.1, 0.35],[0.1,20]],
              [[0.55, 20], [3, 2], [100,20]],
              [[0.1, 0.35], [3, 2],[5,1],[5,0.05],[0.1,0.05]],
              [[100,20],[3, 2], [5, 1],[100,7]],
              [[5, 0.05], [5, 1],[100,7],[100,0.05]] ]
        ]
        self.ItemNames = [
            ['syn-COLG', 'WPG', 'VAG', 'ORG'],
            ['syn-COLG', 'WPG', 'VAG', 'ORG'],
            ['WPG', 'ORG', 'VAG_or_syn-COLG'],
            ['syn-COLG', 'WPG1', 'VAG','WPG2', 'ORG']
        ]
        
        self.condation = [
            {'xLabel': r'Y+Nb (PPM)', 'yLabel': r'Rb (PPM)', 'xlim': (1, 3000), 'ylim': (1, 3000), 'BaseLines': [[(2, 80), (55, 300)], [(55, 300), (400, 2000)], [(55, 300), (51.5, 8)], [(51.5, 8), (50, 1)], [(51.5, 8), (2000, 400)]], 'Labels': [('syn-COLG', (10, 1000)), ('VAG', (10, 10)), ('WPG', (250, 250)), ('ORG', (1000, 10))]},
            {'xLabel': r'Yb+Ta (PPM)', 'yLabel': r'Rb (PPM)', 'xlim': (0.1, 300), 'ylim': (1, 3000), 'BaseLines': [[(0.5, 140), (6, 200)], [(6, 200), (50, 2000)], [(6, 200), (6, 8)], [(6, 8), (6, 1)], [(6, 8), (200, 400)]], 'Labels': [('syn-COLG', (1, 1000)), ('VAG', (1, 10)), ('WPG', (30, 250)), ('ORG', (100, 10))]},
            {'xLabel': r'Y (PPM)', 'yLabel': r'Nb (PPM)', 'xlim': (1, 3000), 'ylim': (1, 3000), 'BaseLines': [[(1, 2000), (50, 10)], [(40, 1), (50, 10)], [(50, 10), (1000, 100)], [(25, 25), (1000, 400)]], 'Labels': [('syn-COLG', (10, 50)), ('VAG', (10, 100)), ('WPG', (100, 100)), ('ORG', (150, 2))]},
            {'xLabel': r'Yb (PPM)', 'yLabel': r'Ta (PPM)', 'xlim': (0.1, 100), 'ylim': (0.01, 100), 'BaseLines': [[(0.55, 20), (3, 2)], [(0.1, 0.35), (3, 2)], [(3, 2), (5, 1)], [(5, 0.05), (5, 1)], [(5, 1), (100, 7)], [(3, 2), (100, 20)]], 'Labels': [('syn-COLG', (0.5, 1)), ('VAG', (0.5, 0.1)), ('WPG', (5, 10)), ('ORG', (30, 1))]}
        ]
        
        self.btn_export = QPushButton("Export Result")
        self.btn_export.clicked.connect(self.export_result)
        self.control_layout.addWidget(self.btn_export)
        self.control_layout.addStretch()

    def update_data(self, df): 
        if df.empty: return
        self.df = self.CleanDataFile(df.copy())
        self.plot()

    def plot(self):
        self.fig.clear(); axes = self.fig.subplots(2, 2); self.fig.subplots_adjust(hspace=0.3, wspace=0.3)
        for idx, ax in enumerate(axes.flat):
            config = self.condation[idx]
            ax.set_xlabel(config['xLabel']); ax.set_ylabel(config['yLabel']); ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(config['xlim']); ax.set_ylim(config['ylim'])
            ax.set_box_aspect(1)
            for line_coords in config['BaseLines']: ax.plot([p[0] for p in line_coords], [p[1] for p in line_coords], color='black', linewidth=1)
            for label, pos in config['Labels']: ax.text(pos[0], pos[1], label, fontsize=8, color='gray', ha='center')
            
            if not self.df.empty:
                try:
                    df = self.clean_data(self.df)
                    
                    # Prepare temp columns for smart plotting
                    if idx == 0: 
                        df['__x__'] = df['Y'] + df['Nb']
                        df['__y__'] = df['Rb']
                    elif idx == 1: 
                        df['__x__'] = df['Yb'] + df['Ta']
                        df['__y__'] = df['Rb']
                    elif idx == 2: 
                        df['__x__'] = df['Y']
                        df['__y__'] = df['Nb']
                    elif idx == 3: 
                        df['__x__'] = df['Yb']
                        df['__y__'] = df['Ta']
                    
                    self.plot_points(ax, '__x__', '__y__', df)
                    
                except: pass
        
        if not self.df.empty:
            handles, labels = axes.flat[0].get_legend_handles_labels()
            if handles:
                self.fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=4, fontsize='small')
                self.fig.subplots_adjust(top=0.9, hspace=0.4, wspace=0.3)
            else:
                self.fig.subplots_adjust(top=0.95, hspace=0.4, wspace=0.3)

        self.canvas.draw()
        
    def export_result(self):
        if self.df.empty: return
        
        results = []
        for i, row in self.df.iterrows():
            res = {'Label': row.get('Label', '')}
            try:
                # Diagram 0: Y+Nb vs Rb
                res['Type_A'] = self.classify_point(row['Y'] + row['Nb'], row['Rb'], 0)
                # Diagram 1: Yb+Ta vs Rb
                res['Type_B'] = self.classify_point(row['Yb'] + row['Ta'], row['Rb'], 1)
                # Diagram 2: Y vs Nb
                res['Type_C'] = self.classify_point(row['Y'], row['Nb'], 2)
                # Diagram 3: Yb vs Ta
                res['Type_D'] = self.classify_point(row['Yb'], row['Ta'], 3)
            except:
                pass
            results.append(res)
            
        TableViewer(pd.DataFrame(results), "Pearce Classification", self).exec()

    def classify_point(self, x, y, diagram_idx):
        areas = self.LocationAreas[diagram_idx]
        names = self.ItemNames[diagram_idx]
        for i, area_coords in enumerate(areas):
             coords = area_coords + [area_coords[0]]
             p = mpath.Path(coords)
             if p.contains_point((x, y)):
                 return names[i]
        return "Unclassified"

class CIPWWindow(QWidget, Tool):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.df = df
        self.layout = QVBoxLayout(self)
        
        hbox = QHBoxLayout()
        self.btn_calc = QPushButton("Calculate CIPW Norm")
        self.btn_calc.clicked.connect(self.calculate)
        hbox.addWidget(self.btn_calc)
        
        self.btn_save = QPushButton("Save Result")
        self.btn_save.clicked.connect(self.save_result)
        hbox.addWidget(self.btn_save)
        self.layout.addLayout(hbox)
        
        self.tabs = QStackedWidget()
        self.table_mole = CustomQTableView()
        self.table_weight = CustomQTableView()
        
        self.layout.addWidget(QLabel("Weight % Result:"))
        self.layout.addWidget(self.table_weight)
        self.layout.addWidget(QLabel("Mole % Result:"))
        self.layout.addWidget(self.table_mole)
        
        self.res_mole = []
        self.res_weight = []
        self.res_volume = []
        self.res_calced = []
        
        self.DataBase = {'Quartz': [60.0843, 2.65], 'Zircon': [183.3031, 4.56], 'K2SiO3': [154.2803, 2.5], 'Anorthite': [278.2093, 2.76], 'Na2SiO3': [122.0632, 2.4], 'Acmite': [462.0083, 3.6], 'Diopside': [229.0691997, 3.354922069], 'Sphene': [196.0625, 3.5], 'Hypersthene': [112.9054997, 3.507622212], 'Albite': [524.446, 2.62], 'Orthoclase': [556.6631, 2.56], 'Wollastonite': [116.1637, 2.86], 'Olivine': [165.7266995, 3.68429065], 'Perovskite': [135.9782, 4], 'Nepheline': [284.1088, 2.56], 'Leucite': [436.4945, 2.49], 'Larnite': [172.2431, 3.27], 'Kalsilite': [316.3259, 2.6], 'Apatite': [493.3138, 3.2], 'Halite': [66.44245, 2.17], 'Fluorite': [94.0762, 3.18], 'Anhydrite': [136.1376, 2.96], 'Thenardite': [142.0371, 2.68], 'Pyrite': [135.9664, 4.99], 'Magnesiochromite': [192.2946, 4.43], 'Chromite': [223.8366, 5.09], 'Ilmenite': [151.7452, 4.75], 'Calcite': [100.0892, 2.71], 'Na2CO3': [105.9887, 2.53], 'Corundum': [101.9613, 3.98], 'Rutile': [79.8988, 4.2], 'Magnetite': [231.5386, 5.2], 'Hematite': [159.6922, 5.25]}
        self.BaseMass  = {'SiO2': 60.083, 'TiO2': 79.865, 'Al2O3': 101.960077, 'Fe2O3': 159.687, 'FeO': 71.844, 'MnO': 70.937044, 'MgO': 40.304, 'CaO': 56.077000000000005, 'Na2O': 61.978538560000004, 'K2O': 94.1956, 'P2O5': 141.942523996, 'CO2': 44.009, 'SO3': 80.057, 'S': 32.06, 'F': 18.998403163, 'Cl': 35.45, 'Sr': 87.62, 'Ba': 137.327, 'Ni': 58.6934, 'Cr': 51.9961, 'Zr': 91.224}
        self.Elements  = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5', 'CO2', 'SO3', 'S', 'F', 'Cl', 'Sr', 'Ba', 'Ni', 'Cr', 'Zr']
        self.itemstocheck = self.Elements

    def update_data(self, df): 
        if df.empty: return
        self.df = self.CleanDataFile(df.copy())

    def calculate(self):
        if self.df.empty: return
        self.res_mole, self.res_weight, self.res_volume, self.res_calced = [], [], [], []
        
        # Keep track of indices to update main df
        updated_rows = []
        
        for i in range(len(self.df)):
            row = self.df.iloc[i].to_dict()
            try:
                m_res = self.singleCalc(row)
                self.res_mole.append(m_res[0])
                self.res_weight.append(m_res[1])
                self.res_volume.append(m_res[2])
                self.res_calced.append(m_res[3])
                
                # Merge QAPF results (from Volume result) back into the original row data
                # QAPF needs Q, A, P, F. CIPW calculates these.
                # We inject them into the main DF so QAPF module can find them.
                row_update = m_res[2].copy() # Volume data
                updated_rows.append(row_update)
                
            except Exception as e:
                print(f"Error row {i}: {e}")
                updated_rows.append({})
        
        QMessageBox.information(self, "Success", "CIPW Calculation Complete.")

        self.table_mole.setModel(PandasModel(pd.DataFrame(self.res_mole)))
        self.table_weight.setModel(PandasModel(pd.DataFrame(self.res_weight)))

    def save_result(self):
        if not self.res_mole: return
        filename, _ = QFileDialog.getSaveFileName(self, "Save CIPW Result", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if filename:
            try:
                base_name = filename.rsplit('.', 1)[0]
                ext = filename.rsplit('.', 1)[1] if '.' in filename else 'xlsx'
                if '.' not in filename: filename += '.xlsx'
                
                # Helper to save
                def save_df(df_list, suffix):
                    df = pd.DataFrame(df_list)
                    fname = f"{base_name}-{suffix}.{ext}"
                    if ext == 'csv': df.to_csv(fname, index=False)
                    else: df.to_excel(fname, index=False)
                
                save_df(self.res_mole, 'cipw-mole')
                save_df(self.res_weight, 'cipw-mass')
                save_df(self.res_volume, 'cipw-volume')
                save_df(self.res_calced, 'cipw-index')
                
                QMessageBox.information(self, "Success", f"Files saved as {base_name}-cipw-*")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def singleCalc(self, m):
        DataResult={}
        DataWeight={}
        DataVolume={}
        DataCalced={}


        DataResult.update({'Label': m['Label']+' Mole%'})
        DataWeight.update({'Label': m['Label']+' Weight%'})
        DataVolume.update({'Label': m['Label']+' Volue%'})
        DataCalced.update({'Label': m['Label']})
        DataResult.update({'Width': m.get('Width', 1)})
        DataWeight.update({'Width': m.get('Width', 1)})
        DataVolume.update({'Width': m.get('Width', 1)})
        DataCalced.update({'Width': m.get('Width', 1)})
        DataResult.update({'Style': m.get('Style', '-')})
        DataWeight.update({'Style': m.get('Style', '-')})
        DataVolume.update({'Style': m.get('Style', '-')})
        DataCalced.update({'Style': m.get('Style', '-')})
        DataResult.update({'Alpha': m.get('Alpha', 0.5)})
        DataWeight.update({'Alpha': m.get('Alpha', 0.5)})
        DataVolume.update({'Alpha': m.get('Alpha', 0.5)})
        DataCalced.update({'Alpha': m.get('Alpha', 0.5)})
        DataResult.update({'Size': m.get('Size', 10)})
        DataWeight.update({'Size': m.get('Size', 10)})
        DataVolume.update({'Size': m.get('Size', 10)})
        DataCalced.update({'Size': m.get('Size', 10)})
        DataResult.update({'Color': m.get('Color', 'black')})
        DataWeight.update({'Color': m.get('Color', 'black')})
        DataVolume.update({'Color': m.get('Color', 'black')})
        DataCalced.update({'Color': m.get('Color', 'black')})
        DataResult.update({'Marker': m.get('Marker', 'o')})
        DataWeight.update({'Marker': m.get('Marker', 'o')})
        DataVolume.update({'Marker': m.get('Marker', 'o')})
        DataCalced.update({'Marker': m.get('Marker', 'o')})

        WholeMass = 0
        EachMole = {}

        for j in self.Elements:
            '''
            Get the Whole Mole of the dataset
            '''

            try:
                T_TMP = m[j]
            except(KeyError):
                T_TMP = 0

            if j == 'Sr':
                TMP = T_TMP / (87.62 / 103.619 * 10000)
            elif j == 'Ba':
                TMP = T_TMP / (137.327 / 153.326 * 10000)
            elif j == 'Ni':
                TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)
            elif j == 'Cr':
                TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)
            elif j == 'Zr':
                # Zr Multi 2 here
                TMP = T_TMP / ((2 * 91.224) / 123.22200000000001 * 10000)
            else:
                TMP = T_TMP
            V = TMP
            try:
                WholeMass += float(V)
            except ValueError:
                pass



        WeightCorrectionFactor = (100 / WholeMass) if WholeMass != 0 else 0

        for j in self.Elements:
            '''
            Get the Mole percentage of each element
            '''

            try:
                T_TMP = m[j]
            except(KeyError):
                T_TMP = 0

            if j == 'Sr':
                TMP = T_TMP / (87.62 / 103.619 * 10000)

            elif j == 'Ba':
                TMP = T_TMP / (137.327 / 153.326 * 10000)

            elif j == 'Ni':
                TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)

            elif j == 'Cr':
                TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)

            elif j == 'Zr':
                # Zr not Multiple by 2 Here
                TMP = T_TMP / ((91.224) / 123.22200000000001 * 10000)

            else:
                TMP = T_TMP

            M = 0
            try:
                M = TMP / self.BaseMass[j] * WeightCorrectionFactor
            except TypeError:
                pass

            # M= TMP/NewMass(j) * WeightCorrectionFactor

            EachMole.update({j: M})
        # self.DataMole.append(EachMole)

        DataCalculating = EachMole

        Fe3 = DataCalculating['Fe2O3']
        Fe2 = DataCalculating['FeO']
        Mg = DataCalculating['MgO']
        Ca = DataCalculating['CaO']
        Na = DataCalculating['Na2O']

        try:
            DataCalced.update({'Fe3+/(Total Fe) in rock (Mole)': 100 * Fe3 * 2 / (Fe3 * 2 + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Fe3+/(Total Fe) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Mg/(Mg+Total Fe) in rock (Mole)': 100 * Mg / (Mg + Fe3 * 2 + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Mg/(Mg+Total Fe) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Mg/(Mg+Fe2+) in rock (Mole)': 100 * Mg / (Mg + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Mg/(Mg+Fe2+) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Ca/(Ca+Na) in rock (Mole)': 100 * Ca / (Ca + Na * 2)})
        except(ZeroDivisionError):
            DataCalced.update({'Ca/(Ca+Na) in rock (Mole)': 0})
            pass

        DataCalculating['CaO'] += DataCalculating['Sr']
        DataCalculating['Sr'] = 0

        DataCalculating['K2O'] += 2 * DataCalculating['Ba']
        DataCalculating['Ba'] = 0

        try:
            if DataCalculating['CaO'] >= 10 / 3 * DataCalculating['P2O5']:
                DataCalculating['CaO'] -= 10 / 3 * DataCalculating['P2O5']
            else:
                DataCalculating['CaO'] = 0
        except(ZeroDivisionError):
            pass

        DataCalculating['P2O5'] = DataCalculating['P2O5'] / 1.5

        Apatite = DataCalculating['P2O5']

        # IF(S19>=T15,S19-T15,0)

        if DataCalculating['F'] >= DataCalculating['P2O5']:
            DataCalculating['F'] -= DataCalculating['P2O5']
        else:
            DataCalculating['F'] = 0

        if DataCalculating['F'] >= DataCalculating['P2O5']:
            DataCalculating['F'] -= DataCalculating['P2O5']
        else:
            DataCalculating['F'] = 0

        if DataCalculating['Na2O'] >= DataCalculating['Cl']:
            DataCalculating['Na2O'] -= DataCalculating['Cl']
        else:
            DataCalculating['Na2O'] = 0

        Halite = DataCalculating['Cl']

        # IF(U12>=(U19/2),U12-(U19/2),0)
        if DataCalculating['CaO'] >= 0.5 * DataCalculating['F']:
            DataCalculating['CaO'] -= 0.5 * DataCalculating['F']
        else:
            DataCalculating['CaO'] = 0

        DataCalculating['F'] *= 0.5

        Fluorite = DataCalculating['F']

        # =IF(V17>0,IF(V13>=V17,'Thenardite',IF(V13>0,'Both','Anhydrite')),'None')
        AorT = 0
        if DataCalculating['SO3'] <= 0:
            AorT = 'None'
        else:
            if DataCalculating['Na2O'] >= DataCalculating['SO3']:
                AorT = 'Thenardite'
            else:
                if DataCalculating['Na2O'] > 0:
                    AorT = 'Both'
                else:
                    AorT = 'Anhydrite'

        # =IF(W26='Anhydrite',V17,IF(W26='Both',V12,0))
        # =IF(W26='Thenardite',V17,IF(W26='Both',V17-W17,0))

        if AorT == 'Anhydrite':
            DataCalculating['Sr'] = 0
        elif AorT == 'Thenardite':
            DataCalculating['Sr'] = DataCalculating['SO3']
            DataCalculating['SO3'] = 0
        elif AorT == 'Both':
            DataCalculating['Sr'] = DataCalculating['SO3'] - DataCalculating['CaO']
            DataCalculating['SO3'] = DataCalculating['CaO']
        else:
            DataCalculating['SO3'] = 0
            DataCalculating['Sr'] = 0

        DataCalculating['CaO'] -= DataCalculating['SO3']

        DataCalculating['Na2O'] -= DataCalculating['Sr']

        Anhydrite = DataCalculating['SO3']
        Thenardite = DataCalculating['Sr']

        Pyrite = 0.5 * DataCalculating['S']

        # =IF(W9>=(W18*0.5),W9-(W18*0.5),0)

        if DataCalculating['FeO'] >= DataCalculating['S'] * 0.5:
            DataCalculating['FeO'] -= DataCalculating['S'] * 0.5
        else:
            DataCalculating['FeO'] = 0

        # =IF(X24>0,IF(X9>=X24,'Chromite',IF(X9>0,'Both','Magnesiochromite')),'None')

        if DataCalculating['Cr'] > 0:
            if DataCalculating['FeO'] >= DataCalculating['Cr']:
                CorM = 'Chromite'
            elif DataCalculating['FeO'] > 0:
                CorM = 'Both'
            else:
                CorM = 'Magnesiochromite'
        else:
            CorM = 'None'

        # =IF(Y26='Chromite',X24,IF(Y26='Both',X9,0))
        # =IF(Y26='Magnesiochromite',X24,IF(Y26='Both',X24-Y24,0))

        if CorM == 'Chromite':
            DataCalculating['Cr'] = DataCalculating['Cr']
            DataCalculating['Ni'] = 0

        elif CorM == 'Magnesiochromite':
            DataCalculating['Ni'] = DataCalculating['Cr']
            DataCalculating['Cr'] = 0

        elif CorM == 'Both':
            DataCalculating['Ni'] = DataCalculating['Cr'] - DataCalculating['FeO']
            DataCalculating['Cr'] = DataCalculating['FeO']

        else:
            DataCalculating['Cr'] = 0
            DataCalculating['Ni'] = 0

        DataCalculating['MgO'] -= DataCalculating['Ni']

        Magnesiochromite = DataCalculating['Ni']
        Chromite = DataCalculating['Cr']

        # =IF(X9>=Y24,X9-Y24,0)

        if DataCalculating['FeO'] >= DataCalculating['Cr']:
            DataCalculating['FeO'] -= DataCalculating['Cr']
        else:
            DataCalculating['FeO'] = 0

        # =IF(Y6>0,IF(Y9>=Y6,'Ilmenite',IF(Y9>0,'Both','Sphene')),'None')

        if DataCalculating['TiO2'] < 0:
            IorS = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['TiO2']:
                IorS = 'Ilmenite'
            else:
                if DataCalculating['FeO'] > 0:
                    IorS = 'Both'
                else:
                    IorS = 'Sphene'

        # =IF(Z26='Ilmenite',Y6,IF(Z26='Both',Y9,0))
        # =IF(Z26='Sphene',Y6,IF(Z26='Both',Y6-Z6,0))

        if IorS == 'Ilmenite':
            DataCalculating['TiO2'] = DataCalculating['TiO2']
            DataCalculating['MnO'] = 0

        elif IorS == 'Sphene':
            DataCalculating['MnO'] = DataCalculating['TiO2']
            DataCalculating['TiO2'] = 0

        elif IorS == 'Both':

            DataCalculating['MnO'] = DataCalculating['TiO2'] - DataCalculating['FeO']
            DataCalculating['TiO2'] = DataCalculating['FeO']

        else:
            DataCalculating['TiO2'] = 0
            DataCalculating['MnO'] = 0

        DataCalculating['FeO'] -= DataCalculating['TiO2']

        Ilmenite = DataCalculating['TiO2']

        # =IF(Z16>0,IF(Z12>=Z16,'Calcite',IF(Z12>0,'Both','Na2CO3')),'None')

        if DataCalculating['CO2'] <= 0:
            CorN = 'None'
        else:
            if DataCalculating['CaO'] >= DataCalculating['CO2']:
                CorN = 'Calcite'
            else:
                if DataCalculating['CaO'] > 0:
                    CorN = 'Both'
                else:
                    CorN = 'Na2CO3'

        # =IF(AA26='Calcite',Z16,IF(AA26='Both',Z12,0))

        # =IF(AA26='Na2CO3',Z16,IF(AA26='Both',Z16-AA16,0))

        if CorN == 'None':
            DataCalculating['CO2'] = 0
            DataCalculating['SO3'] = 0

        elif CorN == 'Calcite':
            DataCalculating['CO2'] = DataCalculating['CO2']
            DataCalculating['SO3'] = 0

        elif CorN == 'Na2CO3':
            DataCalculating['SO3'] = DataCalculating['SO3']
            DataCalculating['CO2'] = 0

        elif CorN == 'Both':
            DataCalculating['SO3'] = DataCalculating['CO2'] - DataCalculating['CaO']
            DataCalculating['CO2'] = DataCalculating['CaO']

        DataCalculating['CaO'] -= DataCalculating['CO2']

        Calcite = DataCalculating['CO2']

        Na2CO3 = DataCalculating['SO3']

        # =IF(AA17>Z13,0,Z13-AA17)
        if DataCalculating['SO3'] > DataCalculating['Na2O']:
            DataCalculating['Na2O'] = 0
        else:
            DataCalculating['Na2O'] -= DataCalculating['SO3']

        DataCalculating['SiO2'] -= DataCalculating['Zr']
        Zircon = DataCalculating['Zr']

        # =IF(AB14>0,IF(AB7>=AB14,'Orthoclase',IF(AB7>0,'Both','K2SiO3')),'None')

        if DataCalculating['K2O'] <= 0:
            OorK = 'None'
        else:
            if DataCalculating['Al2O3'] >= DataCalculating['K2O']:
                OorK = 'Orthoclase'
            else:
                if DataCalculating['Al2O3'] > 0:
                    OorK = 'Both'
                else:
                    OorK = 'K2SiO3'

        # =IF(AC26='Orthoclase',AB14,IF(AC26='Both',AB7,0))
        # =IF(AC26='K2SiO3',AB14,IF(AC26='Both',AB14-AB7,0))

        if OorK == 'None':
            DataCalculating['K2O'] = 0
            DataCalculating['P2O5'] = 0


        elif OorK == 'Orthoclase':
            DataCalculating['K2O'] = DataCalculating['K2O']
            DataCalculating['P2O5'] = 0


        elif OorK == 'K2SiO3':
            DataCalculating['P2O5'] = DataCalculating['K2O']
            DataCalculating['K2O'] = 0



        elif OorK == 'Both':

            DataCalculating['P2O5'] = DataCalculating['K2O'] - DataCalculating['Al2O3']
            DataCalculating['K2O'] = DataCalculating['Al2O3']

        DataCalculating['Al2O3'] -= DataCalculating['K2O']

        # =IF(AC13>0,IF(AC7>=AC13,'Albite',IF(AC7>0,'Both','Na2SiO3')),'None')

        if DataCalculating['Na2O'] <= 0:
            AorN = 'None'
        else:
            if DataCalculating['Al2O3'] >= DataCalculating['Na2O']:
                AorN = 'Albite'
            else:
                if DataCalculating['Al2O3'] > 0:
                    AorN = 'Both'
                else:
                    AorN = 'Na2SiO3'

        # =IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)

        if DataCalculating['Al2O3'] >= DataCalculating['Na2O'] and DataCalculating['Al2O3'] > 0:
            DataCalculating['Al2O3'] -= DataCalculating['Na2O']
        else:
            DataCalculating['Al2O3'] = 0

        # =IF(AD26='Albite',AC13,IF(AD26='Both',AC7,0))
        # =IF(AD26='Na2SiO3',AC13,IF(AD26='Both',AC13-AD13,0))

        if AorN == 'Albite':
            DataCalculating['Cl'] = 0

        elif AorN == 'Both':
            DataCalculating['Cl'] = DataCalculating['Na2O'] - DataCalculating['Al2O3']
            DataCalculating['Na2O'] = DataCalculating['Al2O3']

        elif AorN == 'Na2SiO3':
            DataCalculating['Cl'] = DataCalculating['Na2O']
            DataCalculating['Na2O'] = 0

        elif AorN == 'None':
            DataCalculating['Na2O'] = 0
            DataCalculating['Cl'] = 0

        # =IF(AD7>0,IF(AD12>0,'Anorthite','None'),'None')

        '''
        Seem like should be =IF(AD7>0,IF(AD12>AD7,'Anorthite','Corundum'),'None')

        If Al2O3 is left after alloting orthoclase and albite, then:
        Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
        If Al2O3 exceeds CaO in the preceding calculation, then:
        Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
        Corundum = Al2O3, CaO =0, Al2O3 = 0


            if DataCalculating['Al2O3']<=0:
                AorC='None'
            else:
                if DataCalculating['CaO']>DataCalculating['Al2O3']:
                    AorC= 'Anorthite'
                else:
                    Aorc='Corundum'

        '''
        AorC = 'None'
        if DataCalculating['Al2O3'] <= 0:
            AorC = 'None'
        else:
            if DataCalculating['CaO'] > 0:
                AorC = 'Anorthite'
            else:
                Aorc = 'None'

        # =IF(AE26='Anorthite',IF(AD12>AD7,0,AD7-AD12),AD7)

        # =IF(AE26='Anorthite',IF(AD7>AD12,0,AD12-AD7),AD12)

        # =IF(AE26='Anorthite',IF(AD7>AD12,AD12,AD7),0)

        if AorC == 'Anorthite':
            if DataCalculating['Al2O3'] >= DataCalculating['CaO']:
                DataCalculating['Sr'] = DataCalculating['CaO']
                DataCalculating['Al2O3'] -= DataCalculating['CaO']
                DataCalculating['CaO'] = 0

            else:
                DataCalculating['Sr'] = DataCalculating['Al2O3']
                DataCalculating['CaO'] -= DataCalculating['Al2O3']
                DataCalculating['Al2O3'] = 0

        else:
            DataCalculating['Sr'] = 0

        Corundum = DataCalculating['Al2O3']
        Anorthite = DataCalculating['Sr']

        # =IF(AE10>0,IF(AE12>=AE10,'Sphene',IF(AE12>0,'Both','Rutile')),'None')

        if DataCalculating['MnO'] <= 0:
            SorR = 'None'
        else:
            if DataCalculating['CaO'] >= DataCalculating['MnO']:
                SorR = 'Sphene'
            elif DataCalculating['CaO'] > 0:
                SorR = 'Both'
            else:
                SorR = 'Rutile'

        # =IF(AF26='Sphene',AE10,IF(AF26='Both',AE12,0))

        # =IF(AF26='Rutile',AE10,IF(AF26='Both',AE10-AE12,0))

        if SorR == 'Sphene':
            DataCalculating['MnO'] = DataCalculating['MnO']
            DataCalculating['S'] = 0

        elif SorR == 'Rutile':
            DataCalculating['S'] = DataCalculating['MnO']
            DataCalculating['MnO'] = 0


        elif SorR == 'Both':
            DataCalculating['S'] = DataCalculating['MnO'] - DataCalculating['CaO']
            DataCalculating['MnO'] = DataCalculating['CaO']

        elif SorR == 'None':
            DataCalculating['MnO'] = 0
            DataCalculating['S'] = 0

        DataCalculating['CaO'] -= DataCalculating['MnO']

        Rutile = DataCalculating['S']

        # =IF(AND(AF20>0),IF(AF8>=AF20,'Acmite',IF(AF8>0,'Both','Na2SiO3')),'None')

        if DataCalculating['Cl'] <= 0:
            ACorN = 'None'
        else:
            if DataCalculating['Fe2O3'] >= DataCalculating['Cl']:
                ACorN = 'Acmite'
            else:
                if DataCalculating['Fe2O3'] > 0:
                    ACorN = 'Both'
                else:
                    ACorN = 'Na2SiO3'

        # =IF(AG26='Acmite',AF20,IF(AG26='Both',AF8,0))

        # =IF(AG26='Na2SiO3',AF20,IF(AG26='Both',AF20-AG19,0))

        if ACorN == 'Acmite':
            DataCalculating['F'] = DataCalculating['Cl']
            DataCalculating['Cl'] = 0

        elif ACorN == 'Na2SiO3':
            DataCalculating['Cl'] = DataCalculating['Cl']
            DataCalculating['F'] = 0

        elif ACorN == 'Both':
            DataCalculating['F'] = DataCalculating['Fe2O3']
            DataCalculating['Cl'] = DataCalculating['Cl'] - DataCalculating['F']

        elif ACorN == 'None':
            DataCalculating['F'] = 0
            DataCalculating['Cl'] = 0

        DataCalculating['Fe2O3'] -= DataCalculating['F']

        Acmite = DataCalculating['F']

        # =IF(AG8>0,IF(AG9>=AG8,'Magnetite',IF(AG9>0,'Both','Hematite')),'None')

        if DataCalculating['Fe2O3'] <= 0:
            MorH = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['Fe2O3']:
                MorH = 'Magnetite'
            else:
                if DataCalculating['FeO'] > 0:
                    MorH = 'Both'
                else:
                    MorH = 'Hematite'

        # =IF(AH26='Magnetite',AG8,IF(AH26='Both',AG9,0))
        # =IF(AH26='Hematite',AG8,IF(AH26='Both',AG8-AG9,0))

        if MorH == 'Magnetite':
            DataCalculating['Fe2O3'] = DataCalculating['Fe2O3']
            DataCalculating['Ba'] = 0

        elif MorH == 'Hematite':
            DataCalculating['Fe2O3'] = 0
            DataCalculating['Ba'] = DataCalculating['FeO']


        elif MorH == 'Both':
            DataCalculating['Fe2O3'] = DataCalculating['FeO']
            DataCalculating['Ba'] = DataCalculating['Fe2O3'] - DataCalculating['FeO']


        elif MorH == 'None':
            DataCalculating['Fe2O3'] = 0
            DataCalculating['Ba'] == 0

        DataCalculating['FeO'] -= DataCalculating['Fe2O3']

        Magnetite = DataCalculating['Fe2O3']
        Hematite = DataCalculating['Ba']

        # =IF(AH11>0,AH11/(AH11+AH9),0)

        Fe2 = DataCalculating['FeO']
        Mg = DataCalculating['MgO']

        if Mg > 0:
            DataCalced.update({'Mg/(Mg+Fe2+) in silicates': 100 * Mg / (Mg + Fe2)})
        else:
            DataCalced.update({'Mg/(Mg+Fe2+) in silicates': 0})

        DataCalculating['FeO'] += DataCalculating['MgO']

        DataCalculating['MgO'] = 0

        # =IF(AI12>0,IF(AI9>=AI12,'Diopside',IF(AI9>0,'Both','Wollastonite')),'None')

        if DataCalculating['CaO'] <= 0:
            DorW = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['CaO']:
                DorW = 'Diopside'
            else:
                if DataCalculating['FeO'] > 0:
                    DorW = 'Both'
                else:
                    DorW = 'Wollastonite'

        # =IF(AJ26='Diopside',AI12,IF(AJ26='Both',AI9,0))

        # =IF(AJ26='Wollastonite',AI12,IF(AJ26='Both',AI12-AI9,0))

        if DorW == 'Diopside':
            DataCalculating['CaO'] = DataCalculating['CaO']
            DataCalculating['S'] = 0

        elif DorW == 'Wollastonite':
            DataCalculating['S'] = DataCalculating['CaO']
            DataCalculating['CaO'] = 0

        elif DorW == 'Both':
            DataCalculating['S'] = DataCalculating['CaO'] - DataCalculating['FeO']
            DataCalculating['CaO'] = DataCalculating['FeO']

        elif DorW == 'None':
            DataCalculating['CaO'] = 0
            DataCalculating['S'] = 0

        DataCalculating['FeO'] -= DataCalculating['CaO']

        Diopside = DataCalculating['CaO']

        Quartz = DataCalculating['SiO2']

        Zircon = DataCalculating['Zr']
        K2SiO3 = DataCalculating['P2O5']

        Na2SiO3 = DataCalculating['Cl']

        Sphene = DataCalculating['MnO']

        Hypersthene = DataCalculating['FeO']

        Albite = DataCalculating['Na2O']

        Orthoclase = DataCalculating['K2O']

        Wollastonite = DataCalculating['S']

        # =AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)

        Quartz = Quartz -(Zircon +
                   K2SiO3 +
                   Anorthite * 2 +
                   Na2SiO3 +
                   Acmite * 4 +
                   Diopside * 2 +
                   Sphene +
                   Hypersthene +
                   Albite * 6 +
                   Orthoclase * 6 +
                   Wollastonite)

        # =IF(AL5>0,AL5,0)

        #if Quartz > 0:
        #    Quartz = Quartz
        #else:
        #    Quartz = 0

        # =IF(AL13>0,IF(AL5>=0,'Hypersthene',IF(AL13+(2*AL5)>0,'Both','Olivine')),'None')

        if Hypersthene <= 0:
            HorO = 'None'
        else:
            if Quartz > 0:
                HorO = 'Hypersthene'
            else:
                if Hypersthene + 2 * Quartz > 0:
                    HorO = 'Both'
                else:
                    HorO = 'Olivine'

        # =IF(AN26='Hypersthene',AL13,IF(AN26='Both',AL13+(2*AL5),0))
        # =IF(AN26='Olivine',AL13*0.5,IF(AN26='Both',ABS(AL5),0))
        Old_Hypersthene = Hypersthene
        if HorO == 'Hypersthene':
            Hypersthene = Hypersthene
            Olivine = 0

        elif HorO == 'Both':
            Hypersthene = Hypersthene + Quartz * 2
            Olivine = abs(Quartz)

        elif HorO == 'Olivine':
            Olivine = Hypersthene / 2
            Hypersthene = 0

        elif HorO == 'None':
            Hypersthene = 0
            Olivine = 0

        # =AL5+AL13-(AN13+AN17)
        Quartz =  Quartz + Old_Hypersthene - (Hypersthene + Olivine)

        # =IF(AL12>0,IF(AN5>=0,'Sphene',IF(AL12+AN5>0,'Both','Perovskite')),'None')

        if Sphene <= 0:
            SorP = 'None'
        else:
            if Quartz >= 0:
                SorP = 'Sphene'
            else:
                if Sphene + Quartz > 0:
                    SorP = 'Both'
                else:
                    SorP = 'Perovskite'

        # =IF(AO26='Sphene',AL12,IF(AO26='Both',AL12+AN5,0))
        # =IF(AO26='Perovskite',AL12,IF(AO26='Both',AL12-AO12,0))

        Old_Sphene = Sphene

        if SorP == 'Sphene':
            Sphene = Sphene
            Perovskite = 0

        elif SorP == 'Perovskite':
            Perovskite = Sphene
            Sphene = 0

        elif SorP == 'Both':
            Sphene += Quartz
            Perovskite = Old_Sphene - Sphene

        elif SorP == 'None':
            Sphene = 0
            Perovskite = 0

        Quartz += Old_Sphene - Sphene

        # =IF(AL14>0,IF(AO5>=0,'Albite',IF(AL14+(AO5/4)>0,'Both','Nepheline')),'None')

        if Albite <= 0:
            AlorNe = 'None'
        else:
            if Quartz >= 0:
                AlorNe = 'Albite'
            else:
                if Albite + (Quartz / 4) > 0:
                    AlorNe = 'Both'
                else:
                    AlorNe = 'Nepheline'

        # =AO5+(6*AL14)-(AP14*6)-(AP19*2)

        # =IF(AP26='Albite',AL14,IF(AP26='Both',AL14+(AO5/4),0))
        # =IF(AP26='Nepheline',AL14,IF(AP26='Both',AL14-AP14,0))

        Old_Albite = Albite

        if AlorNe == 'Albite':
            Albite = Albite
            Nepheline = 0

        elif AlorNe == 'Nepheline':
            Nepheline = Albite
            Albite = 0

        elif AlorNe == 'Both':
            Albite += Quartz / 4
            Nepheline = Old_Albite - Albite

        elif AlorNe == 'None':
            Nepheline = 0
            Albite = 0

        Quartz += (6 * Old_Albite) - (Albite * 6) - (Nepheline * 2)

        # =IF(AL8=0,0,AL8/(AL8+(AP14*2)))

        if Anorthite == 0:
            DataCalced.update({'Plagioclase An content': 0})
        else:
            DataCalced.update({'Plagioclase An content': 100 * Anorthite / (Anorthite + 2 * Albite)})

        # =IF(AL15>0,IF(AP5>=0,'Orthoclase',IF(AL15+(AP5/2)>0,'Both','Leucite')),'None')

        if Orthoclase <= 0:
            OorL = 'None'
        else:
            if Quartz >= 0:
                OorL = 'Orthoclase'
            else:
                if Orthoclase + Quartz / 2 > 0:
                    OorL = 'Both'
                else:
                    OorL = 'Leucite'

        # =IF(AQ26='Orthoclase',AL15,IF(AQ26='Both',AL15+(AP5/2),0))
        # =IF(AQ26='Leucite',AL15,IF(AQ26='Both',AL15-AQ15,0))

        Old_Orthoclase = Orthoclase

        if OorL == 'Orthoclase':
            Orthoclase = Orthoclase
            Leucite = 0

        elif OorL == 'Leucite':
            Leucite = Orthoclase
            Orthoclase = 0

        elif OorL == 'Both':
            Orthoclase += Quartz / 2
            Leucite = Old_Orthoclase - Orthoclase

        elif OorL == 'None':
            Orthoclase = 0
            Leucite = 0

        # =AP5+(AL15*6)-(AQ15*6)-(AQ20*4)

        Quartz += (Old_Orthoclase * 6) - (Orthoclase * 6) - (Leucite * 4)

        # =IF(AL16>0,IF(AQ5>=0,'Wollastonite',IF(AL16+(AQ5*2)>0,'Both','Larnite')),'None')
        if Wollastonite <= 0:
            WorB = 'None'
        else:
            if Quartz >= 0:
                WorB = 'Wollastonite'
            else:
                if Wollastonite + Quartz / 2 > 0:
                    WorB = 'Both'
                else:
                    WorB = 'Larnite'

        # =IF(AR26='Wollastonite',AL16,IF(AR26='Both',AL16+(2*AQ5),0))
        # =IF(AR26='Larnite',AL16/2,IF(AR26='Both',(AL16-AR16)/2,0))

        Old_Wollastonite = Wollastonite
        if WorB == 'Wollastonite':
            Wollastonite = Wollastonite
            Larnite = 0

        elif WorB == 'Larnite':
            Larnite = Wollastonite / 2
            Wollastonite = 0

        elif WorB == 'Both':
            Wollastonite += Quartz * 2
            Larnite = (Old_Wollastonite - Wollastonite) / 2

        elif WorB == 'None':
            Wollastonite = 0
            Larnite = 0

        # =AQ5+AL16-AR16-AR21
        Quartz += Old_Wollastonite - Wollastonite - Larnite

        # =IF(AL11>0,IF(AR5>=0,'Diopside',IF(AL11+AR5>0,'Both','LarniteOlivine')),'None')

        if Diopside <= 0:
            DorL = 'None'
        else:
            if Quartz >= 0:
                DorL = 'Diopside'
            else:
                if Diopside + Quartz > 0:
                    DorL = 'Both'
                else:
                    DorL = 'LarniteOlivine'

        # =IF(AS26='Diopside',AL11,IF(AS26='Both',AL11+AR5,0))
        # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AN17
        # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AR21

        Old_Diopside = Diopside
        Old_Larnite = Larnite
        Old_Olivine = Olivine
        if DorL == 'Diopside':
            Diopside = Diopside



        elif DorL == 'LarniteOlivine':
            Larnite += Diopside / 2
            Olivine += Diopside / 2
            Diopside = 0

        elif DorL == 'Both':
            Diopside += Quartz
            Larnite += Old_Diopside - Diopside
            Olivine += Old_Diopside - Diopside



        elif DorL == 'None':
            Diopside = 0

        # =AR5+(AL11*2)+AN17+AR21-AS21-(AS11*2)-AS17
        Quartz += (Old_Diopside * 2) + Old_Olivine + Old_Larnite - Larnite - (Diopside * 2) - Olivine

        # =IF(AQ20>0,IF(AS5>=0,'Leucite',IF(AQ20+(AS5/2)>0,'Both','Kalsilite')),'None')

        if Leucite <= 0:
            LorK = 'None'
        else:
            if Quartz >= 0:
                LorK = 'Leucite'
            else:
                if Leucite + Quartz / 2 > 0:
                    LorK = 'Both'
                else:
                    LorK = 'Kalsilite'

        # =IF(AT26='Leucite',AQ20,IF(AT26='Both',AQ20+(AS5/2),0))
        # =IF(AT26='Kalsilite',AQ20,IF(AT26='Both',AQ20-AT20,0))

        Old_Leucite = Leucite

        if LorK == 'Leucite':
            Leucite = Leucite
            Kalsilite = 0

        elif LorK == 'Kalsilite':
            Kalsilite = Leucite
            Leucite = 0

        elif LorK == 'Both':
            Leucite += Quartz / 2
            Kalsilite = Old_Leucite - Leucite

        elif LorK == 'None':
            Leucite = 0
            Kalsilite = 0

        # =AS5+(AQ20*4)-(AT20*4)-(AT22*2)
        Quartz += Old_Leucite * 4 - Leucite * 4 - Kalsilite * 2

        Q = Quartz
        A = Orthoclase
        P = Anorthite + Albite
        F = Nepheline + Leucite + Kalsilite

        DataResult.update({'Quartz':  round(Quartz*100,4)})
        DataResult.update({'Zircon':  round(Zircon*100,4)})
        DataResult.update({'K2SiO3':  round(K2SiO3*100,4)})
        DataResult.update({'Anorthite':  round(Anorthite*100,4)})
        DataResult.update({'Na2SiO3':  round(Na2SiO3*100,4)})
        DataResult.update({'Acmite':  round(Acmite*100,4)})
        DataResult.update({'Diopside':  round(Diopside*100,4)})
        DataResult.update({'Sphene':  round(Sphene*100,4)})
        DataResult.update({'Hypersthene':  round(Hypersthene*100,4)})
        DataResult.update({'Albite':  round(Albite*100,4)})
        DataResult.update({'Orthoclase':  round(Orthoclase*100,4)})
        DataResult.update({'Wollastonite':  round(Wollastonite*100,4)})
        DataResult.update({'Olivine':  round(Olivine*100,4)})
        DataResult.update({'Perovskite':  round(Perovskite*100,4)})
        DataResult.update({'Nepheline':  round(Nepheline*100,4)})
        DataResult.update({'Leucite':  round(Leucite*100,4)})
        DataResult.update({'Larnite':  round(Larnite*100,4)})
        DataResult.update({'Kalsilite':  round(Kalsilite*100,4)})
        DataResult.update({'Apatite':  round(Apatite*100,4)})
        DataResult.update({'Halite':  round(Halite*100,4)})
        DataResult.update({'Fluorite':  round(Fluorite*100,4)})
        DataResult.update({'Anhydrite':  round(Anhydrite*100,4)})
        DataResult.update({'Thenardite':  round(Thenardite*100,4)})
        DataResult.update({'Pyrite':  round(Pyrite*100,4)})
        DataResult.update({'Magnesiochromite':  round(Magnesiochromite*100,4)})
        DataResult.update({'Chromite':  round(Chromite*100,4)})
        DataResult.update({'Ilmenite':  round(Ilmenite*100,4)})
        DataResult.update({'Calcite':  round(Calcite*100,4)})
        DataResult.update({'Na2CO3':  round(Na2CO3*100,4)})
        DataResult.update({'Corundum':  round(Corundum*100,4)})
        DataResult.update({'Rutile':  round(Rutile*100,4)})
        DataResult.update({'Magnetite':  round(Magnetite*100,4)})
        DataResult.update({'Hematite':  round(Hematite*100,4)})
        DataResult.update({'Q Mole':  round(Q*100,4)})
        DataResult.update({'A Mole':  round(A*100,4)})
        DataResult.update({'P Mole':  round(P*100,4)})
        DataResult.update({'F Mole':  round(F*100,4)})

        DataWeight.update({'Quartz':  round(Quartz * self.DataBase['Quartz'][0],4)})
        DataWeight.update({'Zircon':  round(Zircon * self.DataBase['Zircon'][0],4)})
        DataWeight.update({'K2SiO3':  round(K2SiO3 * self.DataBase['K2SiO3'][0],4)})
        DataWeight.update({'Anorthite':  round(Anorthite * self.DataBase['Anorthite'][0],4)})
        DataWeight.update({'Na2SiO3':  round(Na2SiO3 * self.DataBase['Na2SiO3'][0],4)})
        DataWeight.update({'Acmite':  round(Acmite * self.DataBase['Acmite'][0],4)})
        DataWeight.update({'Diopside':  round(Diopside * self.DataBase['Diopside'][0],4)})
        DataWeight.update({'Sphene':  round(Sphene * self.DataBase['Sphene'][0],4)})
        DataWeight.update({'Hypersthene':  round(Hypersthene * self.DataBase['Hypersthene'][0],4)})
        DataWeight.update({'Albite':  round(Albite * self.DataBase['Albite'][0],4)})
        DataWeight.update({'Orthoclase':  round(Orthoclase * self.DataBase['Orthoclase'][0],4)})
        DataWeight.update({'Wollastonite':  round(Wollastonite * self.DataBase['Wollastonite'][0],4)})
        DataWeight.update({'Olivine':  round(Olivine * self.DataBase['Olivine'][0],4)})
        DataWeight.update({'Perovskite':  round(Perovskite * self.DataBase['Perovskite'][0],4)})
        DataWeight.update({'Nepheline':  round(Nepheline * self.DataBase['Nepheline'][0],4)})
        DataWeight.update({'Leucite':  round(Leucite * self.DataBase['Leucite'][0],4)})
        DataWeight.update({'Larnite':  round(Larnite * self.DataBase['Larnite'][0],4)})
        DataWeight.update({'Kalsilite':  round(Kalsilite * self.DataBase['Kalsilite'][0],4)})
        DataWeight.update({'Apatite':  round(Apatite * self.DataBase['Apatite'][0],4)})
        DataWeight.update({'Halite':  round(Halite * self.DataBase['Halite'][0],4)})
        DataWeight.update({'Fluorite':  round(Fluorite * self.DataBase['Fluorite'][0],4)})
        DataWeight.update({'Anhydrite':  round(Anhydrite * self.DataBase['Anhydrite'][0],4)})
        DataWeight.update({'Thenardite':  round(Thenardite * self.DataBase['Thenardite'][0],4)})
        DataWeight.update({'Pyrite':  round(Pyrite * self.DataBase['Pyrite'][0],4)})
        DataWeight.update({'Magnesiochromite':  round(Magnesiochromite * self.DataBase['Magnesiochromite'][0],4)})
        DataWeight.update({'Chromite':  round(Chromite * self.DataBase['Chromite'][0],4)})
        DataWeight.update({'Ilmenite':  round(Ilmenite * self.DataBase['Ilmenite'][0],4)})
        DataWeight.update({'Calcite':  round(Calcite * self.DataBase['Calcite'][0],4)})
        DataWeight.update({'Na2CO3':  round(Na2CO3 * self.DataBase['Na2CO3'][0],4)})
        DataWeight.update({'Corundum':  round(Corundum * self.DataBase['Corundum'][0],4)})
        DataWeight.update({'Rutile':  round(Rutile * self.DataBase['Rutile'][0],4)})
        DataWeight.update({'Magnetite':  round(Magnetite * self.DataBase['Magnetite'][0],4)})
        DataWeight.update({'Hematite':  round(Hematite * self.DataBase['Hematite'][0],4)})
        DataWeight.update({'Q Weight':  round(Quartz * self.DataBase['Quartz'][0],4)})
        DataWeight.update({'A Weight':  round(Orthoclase * self.DataBase['Orthoclase'][0],4)})
        DataWeight.update({'P Weight':  round(Anorthite * self.DataBase['Anorthite'][0] + Albite * self.DataBase['Albite'][0],4)})
        DataWeight.update({'F Weight':  round(Nepheline * self.DataBase['Nepheline'][0] + Leucite * self.DataBase['Leucite'][0] + Kalsilite * self.DataBase['Kalsilite'][0],4)})


        WholeVolume = 0
        WholeMole = 0
        tmpVolume = []

        tmpVolume.append(Quartz * self.DataBase['Quartz'][0] / self.DataBase['Quartz'][1])
        tmpVolume.append(Zircon * self.DataBase['Zircon'][0] / self.DataBase['Zircon'][1])
        tmpVolume.append(K2SiO3 * self.DataBase['K2SiO3'][0] / self.DataBase['K2SiO3'][1])
        tmpVolume.append(Anorthite * self.DataBase['Anorthite'][0] / self.DataBase['Anorthite'][1])
        tmpVolume.append(Na2SiO3 * self.DataBase['Na2SiO3'][0] / self.DataBase['Na2SiO3'][1])
        tmpVolume.append(Acmite * self.DataBase['Acmite'][0] / self.DataBase['Acmite'][1])
        tmpVolume.append(Diopside * self.DataBase['Diopside'][0] / self.DataBase['Diopside'][1])
        tmpVolume.append(Sphene * self.DataBase['Sphene'][0] / self.DataBase['Sphene'][1])
        tmpVolume.append(Hypersthene * self.DataBase['Hypersthene'][0] / self.DataBase['Hypersthene'][1])
        tmpVolume.append(Albite * self.DataBase['Albite'][0] / self.DataBase['Albite'][1])
        tmpVolume.append(Orthoclase * self.DataBase['Orthoclase'][0] / self.DataBase['Orthoclase'][1])
        tmpVolume.append(Wollastonite * self.DataBase['Wollastonite'][0] / self.DataBase['Wollastonite'][1])
        tmpVolume.append(Olivine * self.DataBase['Olivine'][0] / self.DataBase['Olivine'][1])
        tmpVolume.append(Perovskite * self.DataBase['Perovskite'][0] / self.DataBase['Perovskite'][1])
        tmpVolume.append(Nepheline * self.DataBase['Nepheline'][0] / self.DataBase['Nepheline'][1])
        tmpVolume.append(Leucite * self.DataBase['Leucite'][0] / self.DataBase['Leucite'][1])
        tmpVolume.append(Larnite * self.DataBase['Larnite'][0] / self.DataBase['Larnite'][1])
        tmpVolume.append(Kalsilite * self.DataBase['Kalsilite'][0] / self.DataBase['Kalsilite'][1])
        tmpVolume.append(Apatite * self.DataBase['Apatite'][0] / self.DataBase['Apatite'][1])
        tmpVolume.append(Halite * self.DataBase['Halite'][0] / self.DataBase['Halite'][1])
        tmpVolume.append(Fluorite * self.DataBase['Fluorite'][0] / self.DataBase['Fluorite'][1])
        tmpVolume.append(Anhydrite * self.DataBase['Anhydrite'][0] / self.DataBase['Anhydrite'][1])
        tmpVolume.append(Thenardite * self.DataBase['Thenardite'][0] / self.DataBase['Thenardite'][1])
        tmpVolume.append(Pyrite * self.DataBase['Pyrite'][0] / self.DataBase['Pyrite'][1])
        tmpVolume.append(Magnesiochromite * self.DataBase['Magnesiochromite'][0] / self.DataBase['Magnesiochromite'][1])
        tmpVolume.append(Chromite * self.DataBase['Chromite'][0] / self.DataBase['Chromite'][1])
        tmpVolume.append(Ilmenite * self.DataBase['Ilmenite'][0] / self.DataBase['Ilmenite'][1])
        tmpVolume.append(Calcite * self.DataBase['Calcite'][0] / self.DataBase['Calcite'][1])
        tmpVolume.append(Na2CO3 * self.DataBase['Na2CO3'][0] / self.DataBase['Na2CO3'][1])
        tmpVolume.append(Corundum * self.DataBase['Corundum'][0] / self.DataBase['Corundum'][1])
        tmpVolume.append(Rutile * self.DataBase['Rutile'][0] / self.DataBase['Rutile'][1])
        tmpVolume.append(Magnetite * self.DataBase['Magnetite'][0] / self.DataBase['Magnetite'][1])
        tmpVolume.append(Hematite * self.DataBase['Hematite'][0] / self.DataBase['Hematite'][1])

        WholeVolume = sum(tmpVolume)

        DataVolume.update(
            {'Quartz':  round((Quartz * self.DataBase['Quartz'][0] / self.DataBase['Quartz'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Zircon':  round((Zircon * self.DataBase['Zircon'][0] / self.DataBase['Zircon'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'K2SiO3':  round((K2SiO3 * self.DataBase['K2SiO3'][0] / self.DataBase['K2SiO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Anorthite':  round((Anorthite * self.DataBase['Anorthite'][0] / self.DataBase['Anorthite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Na2SiO3':  round((Na2SiO3 * self.DataBase['Na2SiO3'][0] / self.DataBase['Na2SiO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Acmite':  round((Acmite * self.DataBase['Acmite'][0] / self.DataBase['Acmite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Diopside':  round((Diopside * self.DataBase['Diopside'][0] / self.DataBase['Diopside'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Sphene':  round((Sphene * self.DataBase['Sphene'][0] / self.DataBase['Sphene'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Hypersthene':  round((Hypersthene * self.DataBase['Hypersthene'][0] / self.DataBase['Hypersthene'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Albite':  round((Albite * self.DataBase['Albite'][0] / self.DataBase['Albite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Orthoclase':  round((Orthoclase * self.DataBase['Orthoclase'][0] / self.DataBase['Orthoclase'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Wollastonite':  round((Wollastonite * self.DataBase['Wollastonite'][0] /
                                            self.DataBase['Wollastonite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Olivine':  round((Olivine * self.DataBase['Olivine'][0] / self.DataBase['Olivine'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Perovskite':  round((Perovskite * self.DataBase['Perovskite'][0] / self.DataBase['Perovskite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Nepheline':  round((Nepheline * self.DataBase['Nepheline'][0] / self.DataBase['Nepheline'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Leucite':  round((Leucite * self.DataBase['Leucite'][0] / self.DataBase['Leucite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Larnite':  round((Larnite * self.DataBase['Larnite'][0] / self.DataBase['Larnite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Kalsilite':  round((Kalsilite * self.DataBase['Kalsilite'][0] / self.DataBase['Kalsilite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Apatite':  round((Apatite * self.DataBase['Apatite'][0] / self.DataBase['Apatite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Halite':  round((Halite * self.DataBase['Halite'][0] / self.DataBase['Halite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Fluorite':  round((Fluorite * self.DataBase['Fluorite'][0] / self.DataBase['Fluorite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Anhydrite':  round((Anhydrite * self.DataBase['Anhydrite'][0] / self.DataBase['Anhydrite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Thenardite':  round((Thenardite * self.DataBase['Thenardite'][0] / self.DataBase['Thenardite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Pyrite':  round((Pyrite * self.DataBase['Pyrite'][0] / self.DataBase['Pyrite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Magnesiochromite':  round((Magnesiochromite * self.DataBase['Magnesiochromite'][0] /
                                                self.DataBase['Magnesiochromite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Chromite':  round((Chromite * self.DataBase['Chromite'][0] / self.DataBase['Chromite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Ilmenite':  round((Ilmenite * self.DataBase['Ilmenite'][0] / self.DataBase['Ilmenite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Calcite':  round((Calcite * self.DataBase['Calcite'][0] / self.DataBase['Calcite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Na2CO3':  round((Na2CO3 * self.DataBase['Na2CO3'][0] / self.DataBase['Na2CO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Corundum':  round((Corundum * self.DataBase['Corundum'][0] / self.DataBase['Corundum'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Rutile':  round((Rutile * self.DataBase['Rutile'][0] / self.DataBase['Rutile'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Magnetite':  round((Magnetite * self.DataBase['Magnetite'][0] / self.DataBase['Magnetite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Hematite':  round((Hematite * self.DataBase['Hematite'][0] / self.DataBase['Hematite'][1]) / WholeVolume * 100,4)})

        DataVolume.update({'Q':  round(DataVolume['Quartz'],4)})
        DataVolume.update({'A':  round(DataVolume['Orthoclase'],4)})

        DataVolume.update({'P':  round(DataVolume['Anorthite'] + DataVolume['Albite'],4)})
        DataVolume.update({'F':  round(DataVolume['Nepheline'] + DataVolume['Leucite'] + DataVolume['Kalsilite'],4)})

        DI = 0

        DI = Quartz + Anorthite + Albite + Orthoclase + Nepheline + Leucite + Kalsilite


        DiWeight=0
        DiVolume=0

        DiWeight = DataWeight['Quartz']+DataWeight['Anorthite']+DataWeight['Albite']+DataWeight['Orthoclase']+DataWeight['Nepheline']+DataWeight['Leucite']+DataWeight['Kalsilite']
        DiVolume = DataVolume['Quartz']+DataVolume['Anorthite']+DataVolume['Albite']+DataVolume['Orthoclase']+DataVolume['Nepheline']+DataVolume['Leucite']+DataVolume['Kalsilite']

        DataCalced.update({'Differentiation Index Weight': DiWeight})

        DataCalced.update({'Differentiation Index Volume': DiVolume})

        return (DataResult, DataWeight, DataVolume, DataCalced)

class HarkerWindow(BasePlotWindow, Tool):
    def __init__(self, df=pd.DataFrame(), parent=None):
        BasePlotWindow.__init__(self, df, parent)
        self.itemstocheck = ['SiO2', 'Al2O3', 'MgO', 'Fe2O3', 'CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'MnO']
        
        # Controls
        self.chk_fit1 = QCheckBox("Linear Fit")
        self.chk_fit1.stateChanged.connect(self.plot)
        self.chk_fit2 = QCheckBox("Quadratic Fit")
        self.chk_fit2.stateChanged.connect(self.plot)
        self.chk_fit3 = QCheckBox("Cubic Fit")
        self.chk_fit3.stateChanged.connect(self.plot)
        self.btn_export = QPushButton("Export Data")
        self.btn_export.clicked.connect(self.export_result)
        
        self.control_layout.addWidget(self.chk_fit1)
        self.control_layout.addWidget(self.chk_fit2)
        self.control_layout.addWidget(self.chk_fit3)
        self.control_layout.addWidget(self.btn_export)
        self.control_layout.addStretch()
        
        self.items = [r'$Al_2O_3$', r'$MgO$', r'$Fe2O3_{Total}$', r'$CaO$', r'$Na_2O$', r'$K_2O$', r'$TiO_2$', r'$P_2O_5$', r'$MnO$']
        self.col_map = {'$Al_2O_3$': 'Al2O3', '$MgO$': 'MgO', '$Fe2O3_{Total}$': 'Fe2O3', '$CaO$': 'CaO', '$Na_2O$': 'Na2O', '$K_2O$': 'K2O', '$TiO_2$': 'TiO2', '$P_2O_5$': 'P2O5', '$MnO$': 'MnO'}
        self.info_box.setText("Harker Diagram")

    def update_data(self, df): 
        if df.empty: return
        self.df = self.CleanDataFile(df.copy())
        self.plot()

    def plot(self):
        self.fig.clear()
        axes = self.fig.subplots(3, 3)
        self.fig.subplots_adjust(hspace=0.4, wspace=0.3)
        if self.df.empty: return
        
        # Use our new BasePlotWindow helper for the points
        x = pd.to_numeric(self.df.get('SiO2', []), errors='coerce')
        
        for i, ax in enumerate(axes.flat):
            ax.set_box_aspect(1) # Enforce square aspect ratio
            if i < len(self.items):
                ylabel = self.items[i]
                col = self.col_map.get(ylabel)
                
                # Plot points with smart legend
                self.plot_points(ax, 'SiO2', col)
                
                ax.set_ylabel(ylabel)
                ax.set_xlabel('SiO2')
                
                # Fits (Calculated on all valid data, regardless of groups)
                y = pd.to_numeric(self.df.get(col, []), errors='coerce')
                mask = ~np.isnan(x) & ~np.isnan(y)
                x_clean = x[mask]
                y_clean = y[mask]

                if len(x_clean) > 1:
                    xx = np.linspace(x_clean.min(), x_clean.max(), 100)
                    if self.chk_fit1.isChecked() and len(x_clean) > 1:
                        try:
                            z = np.polyfit(x_clean, y_clean, 1)
                            ax.plot(xx, np.poly1d(z)(xx), 'r--', lw=1, label='Linear' if i==0 else "_nolegend_")
                        except: pass
                    if self.chk_fit2.isChecked() and len(x_clean) > 2:
                        try:
                            z = np.polyfit(x_clean, y_clean, 2)
                            ax.plot(xx, np.poly1d(z)(xx), 'g--', lw=1, label='Quad' if i==0 else "_nolegend_")
                        except: pass
                    if self.chk_fit3.isChecked() and len(x_clean) > 3:
                        try:
                            z = np.polyfit(x_clean, y_clean, 3)
                            ax.plot(xx, np.poly1d(z)(xx), 'm--', lw=1, label='Cubic' if i==0 else "_nolegend_")
                        except: pass
        
        # Single Legend for the whole figure
        # Gather handles and labels from the first subplot (assuming consistency)
        handles, labels = axes.flat[0].get_legend_handles_labels()
        if handles:
            self.fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=4, fontsize='small')
            self.fig.subplots_adjust(top=0.9, hspace=0.4, wspace=0.3)
        else:
            self.fig.subplots_adjust(top=0.95, hspace=0.4, wspace=0.3)
                        
        self.canvas.draw()

    def export_result(self):
        if self.df.empty: return
        TableViewer(self.df, "Harker Data", self).exec()

class QuickPlotWindow(QWidget):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.df = df
        self.layout = QVBoxLayout(self)
        self.ctrl = QHBoxLayout()
        self.cb_x = QComboBox(); self.cb_y = QComboBox()
        self.btn = QPushButton("Plot"); self.btn.clicked.connect(self.plot)
        self.ctrl.addWidget(QLabel("X:")); self.ctrl.addWidget(self.cb_x)
        self.ctrl.addWidget(QLabel("Y:")); self.ctrl.addWidget(self.cb_y)
        self.ctrl.addWidget(self.btn); self.layout.addLayout(self.ctrl)
        self.plot_widget = pg.PlotWidget(); self.plot_widget.setBackground('w')
        self.layout.addWidget(self.plot_widget)

    def update_data(self, df):
        self.df = df; self.cb_x.clear(); self.cb_y.clear()
        cols = df.select_dtypes(include=np.number).columns.tolist()
        self.cb_x.addItems(cols); self.cb_y.addItems(cols)
        if 'SiO2' in cols: self.cb_x.setCurrentText('SiO2')
        if 'MgO' in cols: self.cb_y.setCurrentText('MgO')
        self.plot()

    def plot(self):
        self.plot_widget.clear()
        if self.df.empty: return
        x = self.df[self.cb_x.currentText()].values
        y = self.df[self.cb_y.currentText()].values
        self.plot_widget.plot(x, y, pen=None, symbol='o', symbolBrush='b')
        self.plot_widget.setLabel('bottom', self.cb_x.currentText())
        self.plot_widget.setLabel('left', self.cb_y.currentText())

# ==========================================
# 6. Main App
# ==========================================

class GeoPyToolApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"GeoPyTool {VERSION}")
        self.resize(1280, 800)
        self.central = QWidget(); self.setCentralWidget(self.central)
        self.layout = QHBoxLayout(self.central)
        
        self.sidebar = QListWidget(); self.sidebar.setMaximumWidth(200)
        self.sidebar.addItems(["Data Table", "TAS", "REE", "Trace", "Pearce", "CIPW", "Harker", "Quick Plot"])
        self.sidebar.currentRowChanged.connect(self.switch)
        
        self.stack = QStackedWidget()
        self.df = pd.DataFrame()
        
        # Modules
        self.view_data = QWidget()
        l = QVBoxLayout(self.view_data)
        btn = QPushButton("Load Data"); btn.clicked.connect(self.load)
        self.table = CustomQTableView()
        l.addWidget(btn); l.addWidget(self.table)
        
        self.mod_tas = TASWindow()
        self.mod_ree = REEWindow()
        self.mod_trace = TraceWindow()
        self.mod_pearce = PearceWindow()
        self.mod_cipw = CIPWWindow()
        self.mod_harker = HarkerWindow()
        self.mod_quick = QuickPlotWindow()
        
        self.stack.addWidget(self.view_data)
        self.stack.addWidget(self.mod_tas)
        self.stack.addWidget(self.mod_ree)
        self.stack.addWidget(self.mod_trace)
        self.stack.addWidget(self.mod_pearce)
        self.stack.addWidget(self.mod_cipw)
        self.stack.addWidget(self.mod_harker)
        self.stack.addWidget(self.mod_quick)
        
        self.layout.addWidget(self.sidebar); self.layout.addWidget(self.stack)

    def switch(self, idx):
        self.stack.setCurrentIndex(idx)
        w = self.stack.currentWidget()
        if hasattr(w, 'update_data'): w.update_data(self.df)

    def load(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open", "", "Data (*.csv *.xlsx)")
        if f:
            if f.endswith('.csv'): self.df = pd.read_csv(f)
            else: self.df = pd.read_excel(f)
            self.table.setModel(PandasModel(self.df))
            self.statusBar().showMessage(f"Loaded {len(self.df)} rows")


def main():
    # Linux desktop environments use an app's .desktop file to integrate the app
    # in to their application menus. The .desktop file of this app will include
    # the StartupWMClass key, set to app's formal name. This helps associate the
    # app's windows to its menu item.
    #
    # For association to work, any windows of the app must have WMCLASS property
    # set to match the value set in app's desktop file. For PySide6, this is set
    # with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    
    # Retrieve the app's metadata
    try:
        metadata = importlib.metadata.metadata(app_module)
        formal_name = metadata["Formal-Name"]
    except:
        formal_name = "GeoPyToolLite"

    QApplication.setApplicationName(formal_name)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    main_window = GeoPyToolApp()
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = GeoPyToolApp()
    w.show()
    sys.exit(app.exec())
