#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from .ui import QuizApp
from .ui.themes import Theme, ThemeColors

def main():
    """Main entry point for the Markdown Quiz application."""
    try:
        app = QApplication(sys.argv)
        
        # Set application-wide font
        font = QFont("Segoe UI", 11)  # Modern font with good readability
        app.setFont(font)
        
        # Apply the dark theme
        Theme.apply_theme(app)
        
        # Create and show the main window
        main_window = QuizApp()
        main_window.show()
        
        # Start the event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
