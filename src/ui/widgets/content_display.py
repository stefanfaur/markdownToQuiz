from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt5.QtCore import Qt
from typing import List, Optional

from ...models import ContentBlock, ContentType
from .code_display import CodeDisplay
from .image_display import ImageDisplay

class ContentDisplay(QWidget):
    """Widget for displaying mixed content types (text, code, images)."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(5)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(scroll)
        
        # Style
        self.setStyleSheet("""
            QLabel {
                color: #F8F8F2;
                font-size: 14px;
            }
            QScrollArea {
                background-color: transparent;
            }
            QWidget#content_widget {
                background-color: transparent;
            }
        """)
        self.content_widget.setObjectName("content_widget")
        
    def clear(self):
        """Clear all content from the display."""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def display_content(self, blocks: List[ContentBlock]):
        self.clear()
        
        for block in blocks:
            if block.type == ContentType.TEXT:
                spacer = QWidget()
                spacer.setFixedHeight(5)
                self.content_layout.addWidget(spacer)
                self._add_text_block(block)
            elif block.type == ContentType.CODE:
                # Add minimal spacing before code
                spacer = QWidget()
                spacer.setFixedHeight(5)
                self.content_layout.addWidget(spacer)
                self._add_code_block(block)
            elif block.type == ContentType.IMAGE:
                self._add_image_block(block)
                
    def _add_text_block(self, block: ContentBlock):
        label = QLabel(block.content)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setStyleSheet("font-size: 14px; line-height: 1.4;")
        self.content_layout.addWidget(label)
        
    def _add_code_block(self, block: ContentBlock):
        code_display = CodeDisplay()
        language = block.metadata.get('language', 'text')
        code_display.set_code(block.content, language)
        self.content_layout.addWidget(code_display)
        
    def _add_image_block(self, block: ContentBlock):
        image_display = ImageDisplay()
        alt_text = block.metadata.get('alt_text', '')
        image_display.load_image(block.content, alt_text)
        self.content_layout.addWidget(image_display)
        
    def add_spacing(self, height: int = 15):
        spacer = QWidget()
        spacer.setFixedHeight(height)
        self.content_layout.addWidget(spacer)
