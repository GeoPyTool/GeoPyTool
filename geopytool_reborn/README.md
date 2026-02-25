# GeoPyTool Reborn

A restructured and modernized version of GeoPyTool - a comprehensive geochemistry data analysis toolkit.

## Features

- **TAS Diagram**: Total Alkali-Silica classification for volcanic/plutonic rocks
- **REE Spider Diagram**: Rare Earth Element patterns with multiple normalization standards
- **Trace Element Diagram**: Multi-element spider diagrams
- **Harker Diagrams**: Major element variation diagrams
- **Pearce Diagrams**: Tectonic discrimination diagrams for granites
- **QAPF/QFL Diagrams**: Triangular classification diagrams
- **PCA**: Principal Component Analysis
- **Cluster Analysis**: Hierarchical and K-means clustering
- **Statistics**: Descriptive statistics and distribution analysis

## Installation

### Development Mode

```bash
cd geopytool_reborn
pip install -e .
python -m geopytool_reborn
```

### Using Briefcase

```bash
# Install briefcase
pip install briefcase

# Run in development mode
cd geopytool_reborn
briefcase dev

# Build standalone application
briefcase build

# Package for distribution
briefcase package
```

## Requirements

- Python >= 3.8
- PySide6 >= 6.4.0
- numpy >= 1.20.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0
- scipy >= 1.7.0
- scikit-learn >= 1.0.0
- openpyxl >= 3.0.0

## License

GNU General Public License v3.0

## Credits

Original GeoPyTool by cycleuser (cycleuser@cycleuser.org)
