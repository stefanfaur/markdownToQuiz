from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                            QLabel, QFileDialog, QMessageBox, QProgressBar,
                            QStatusBar, QSplitter, QFrame, QStackedWidget)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QIcon
import os
from typing import Optional, List

from .widgets import (AnswerEdit, ChapterSelectionDialog, ContentDisplay,
                     WelcomeWidget)
from ..models import Quiz, Chapter, Question, ContentBlock, ContentType
from ..parsers import MarkdownParser, ParserError

class QuizApp(QMainWindow):
    """Main application window for the Quiz application."""
    
    def __init__(self):
        super().__init__()
        self.quiz: Optional[Quiz] = None
        self.current_file: Optional[str] = None
        self.settings = QSettings('MarkdownQuiz', 'Quiz Application')
        
        # Create stacked widget for managing screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize UI components
        self.init_welcome_screen()
        self.init_quiz_screen()
        self.init_ui()
        self.load_settings()
        
        # Show welcome screen initially
        self.stacked_widget.setCurrentIndex(0)
        
    def init_welcome_screen(self):
        """Initialize the welcome screen."""
        self.welcome_widget = WelcomeWidget()
        self.welcome_widget.loadFile.connect(self.load_file)
        self.welcome_widget.loadRecentFile.connect(self.load_recent_file)
        self.stacked_widget.addWidget(self.welcome_widget)
        
    def init_quiz_screen(self):
        """Initialize the quiz screen."""
        self.quiz_widget = QWidget()
        layout = QVBoxLayout(self.quiz_widget)
        layout.setSpacing(10)
        
        # Create splitter for content and answer areas
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Content area (top)
        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        
        # Question display
        self.content_display = ContentDisplay()
        content_layout.addWidget(self.content_display)
        
        # Answer area (bottom)
        answer_widget = QFrame()
        answer_layout = QVBoxLayout(answer_widget)
        
        # Answer input
        self.answer_edit = AnswerEdit()
        self.answer_edit.submitAnswer.connect(self.submit_answer)
        self.answer_edit.nextQuestion.connect(self.show_next_question)
        answer_layout.addWidget(self.answer_edit)
        
        # Feedback display
        self.feedback_label = QLabel()
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                border-radius: 5px;
                background-color: #2D2D2D;
            }
        """)
        answer_layout.addWidget(self.feedback_label)
        
        # Add widgets to splitter
        splitter.addWidget(content_widget)
        splitter.addWidget(answer_widget)
        splitter.setStretchFactor(0, 6)  # Content area gets more space
        splitter.setStretchFactor(1, 1)
        
        # Add splitter to main layout
        layout.addWidget(splitter)
        
        # Control buttons
        button_layout = QVBoxLayout()
        
        self.submit_button = QPushButton('Submit Answer')
        self.submit_button.clicked.connect(self.submit_answer)
        button_layout.addWidget(self.submit_button)
        
        self.next_button = QPushButton('Next Question')
        self.next_button.clicked.connect(self.show_next_question)
        self.next_button.hide()
        button_layout.addWidget(self.next_button)
        
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Return to welcome screen button
        self.return_button = QPushButton('Return to Welcome Screen')
        self.return_button.clicked.connect(self.return_to_welcome)
        self.return_button.hide()
        layout.addWidget(self.return_button)
        
        self.stacked_widget.addWidget(self.quiz_widget)
        
    def init_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle('Markdown Quiz')
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(800, 600)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def load_settings(self):
        """Load application settings."""
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
            
        self.recent_files = self.settings.value('recent_files', [])
        self.welcome_widget.update_recent_files(self.recent_files)
        
    def save_settings(self):
        """Save application settings."""
        self.settings.setValue('geometry', self.saveGeometry())
        if self.current_file and self.current_file not in self.recent_files:
            self.recent_files.insert(0, self.current_file)
            self.recent_files = self.recent_files[:5]  # Keep last 5
            self.settings.setValue('recent_files', self.recent_files)
            self.welcome_widget.update_recent_files(self.recent_files)
            
    def load_recent_file(self, file_path: str):
        """Load a quiz from a recent file."""
        if os.path.exists(file_path):
            self.process_file(file_path)
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"File not found: {file_path}"
            )
            # Remove from recent files
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
                self.settings.setValue('recent_files', self.recent_files)
                self.welcome_widget.update_recent_files(self.recent_files)
            
    def load_file(self):
        """Show file dialog and load selected file."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md);;All Files (*)",
            options=options
        )
        
        if filename:
            self.process_file(filename)
            
    def process_file(self, filename: str):
        """Process the selected markdown file."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            parser = MarkdownParser()
            chapters = parser.parse(content)
            
            if not chapters:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No chapters found in the markdown file."
                )
                return
                
            dialog = ChapterSelectionDialog(chapters, self)
            if dialog.exec_():
                selected_chapters = dialog.selected_chapters
                if selected_chapters:
                    # Validate that selected chapters have questions
                    total_questions = sum(len(ch.questions) for ch in selected_chapters)
                    if total_questions == 0:
                        QMessageBox.warning(
                            self,
                            "Error",
                            "Selected chapters contain no questions."
                        )
                        return
                        
                    self.current_file = filename
                    self.start_quiz(selected_chapters)
                    self.save_settings()
                    
        except (IOError, ParserError) as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load file: {str(e)}"
            )
            
    def start_quiz(self, chapters: List[Chapter]):
        """Start a new quiz with the selected chapters."""
        self.quiz = Quiz(chapters)
        self.stacked_widget.setCurrentIndex(1)  # Switch to quiz screen
        self.update_ui_for_quiz()
        self.show_next_question()
        
    def update_ui_for_quiz(self):
        """Update UI elements for quiz mode."""
        self.submit_button.show()
        self.next_button.hide()
        self.return_button.hide()
        self.progress_bar.setMaximum(self.quiz.stats.total_questions)
        self.update_progress()
        
    def update_progress(self):
        """Update progress indicators."""
        if not self.quiz:
            return
            
        stats = self.quiz.stats
        progress = stats.answered_questions
        total = stats.total_questions
        
        # Update progress bar
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(
            f"{progress}/{total} "
            f"(Correct: {stats.correct_answers}, "
            f"Wrong: {stats.wrong_answers})"
        )
        
        # Update status bar
        if progress > 0:
            accuracy = (stats.correct_answers / progress) * 100
            self.status_bar.showMessage(
                f"Accuracy: {accuracy:.1f}% | "
                f"Remaining: {self.quiz.get_remaining_count()}"
            )
            
    def show_next_question(self):
        """Display the next question."""
        if not self.quiz:
            return
            
        question = self.quiz.current_question
        if not question:
            self.show_final_results()
            return
            
        # Clear previous content
        self.content_display.clear()
        
        # Combine question content and options
        all_blocks = []
        
        # Add question content
        all_blocks.extend(question.content_blocks)
        
        # Add options if available
        if question.options:
            # Format options cleanly
            options_text = "<div style='margin-top: 15px'>" + "\n".join(
                f"<div style='margin: 3px 0; padding: 8px 12px; background-color: #2d2d2d; border-radius: 4px'>"
                f"<strong style='color: #66d9ef'>{tag}</strong>) {text}</div>" 
                for tag, text in question.options
            ) + "</div>"
            
            all_blocks.append(
                ContentBlock(type=ContentType.TEXT, content=options_text)
            )
            
        # Display all content in one go
        self.content_display.display_content(all_blocks)
            
        # Reset UI elements
        self.answer_edit.clear()
        self.submit_button.show()
        self.next_button.hide()
        self.return_button.hide()
        self.feedback_label.clear()
        self.answer_edit.setFocus()
        
    def submit_answer(self):
        """Submit the current answer."""
        if not self.quiz or not self.quiz.current_question:
            return
            
        answer = self.answer_edit.toPlainText().strip()
        if not answer:
            return
            
        is_correct = self.quiz.submit_answer(answer)
        self.show_feedback(is_correct)
        self.update_progress()
        
    def show_feedback(self, is_correct: Optional[bool]):
        """Display feedback for the submitted answer."""
        # Retrieve the question that was just answered
        question = self.quiz.questions[self.quiz._current_index - 1]
        
        if is_correct is True:
            feedback_color = "#A6E22E"  # Success green
            feedback_text = "✓ Correct!"
        elif is_correct is False:
            feedback_color = "#F92672"  # Error red
            feedback_text = f"✗ Incorrect. The correct answer is: {question.correct_answer}"
        else: # is_correct is None (Open-ended question)
            feedback_color = "#75715E"  # Neutral/inactive color
            feedback_text = f"Answer noted. Expected answer: {question.correct_answer}"
            
        self.feedback_label.setStyleSheet(f"""
            QLabel {{
                color: {feedback_color};
                padding: 10px;
                border: 1px solid {feedback_color};
                border-radius: 5px;
                background-color: #2D2D2D;
            }}
        """)
        self.feedback_label.setText(feedback_text)
        
        # Update UI elements
        self.submit_button.hide()
        self.next_button.show()
        self.answer_edit.setFeedbackMode(True)
        
    def show_final_results(self):
        """Display the final quiz results."""
        stats = self.quiz.stats
        accuracy = stats.accuracy_percentage # Use the property for correct calculation
        
        # Count open-ended questions answered
        open_ended_answered = stats.answered_questions - stats.mcq_answered
            
        message = (
            f"Quiz completed!\n\n"
            f"Total questions: {stats.total_questions}\n"
            f"Answered: {stats.answered_questions}\n"
            f"  - Multiple Choice: {stats.mcq_answered}\n"
            f"  - Open Ended: {open_ended_answered}\n\n"
            f"Multiple Choice Score:\n"
            f"  - Correct: {stats.correct_answers}\n"
            f"  - Wrong: {stats.wrong_answers}\n"
            f"  - Accuracy: {accuracy:.1f}%\n\n"
            "Chapter breakdown (MCQ Accuracy):\n"
        )
        
        for chapter_title, chapter_stats in stats.chapter_stats.items():
            chapter_mcq_answered = chapter_stats['mcq_answered']
            chapter_correct = chapter_stats['correct']
            chapter_total = chapter_stats['total']
            chapter_answered = chapter_stats['answered']
            
            try:
                # Calculate accuracy based on MCQs answered in this chapter
                chapter_accuracy = (
                    (chapter_correct / chapter_mcq_answered) * 100
                    if chapter_mcq_answered > 0 else 0
                )
            except ZeroDivisionError:
                chapter_accuracy = 0
                
            message += (
                f"\n{chapter_title} ({chapter_answered}/{chapter_total} answered):\n"
                f"- MCQ Accuracy: {chapter_accuracy:.1f}% ({chapter_correct}/{chapter_mcq_answered})\n"
            )
            
        QMessageBox.information(self, "Quiz Results", message)
        
        # Show return button
        self.content_display.clear()
        self.answer_edit.clear()
        self.feedback_label.clear()
        self.submit_button.hide()
        self.next_button.hide()
        self.return_button.show()
        self.status_bar.clearMessage()
        
    def return_to_welcome(self):
        """Return to the welcome screen."""
        self.quiz = None
        self.stacked_widget.setCurrentIndex(0)
        
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        super().closeEvent(event)
