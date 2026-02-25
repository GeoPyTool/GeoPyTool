# -*- coding: utf-8 -*-
"""
Base widget module - Base classes for plot windows and custom widgets.
"""

import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QCheckBox, QSlider, QLabel, QTextEdit,
    QFileDialog, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from .geometry import Tool
from .data_model import DataCleaner


class GrowingTextEdit(QTextEdit):
    """
    A QTextEdit that grows with its content up to a maximum height.
    
    Useful for reference text or notes that should expand as needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self._size_change)
        self.heightMin = 0
        self.heightMax = 100

    def _size_change(self):
        doc_height = self.document().size().height()
        if self.heightMin <= doc_height <= self.heightMax:
            self.setMinimumHeight(int(doc_height))


class BasePlotWindow(QMainWindow, Tool):
    """
    Base class for all plotting windows in GeoPyTool.
    
    Provides:
    - Matplotlib figure and canvas setup
    - Navigation toolbar
    - Data cleaning functionality
    - Common UI elements (save button, reference textbox)
    - Image/data export capabilities
    
    Subclasses should override:
    - create_controls(): Add diagram-specific controls
    - plot(): Implement the actual plotting logic
    """

    # Override these in subclasses
    title = "Base Plot Window"
    reference = ""
    items_to_check = []
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.title)
        self._df = df
        self._df_backup = df.copy()
        self._changed = len(df) > 0
        
        # Data cleaner
        self.data_cleaner = DataCleaner(self.items_to_check)
        
        # Filename hint for saving
        self.filename_hint = self.title.replace(' ', '_')
        
        # Setup UI
        self._create_main_frame()
        self._create_status_bar()
        
        # Clean data if provided
        if not df.empty:
            self._df = self.data_cleaner.clean(df, self.items_to_check)
            self._df = self.data_cleaner.ensure_style_columns(self._df)

    @property
    def df(self):
        """Get the current DataFrame."""
        return self._df

    @df.setter
    def df(self, value):
        """Set a new DataFrame and trigger replot."""
        self._df = self.data_cleaner.clean(value, self.items_to_check)
        self._df = self.data_cleaner.ensure_style_columns(self._df)
        self._changed = True
        self.plot()

    def _create_main_frame(self):
        """Create the main frame with canvas and toolbar."""
        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        
        # Create figure and canvas
        self.fig = Figure((12.0, 9.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.15, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        
        # Navigation toolbar
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Save button
        self.save_button = QPushButton('&Save Image')
        self.save_button.clicked.connect(self.save_image)
        
        # Layout
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.save_button)
        
        # Call subclass method to add custom controls
        self.create_controls()
        
        self.control_layout.addStretch()
        
        # Reference textbox
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        self.textbox.setReadOnly(True)
        
        # Main layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.control_layout)
        self.vbox.addWidget(self.textbox)
        
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def _create_status_bar(self):
        """Create the status bar."""
        self.statusBar().showMessage("Ready")

    def create_controls(self):
        """
        Override in subclasses to add diagram-specific controls.
        
        Add widgets to self.control_layout
        """
        pass

    def plot(self):
        """
        Override in subclasses to implement plotting logic.
        
        Clear self.axes and draw the diagram.
        Call self.canvas.draw() at the end.
        """
        pass

    def save_image(self):
        """Save the current figure to a file."""
        file_filter = "PDF Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)"
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save Image', self.filename_hint, file_filter
        )
        
        if filename:
            try:
                self.canvas.print_figure(filename, dpi=300)
                self.statusBar().showMessage(f"Saved to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def show_error(self, text=''):
        """Show an error message dialog."""
        if not text:
            text = ("Data does not match this function.\n"
                    "Check for missing columns or non-numeric values.")
        QMessageBox.warning(self, "Warning", text)

    def get_unique_labels(self):
        """Get list of unique labels from the data."""
        if 'Label' not in self._df.columns:
            return []
        return self._df['Label'].dropna().unique().tolist()

    def draw_line(self, points, color='grey', linewidth=0.5, linestyle='-', 
                  label='', alpha=0.5, ax=None):
        """
        Draw a line from a list of points.
        
        Args:
            points: List of (x, y) tuples
            color: Line color
            linewidth: Line width
            linestyle: Line style
            label: Line label for legend
            alpha: Transparency
            ax: Axes to draw on (defaults to self.axes)
        """
        if ax is None:
            ax = self.axes
        
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        ax.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, 
                label=label, alpha=alpha)

    def plot_data_points(self, ax, x_col, y_col, df=None, show_legend=True):
        """
        Plot data points from DataFrame columns with styling.
        
        Args:
            ax: Matplotlib axes
            x_col: Column name for X values
            y_col: Column name for Y values
            df: DataFrame (defaults to self._df)
            show_legend: Whether to add labels for legend
        """
        if df is None:
            df = self._df
        
        if df.empty:
            return
        
        seen_labels = set()
        
        for idx, row in df.iterrows():
            try:
                x = row.get(x_col)
                y = row.get(y_col)
                
                if pd.isna(x) or pd.isna(y):
                    continue
                
                label = str(row.get('Label', ''))
                
                # Only use label for legend if not seen before
                if show_legend and label and label not in seen_labels:
                    plot_label = label
                    seen_labels.add(label)
                else:
                    plot_label = "_nolegend_"
                
                ax.scatter(
                    x, y,
                    label=plot_label,
                    marker=row.get('Marker', 'o'),
                    c=row.get('Color', 'red'),
                    s=row.get('Size', 20),
                    alpha=row.get('Alpha', 0.7),
                    edgecolors='none'
                )
            except Exception:
                pass
