# -*- coding: utf-8 -*-
"""
GeoPyTool Reborn - Main entry point.

Usage:
    python -m geopytool_reborn
    
Or from command line:
    geopytool-reborn
    
For Briefcase packaging:
    briefcase dev
    briefcase build
    briefcase package
"""

import sys
import os


def main():
    """Main entry point for GeoPyTool Reborn (Briefcase compatible)."""
    # Set environment variables before importing Qt
    os.environ.setdefault('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    
    from PySide6.QtWidgets import QApplication
    
    from .app import MainWindow
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("GeoPyTool Reborn")
    app.setOrganizationName("GeoPyTool")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    # Run event loop and return exit code
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
