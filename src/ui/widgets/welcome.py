from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                            QListWidget, QListWidgetItem, QFrame, QHBoxLayout,
                            QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os

class WelcomeWidget(QWidget):
    """Welcome screen widget showing app info and file loading options."""
    
    loadFile = pyqtSignal()  # Signal emitted when load button is clicked
    loadRecentFile = pyqtSignal(str)  # Signal emitted with path when recent file is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Center container
        center_container = QFrame()
        center_container.setObjectName("welcomeContainer")
        center_container.setStyleSheet("""
            QFrame#welcomeContainer {
                background-color: #2D2D2D;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        center_layout = QVBoxLayout(center_container)
        center_layout.setSpacing(30)
        
        # Title
        title_label = QLabel("Markdown Quiz")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #66D9EF;")
        center_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Welcome to Markdown Quiz!\n\n"
            "Load a markdown file to start the quiz. Your file should contain "
            "chapters with questions, options, and answers.\n\n"
            "The quiz supports code blocks with syntax highlighting and images."
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #F8F8F2; font-size: 14px;")
        center_layout.addWidget(desc_label)
        
        # Load button
        load_button = QPushButton("Load Markdown File")
        load_button.setMinimumHeight(50)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #66D9EF;
                color: #272822;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A6E22E;
            }
        """)
        load_button.clicked.connect(self.loadFile.emit)
        
        # Button container for centering
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(load_button)
        button_layout.addStretch()
        center_layout.addWidget(button_container)
        
        # Recent files section
        self.recent_files_list = QListWidget()
        self.recent_files_list.setMaximumHeight(150)
        self.recent_files_list.setStyleSheet("""
            QListWidget {
                background-color: #272822;
                border: 1px solid #49483E;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                color: #F8F8F2;
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #49483E;
            }
            QListWidget::item:selected {
                background-color: #66D9EF;
                color: #272822;
            }
        """)
        self.recent_files_list.itemClicked.connect(
            lambda item: self.loadRecentFile.emit(item.data(Qt.UserRole))
        )
        
        recent_label = QLabel("Recent Files:")
        recent_label.setStyleSheet("color: #F8F8F2; font-weight: bold;")
        
        center_layout.addWidget(recent_label)
        center_layout.addWidget(self.recent_files_list)
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #75715E;")
        center_layout.addWidget(version_label)
        
        # Add center container to main layout
        layout.addStretch()
        layout.addWidget(center_container)
        layout.addStretch()
        
    def update_recent_files(self, files: list[str]):
        """Update the recent files list."""
        self.recent_files_list.clear()
        for file_path in files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            item.setToolTip(file_path)
            self.recent_files_list.addItem(item)
