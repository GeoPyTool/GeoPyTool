# AGENTS.md - Guidelines for Coding Agents

This document provides guidance for AI coding agents working on the GeoPyTool codebase.

## Project Overview

GeoPyTool is a cross-platform geochemistry data analysis toolkit containing:
- **geopytool/**: Original version (PyQt5)
- **geopytool_reborn/**: Restructured version (PySide6)
- **geopytoollite/**: Lite version (BeeWare Briefcase)

## Build/Lint/Test Commands

### Installation

```bash
pip install -r requirements.txt
pip install -e .                    # Install original geopytool
cd geopytool_reborn && pip install -e .  # Install reborn version
```

### Running the Application

```bash
python run.py                       # Run original geopytool
cd geopytool_reborn && python -m geopytool_reborn
cd geopytoollite && briefcase dev   # Run lite version
```

### Testing

```bash
pytest                              # Run all tests
pytest tests/test_specific.py       # Run single test file
pytest tests/test_specific.py::test_function_name  # Run single test
pytest -v tests/                    # Verbose output
```

### Building

```bash
python setup.py sdist --formats=zip  # Build source distribution
cd geopytoollite && briefcase create && briefcase build && briefcase run
```

### Linting (Recommended, not configured)

```bash
mypy geopytool_reborn/src/          # Type checking
black geopytool_reborn/src/          # Code formatting
```

## Code Style Guidelines

### File Headers

```python
# -*- coding: utf-8 -*-
"""Module docstring describing purpose."""
```

### Imports (3 groups: stdlib, third-party, local)

```python
import os
from typing import Optional, List

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QMainWindow

from .core.base_widget import BasePlotWindow
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `TASWindow`, `DataCleaner` |
| Functions/Methods | snake_case | `clean_data()`, `plot_points()` |
| Variables | snake_case | `total_alkali` |
| Constants | UPPER_SNAKE_CASE | `VERSION`, `TAS_FIELDS` |
| Private methods | _underscore | `_init_field_paths()` |

### Class Structure

```python
class DiagramWindow(BasePlotWindow):
    """Brief description. Required columns: SiO2, Na2O, K2O"""
    
    title = "Diagram Name"
    reference = "Reference citation"
    items_to_check = ['SiO2', 'Na2O', 'K2O']
    
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
    
    def plot(self):
        """Draw the diagram."""
        pass
```

### Type Hints (for geopytool_reborn)

```python
def clean_data(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    pass
```

### Error Handling

```python
try:
    df = pd.read_excel(filepath, engine='openpyxl')
except Exception as e:
    QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
    return
```

### Data Column Conventions

| Column | Description |
|--------|-------------|
| `SiO2`, `Al2O3`, etc. | Major oxides (wt%) |
| `Label` | Sample identifier for legend |
| `Marker` | Matplotlib marker style (default: 'o') |
| `Color` | Point color (default: 'red') |
| `Size` | Point size (default: 20) |
| `Alpha` | Transparency 0-1 (default: 0.7) |

### Qt/GUI Patterns

- Use PySide6 for new code (geopytool_reborn), PyQt5 for legacy code
- Signal/slot: `self.button.clicked.connect(self.on_click)`

### Matplotlib Patterns

```python
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

self.fig = Figure((10.0, 8.0), dpi=100)
self.canvas = FigureCanvas(self.fig)
self.axes = self.fig.add_subplot(111)
```

## Project Structure

```
GeoPyTool/
├── geopytool/                 # Original (PyQt5)
│   ├── app.py, CustomClass.py, TAS.py, REE.py, ...
├── geopytool_reborn/          # Restructured (PySide6)
│   └── src/geopytool_reborn/
│       ├── app.py             # Main window
│       ├── core/              # base_widget, data_model, geometry
│       ├── diagrams/          # tas, ree, trace, harker, pearce
│       └── resources/         # Constants, standards
├── geopytoollite/             # Lite version
├── DataFileSamples/           # Sample data files
└── requirements.txt
```

## Key Dependencies

numpy, pandas, matplotlib, scipy, PySide6 (new) / PyQt5 (legacy), scikit-learn, openpyxl

## Important Notes

1. **Do not add comments** unless explicitly requested
2. Makefile is for Sphinx documentation, not main build
3. Use `Tool` class mixin for coordinate transformations (triangular diagrams)
4. Geochemical data templates are in `DataFileSamples/`