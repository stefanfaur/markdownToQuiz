from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QCheckBox,
                           QPushButton, QDialogButtonBox, QScrollArea,
                           QWidget, QLabel, QFrame)
from PyQt5.QtCore import Qt
from typing import List, Optional

from ...models import Chapter

class ChapterSelectionDialog(QDialog):
    """Dialog for selecting chapters to include in the quiz."""
    
    def __init__(self, chapters: List[Chapter], parent: Optional['QWidget'] = None):
        super().__init__(parent)
        self.chapters = chapters
        self.selected_chapters: List[Chapter] = []
        self.checkboxes: List[QCheckBox] = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle('Select Chapters')
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2D2D2D;
            }
            QGroupBox {
                border: 1px solid #49483E;
                border-radius: 5px;
                margin-top: 1em;
                color: #F8F8F2;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QCheckBox {
                color: #F8F8F2;
                padding: 5px;
            }
            QCheckBox:hover {
                background-color: #3D3D3D;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #49483E;
                color: #F8F8F2;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #66D9EF;
            }
            QScrollArea {
                border: none;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Add description label
        desc_label = QLabel("Select the chapters you want to include in the quiz:")
        desc_label.setStyleSheet("color: #F8F8F2; padding-bottom: 10px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Create scroll area for chapters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Create content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Create group box for chapters
        self.group_box = QGroupBox("Chapters")
        group_box_layout = QVBoxLayout()
        
        # Add checkboxes for each chapter
        for chapter in self.chapters:
            checkbox = QCheckBox(chapter.title)
            checkbox.setToolTip(f"{len(chapter.questions)} questions")
            self.checkboxes.append(checkbox)
            group_box_layout.addWidget(checkbox)
            
        self.group_box.setLayout(group_box_layout)
        content_layout.addWidget(self.group_box)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Add Select All/None buttons
        button_layout = QVBoxLayout()
        
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(self.select_all_button)
        
        self.deselect_all_button = QPushButton("Deselect All")
        self.deselect_all_button.clicked.connect(self.deselect_all)
        button_layout.addWidget(self.deselect_all_button)
        
        layout.addLayout(button_layout)
        
        # Add dialog buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(self.button_box)
        
        # Connect checkbox state changes to validate selection
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(self.validate_selection)
            
    def select_all(self):
        """Select all chapters."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
            
    def deselect_all(self):
        """Deselect all chapters."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
            
    def validate_selection(self):
        """Validate that at least one chapter is selected."""
        has_selection = any(cb.isChecked() for cb in self.checkboxes)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(has_selection)
        
    def get_selected_chapters(self) -> List[Chapter]:
        """Get the list of selected chapters."""
        return [
            self.chapters[i] 
            for i, checkbox in enumerate(self.checkboxes) 
            if checkbox.isChecked()
        ]
        
    def accept(self):
        """Handle dialog acceptance."""
        self.selected_chapters = self.get_selected_chapters()
        super().accept()
