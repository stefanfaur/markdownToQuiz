from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional, Callable

class AnswerEdit(QTextEdit):
    """Custom text edit widget for quiz answers with enhanced keyboard handling."""
    
    submitAnswer = pyqtSignal()  # Signal emitted when enter is pressed
    nextQuestion = pyqtSignal()  # Signal emitted when enter is pressed in feedback mode
    
    def __init__(self, parent: Optional['QWidget'] = None):
        super().__init__(parent)
        self.init_ui()
        self.is_feedback_mode = False
        
    def init_ui(self):
        """Initialize the UI components."""
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #F8F8F2;
                border: 1px solid #49483E;
                border-radius: 5px;
                padding: 10px;
                selection-background-color: #49483E;
            }
            QTextEdit:focus {
                border: 1px solid #66D9EF;
            }
        """)
        
        # Set placeholder text
        self.setPlaceholderText("Type your answer here...")
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        # Check for Enter/Return key
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Don't insert newline
            event.accept()
            
            if not event.modifiers():  # No modifiers (Shift/Ctrl/etc)
                if self.is_feedback_mode:
                    self.nextQuestion.emit()
                else:
                    self.submitAnswer.emit()
                return
                
        # Handle all other keys normally
        super().keyPressEvent(event)
        
    def setFeedbackMode(self, enabled: bool):
        """Toggle feedback mode where Enter triggers next question."""
        self.is_feedback_mode = enabled
        if enabled:
            self.setReadOnly(True)
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #3D3D3D;
                    color: #F8F8F2;
                    border: 1px solid #49483E;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
        else:
            self.setReadOnly(False)
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #F8F8F2;
                    border: 1px solid #49483E;
                    border-radius: 5px;
                    padding: 10px;
                    selection-background-color: #49483E;
                }
                QTextEdit:focus {
                    border: 1px solid #66D9EF;
                }
            """)
            
    def clear(self):
        """Clear the text and reset to input mode."""
        super().clear()
        self.setFeedbackMode(False)
