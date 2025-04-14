from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from dataclasses import dataclass
from typing import Dict

@dataclass
class ThemeColors:
    """Define colors for a theme."""
    background: str
    foreground: str
    accent: str
    accent_light: str
    accent_dark: str
    error: str
    success: str
    warning: str
    inactive: str

class Theme:
    """Theme configuration for the application."""
    
    # Monokai-inspired dark theme (default)
    DARK = ThemeColors(
        background="#272822",
        foreground="#F8F8F2",
        accent="#66D9EF",
        accent_light="#A6E22E",
        accent_dark="#49483E",
        error="#F92672",
        success="#A6E22E",
        warning="#FD971F",
        inactive="#75715E"
    )
    
    @staticmethod
    def apply_theme(app, colors: ThemeColors = DARK):
        """Apply theme colors to the application."""
        app.setStyle("Fusion")
        
        # Create and configure dark palette
        palette = QPalette()
        
        # Basic colors
        palette.setColor(QPalette.Window, QColor(colors.background))
        palette.setColor(QPalette.WindowText, QColor(colors.foreground))
        palette.setColor(QPalette.Base, QColor(colors.background))
        palette.setColor(QPalette.AlternateBase, QColor(colors.accent_dark))
        palette.setColor(QPalette.ToolTipBase, QColor(colors.background))
        palette.setColor(QPalette.ToolTipText, QColor(colors.foreground))
        palette.setColor(QPalette.Text, QColor(colors.foreground))
        palette.setColor(QPalette.Button, QColor(colors.accent_dark))
        palette.setColor(QPalette.ButtonText, QColor(colors.foreground))
        palette.setColor(QPalette.BrightText, QColor(colors.accent_light))
        
        # Links
        palette.setColor(QPalette.Link, QColor(colors.accent))
        palette.setColor(QPalette.LinkVisited, QColor(colors.accent))
        
        # Selection
        palette.setColor(QPalette.Highlight, QColor(colors.accent))
        palette.setColor(QPalette.HighlightedText, QColor(colors.background))
        
        # Disabled state
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(colors.inactive))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(colors.inactive))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(colors.inactive))
        
        app.setPalette(palette)
        
        # Global stylesheet
        app.setStyleSheet(f"""
            QToolTip {{
                color: {colors.foreground};
                background-color: {colors.background};
                border: 1px solid {colors.accent};
                padding: 5px;
            }}
            
            QPushButton {{
                background-color: {colors.accent_dark};
                color: {colors.foreground};
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }}
            
            QPushButton:hover {{
                background-color: {colors.accent};
            }}
            
            QPushButton:disabled {{
                background-color: {colors.inactive};
                color: {colors.background};
            }}
            
            QLineEdit, QTextEdit {{
                background-color: {colors.background};
                color: {colors.foreground};
                border: 1px solid {colors.accent_dark};
                border-radius: 3px;
                padding: 5px;
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {colors.accent};
            }}
            
            QLabel {{
                color: {colors.foreground};
            }}
            
            QMenuBar {{
                background-color: {colors.background};
                color: {colors.foreground};
            }}
            
            QMenuBar::item:selected {{
                background-color: {colors.accent_dark};
            }}
            
            QMenu {{
                background-color: {colors.background};
                color: {colors.foreground};
            }}
            
            QMenu::item:selected {{
                background-color: {colors.accent_dark};
            }}
            
            QProgressBar {{
                border: 1px solid {colors.accent_dark};
                border-radius: 3px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {colors.accent};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background-color: {colors.background};
                width: 10px;
                margin: 0;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {colors.accent_dark};
                min-height: 20px;
                border-radius: 5px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            
            QScrollBar:horizontal {{
                border: none;
                background-color: {colors.background};
                height: 10px;
                margin: 0;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {colors.accent_dark};
                min-width: 20px;
                border-radius: 5px;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
            }}
        """)
