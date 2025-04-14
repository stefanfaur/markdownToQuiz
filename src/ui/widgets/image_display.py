from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
import requests
from typing import Optional
from urllib.parse import urlparse
import os

class ImageDisplay(QWidget):
    """Widget for displaying images with automatic scaling and caching."""
    
    CACHE_DIR = os.path.expanduser("~/.cache/markdownToQuiz/images")
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.init_ui()
        self.setup_cache_dir()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMinimumSize(QSize(200, 100))
        layout.addWidget(self.image_label)
        
        # Alt text label
        self.alt_text_label = QLabel()
        self.alt_text_label.setAlignment(Qt.AlignCenter)
        self.alt_text_label.setStyleSheet("""
            QLabel {
                color: #75715E;
                padding: 5px;
                font-style: italic;
            }
        """)
        layout.addWidget(self.alt_text_label)
        
    def setup_cache_dir(self):
        """Create cache directory if it doesn't exist."""
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
            
    def get_cached_path(self, url: str) -> str:
        """Get the cached file path for a URL."""
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            filename = url.replace('://', '_').replace('/', '_')
        return os.path.join(self.CACHE_DIR, filename)
            
    def load_image(self, source: str, alt_text: str = ''):
        """Load and display an image from a URL or local path."""
        if not source:
            self.clear()
            return
            
        self.alt_text_label.setText(alt_text if alt_text else '')
        
        try:
            if source.startswith(('http://', 'https://')):
                # Check cache first
                cache_path = self.get_cached_path(source)
                if os.path.exists(cache_path):
                    pixmap = QPixmap(cache_path)
                else:
                    # Download and cache the image
                    response = requests.get(source)
                    image = QImage()
                    image.loadFromData(response.content)
                    image.save(cache_path)
                    pixmap = QPixmap.fromImage(image)
            else:
                # Local file
                pixmap = QPixmap(source)
                
            if pixmap.isNull():
                self.show_error("Failed to load image")
                return
                
            # Scale the image to fit the widget while maintaining aspect ratio
            scaled_pixmap = self.scale_image(pixmap)
            self.image_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.show_error(f"Error loading image: {str(e)}")
            
    def scale_image(self, pixmap: QPixmap) -> QPixmap:
        """Scale the image to fit the widget while maintaining aspect ratio."""
        available_size = self.image_label.size()
        return pixmap.scaled(
            available_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
    def show_error(self, message: str):
        """Display an error message instead of the image."""
        self.image_label.setText(message)
        self.image_label.setStyleSheet("""
            QLabel {
                color: #F92672;
                padding: 10px;
                border: 1px solid #F92672;
                border-radius: 5px;
            }
        """)
        
    def clear(self):
        """Clear the displayed image and alt text."""
        self.image_label.clear()
        self.alt_text_label.clear()
        
    def resizeEvent(self, event):
        """Handle widget resize events to scale the image appropriately."""
        super().resizeEvent(event)
        if self.image_label.pixmap():
            original_pixmap = self.image_label.pixmap()
            scaled_pixmap = self.scale_image(original_pixmap)
            self.image_label.setPixmap(scaled_pixmap)
