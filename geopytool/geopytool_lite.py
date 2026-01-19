import sys
import csv
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QFileDialog, QLabel, 
                               QMessageBox, QSizePolicy, QFrame, QSplitter)
from PySide6.QtCore import Qt, QPointF, QRectF, QSize, Signal
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QFont, QAction, QIcon, QPainterPath

# ==========================================
# Core Data Handling (Replaces Pandas)
# ==========================================
class GeoData:
    def __init__(self):
        self.headers = []
        self.data = []  # List of dictionaries
        self.filepath = ""

    def load_csv(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames
                self.data = [row for row in reader]
                self.filepath = filepath
            
            # Clean numeric data
            for row in self.data:
                for key in row:
                    try:
                        row[key] = float(row[key])
                    except (ValueError, TypeError):
                        pass # Keep as string if not numeric
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False

    def get_column(self, col_name):
        if not self.data:
            return []
        return [row.get(col_name) for row in self.data]

    def get_numeric_column(self, col_name):
        values = []
        for row in self.data:
            val = row.get(col_name)
            if isinstance(val, (int, float)):
                values.append(val)
            else:
                values.append(0.0) # Default to 0 for NaNs in this simple version
        return values

# ==========================================
# Plotting Framework (Replaces Matplotlib)
# ==========================================
class GeoPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.setAutoFillBackground(True)
        self.margins = {'left': 60, 'right': 40, 'top': 40, 'bottom': 50}
        self.x_range = (0, 100)
        self.y_range = (0, 100)
        self.data_points = [] # List of (x, y, color, label)
        
    def set_range(self, x_min, x_max, y_min, y_max):
        self.x_range = (x_min, x_max)
        self.y_range = (y_min, y_max)
        self.update()

    def transform_x(self, x_val):
        width = self.width() - self.margins['left'] - self.margins['right']
        x_span = self.x_range[1] - self.x_range[0]
        if x_span == 0: return self.margins['left']
        return self.margins['left'] + ((x_val - self.x_range[0]) / x_span) * width

    def transform_y(self, y_val):
        height = self.height() - self.margins['top'] - self.margins['bottom']
        y_span = self.y_range[1] - self.y_range[0]
        if y_span == 0: return self.height() - self.margins['bottom']
        return (self.height() - self.margins['bottom']) - ((y_val - self.y_range[0]) / y_span) * height

    def draw_axes(self, painter):
        w = self.width()
        h = self.height()
        left = self.margins['left']
        right = w - self.margins['right']
        top = self.margins['top']
        bottom = h - self.margins['bottom']

        painter.setPen(QPen(Qt.black, 2))
        
        # Draw Box
        painter.drawLine(left, top, left, bottom) # Y axis
        painter.drawLine(left, bottom, right, bottom) # X axis
        painter.drawLine(right, bottom, right, top)
        painter.drawLine(right, top, left, top)

        # Draw Ticks (Simple auto-ticks)
        painter.setFont(QFont("Arial", 10))
        
        # X Ticks
        x_span = self.x_range[1] - self.x_range[0]
        x_step = 10 if x_span > 50 else 5 if x_span > 10 else 1
        x_curr = math.ceil(self.x_range[0] / x_step) * x_step
        while x_curr <= self.x_range[1]:
            px = self.transform_x(x_curr)
            painter.drawLine(int(px), bottom, int(px), bottom + 5)
            painter.drawText(int(px) - 20, bottom + 20, 40, 20, Qt.AlignCenter, str(x_curr))
            x_curr += x_step

        # Y Ticks
        y_span = self.y_range[1] - self.y_range[0]
        y_step = 5 if y_span > 20 else 2 if y_span > 5 else 1
        y_curr = math.ceil(self.y_range[0] / y_step) * y_step
        while y_curr <= self.y_range[1]:
            py = self.transform_y(y_curr)
            painter.drawLine(left - 5, int(py), left, int(py))
            painter.drawText(left - 45, int(py) - 10, 40, 20, Qt.AlignRight | Qt.AlignVCenter, str(y_curr))
            y_curr += y_step

# ==========================================
# TAS Diagram Implementation
# ==========================================
class TASPlot(GeoPlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_range(30, 90, 0, 20) # Standard TAS ranges
        
        # TAS Fields (Wilson et al. 1989)
        # Format: List of polygons, each polygon is a list of [x, y]
        self.fields = [
            [[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]], # F
            [[41, 0], [41, 3], [45, 3], [45, 0]], # Pc
            [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]], # U1
            [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]], # U2
            [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]], # U3
            [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]], # Ph
            [[45, 0], [45, 2], [52, 5], [52, 0]], # Ba
            [[45, 2], [45, 5], [52, 5]], # Bs
            [[45, 5], [49.4, 7.3], [52, 5]], # S1
            [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]], # S2
            [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]], # S3
            [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]], # T
            [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]], # Td
            [[52, 0], [52, 5], [57, 5.9], [57, 0]], # O1
            [[57, 0], [57, 5.9], [63, 7], [63, 0]], # O2
            [[63, 0], [63, 7], [69, 8], [77.3, 0]], # O3
            [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]], # R
            [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]], # Q
        ]
        
        self.field_labels = [
            ("F", 39, 10), ("Pc", 43, 1.5), ("U1", 44, 6), ("U2", 47.5, 3.5), 
            ("U3", 49.5, 12), ("Ph", 55, 16), ("Ba", 48, 1), ("Bs", 48, 3.5),
            ("S1", 49, 5.2), ("S2", 53, 7), ("S3", 58, 9), ("T", 60, 12),
            ("Td", 65, 10), ("O1", 54, 3), ("O2", 59, 3), ("O3", 67, 3),
            ("R", 75, 9), ("Q", 85, 2)
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # White background
        painter.fillRect(self.rect(), Qt.white)
        
        # Draw TAS Fields
        painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        
        for poly_coords in self.fields:
            polygon = QPolygonF()
            for x, y in poly_coords:
                polygon.append(QPointF(self.transform_x(x), self.transform_y(y)))
            painter.drawPolygon(polygon)

        # Draw Labels
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        for label, x, y in self.field_labels:
            px = self.transform_x(x)
            py = self.transform_y(y)
            painter.drawText(int(px)-15, int(py)-10, 30, 20, Qt.AlignCenter, label)

        # Draw Axes
        self.draw_axes(painter)
        
        # Draw Data Points
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.red))
        for x, y, label in self.data_points:
            px = self.transform_x(x)
            py = self.transform_y(y)
            painter.drawEllipse(QPointF(px, py), 4, 4)

        # Draw Axis Labels
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        # X Label
        painter.drawText(self.rect().width()//2 - 50, self.rect().height() - 10, 100, 20, Qt.AlignCenter, "SiO2 (wt%)")
        # Y Label
        painter.save()
        painter.translate(20, self.rect().height()//2 + 50)
        painter.rotate(-90)
        painter.drawText(0, 0, 100, 20, Qt.AlignCenter, "Na2O + K2O (wt%)")
        painter.restore()

# ==========================================
# Main Application Window
# ==========================================
from PySide6.QtGui import QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GeoPyTool Lite - Single File Edition")
        self.resize(1000, 800)
        
        self.geo_data = GeoData()
        
        # UI Components
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Toolbar / Menu
        self.toolbar_layout = QHBoxLayout()
        self.btn_load = QPushButton("Load Data (CSV)")
        self.btn_load.clicked.connect(self.load_data)
        self.lbl_status = QLabel("Ready")
        
        self.toolbar_layout.addWidget(self.btn_load)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.lbl_status)
        
        self.layout.addLayout(self.toolbar_layout)
        
        # Main Content Area
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)
        
        # Left: Controls / Info (Placeholder for more options)
        self.info_panel = QFrame()
        self.info_panel.setFrameShape(QFrame.StyledPanel)
        self.info_layout = QVBoxLayout(self.info_panel)
        self.info_layout.addWidget(QLabel("<b>TAS Diagram</b>"))
        self.info_layout.addWidget(QLabel("Total Alkali-Silica classification"))
        self.info_layout.addStretch()
        self.info_layout.addWidget(QLabel("<i>More modules coming soon...</i>"))
        
        # Right: Plot Area
        self.plot_area = TASPlot()
        
        self.splitter.addWidget(self.info_panel)
        self.splitter.addWidget(self.plot_area)
        self.splitter.setSizes([200, 800])

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if filename:
            success = self.geo_data.load_csv(filename)
            if success:
                self.lbl_status.setText(f"Loaded: {filename}")
                self.process_tas_data()
            else:
                QMessageBox.critical(self, "Error", "Failed to load CSV file.")

    def process_tas_data(self):
        # Look for SiO2 and Na2O+K2O columns
        sio2_col = None
        na2o_col = None
        k2o_col = None
        
        # Case-insensitive search
        for col in self.geo_data.headers:
            c = col.lower()
            if 'sio2' in c: sio2_col = col
            if 'na2o' in c: na2o_col = col
            if 'k2o' in c: k2o_col = col
            
        if not sio2_col:
            QMessageBox.warning(self, "Data Error", "Could not find 'SiO2' column.")
            return

        sio2 = self.geo_data.get_numeric_column(sio2_col)
        alkali = []
        
        # Calculate Total Alkali
        if na2o_col and k2o_col:
            na2o = self.geo_data.get_numeric_column(na2o_col)
            k2o = self.geo_data.get_numeric_column(k2o_col)
            alkali = [n + k for n, k in zip(na2o, k2o)]
        else:
             QMessageBox.warning(self, "Data Error", "Could not find Na2O and K2O columns.")
             return

        # Update Plot
        self.plot_area.data_points = []
        for x, y in zip(sio2, alkali):
            if x > 0 and y > 0:
                self.plot_area.data_points.append((x, y, "Point"))
        
        self.plot_area.update()
        self.lbl_status.setText(f"Plotting {len(self.plot_area.data_points)} points.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
