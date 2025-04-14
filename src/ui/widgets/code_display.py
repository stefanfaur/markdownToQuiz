from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat, QSyntaxHighlighter, QColor
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from typing import Optional

class CodeHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for code blocks using Pygments."""
    
    def __init__(self, parent: QTextEdit, language: str = 'text'):
        super().__init__(parent)
        self.language = language
        
        try:
            self.lexer = get_lexer_by_name(language, stripall=True)
        except:
            self.lexer = TextLexer()
            
        self.formatter = HtmlFormatter(style='monokai')
        
    def highlightBlock(self, text: str):
        """Highlight a block of code using Pygments."""
        html = highlight(text, self.lexer, self.formatter)
        
        # Convert the HTML formatting to QTextCharFormat
        format = QTextCharFormat()
        format.setBackground(QColor('#272822'))  # Monokai background color
        format.setForeground(QColor('#F8F8F2'))  # Monokai default text color
        self.setFormat(0, len(text), format)
        
        # Apply specific syntax highlighting
        block_data = self.currentBlock().text()
        highlighted = highlight(block_data, self.lexer, self.formatter)
        
        # Parse the HTML and apply formatting
        current_pos = 0
        for token, value in self.lexer.get_tokens(block_data):
            format = QTextCharFormat()
            color = self.get_token_color(token)
            format.setForeground(QColor(color))
            format.setFontFamily('Courier')
            self.setFormat(current_pos, len(value), format)
            current_pos += len(value)
            
    def get_token_color(self, token) -> str:
        """Map Pygments tokens to color codes."""
        # Default Monokai color scheme
        COLOR_MAP = {
            'Keyword': '#F92672',
            'String': '#E6DB74',
            'Number': '#AE81FF',
            'Comment': '#75715E',
            'Operator': '#F92672',
            'Name.Function': '#A6E22E',
            'Name.Class': '#A6E22E',
            'Name.Builtin': '#66D9EF',
        }
        
        token_name = str(token)
        for key, color in COLOR_MAP.items():
            if key.lower() in token_name.lower():
                return color
        return '#F8F8F2'  # Default text color

class CodeDisplay(QWidget):
    """Widget for displaying syntax-highlighted code."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Language label
        self.language_label = QLabel()
        self.language_label.setAlignment(Qt.AlignRight)
        self.language_label.setStyleSheet("""
            QLabel {
                color: #75715E;
                padding: 2px 5px;
                background-color: #272822;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
        """)
        layout.addWidget(self.language_label)
        
        # Code editor
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setFont(QFont("Courier", 12))
        self.code_edit.setStyleSheet("""
            QTextEdit {
                background-color: #272822;
                color: #F8F8F2;
                border: 1px solid #49483E;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.code_edit)
        
        self.highlighter = None
        
    def set_code(self, code: str, language: str = 'text'):
        """Set the code content and language for syntax highlighting."""
        self.language_label.setText(language)
        self.code_edit.setText(code)
        
        # Update syntax highlighter
        if self.highlighter:
            self.highlighter.setDocument(None)
        self.highlighter = CodeHighlighter(self.code_edit, language)
        self.highlighter.rehighlight()
        
    def copy_to_clipboard(self):
        """Copy the code content to clipboard."""
        self.code_edit.copy()
