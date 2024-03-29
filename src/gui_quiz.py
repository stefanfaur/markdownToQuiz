import sys
import random
from typing import List
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit, QFileDialog, QDialog, QCheckBox, QDialogButtonBox, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


from parse_md import parse_markdown, Chapter, Question


class ChapterSelectionDialog(QDialog):
    def __init__(self, chapters, parent=None):
        super().__init__(parent)
        self.chapters = chapters
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Chapters')
        layout = QVBoxLayout(self)

        self.groupBox = QGroupBox("Chapters")
        groupBoxLayout = QVBoxLayout()

        self.checkboxes = []
        for chapter in self.chapters:
            checkbox = QCheckBox(chapter.title)
            self.checkboxes.append(checkbox)
            groupBoxLayout.addWidget(checkbox)

        self.groupBox.setLayout(groupBoxLayout)
        layout.addWidget(self.groupBox)

        # Buttons for select all and deselect all
        self.selectAllButton = QPushButton("Select All", self)
        self.selectAllButton.clicked.connect(self.selectAll)
        layout.addWidget(self.selectAllButton)

        self.deselectAllButton = QPushButton("Deselect All", self)
        self.deselectAllButton.clicked.connect(self.deselectAll)
        layout.addWidget(self.deselectAllButton)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def selectAll(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselectAll(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def getSelectedChapters(self):
        self.selected_chapters = [self.chapters[i] for i, cb in enumerate(self.checkboxes) if cb.isChecked()]
        return self.selected_chapters

    

class AnswerEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.parent.submitButton.isVisible():
                self.parent.submitAnswer()
            elif self.parent.nextQuestionButton.isVisible():
                self.parent.showNextQuestion()
        else:
            super().keyPressEvent(event)

class Quiz:
    def __init__(self, chapters: List[Chapter]):
        self.chapters = chapters
        self.questions = [q for chapter in chapters for q in chapter.questions]
        random.shuffle(self.questions)
        self.total_questions = len(self.questions)
        self.current_question_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0

    def get_next_question(self):
        if self.current_question_index < self.total_questions:
            return self.questions[self.current_question_index]
        return None

    def submit_answer(self, answer):
        no_option_question = self.questions[self.current_question_index].options is None
        question = self.questions[self.current_question_index]
        is_correct = (answer == question.correct_answer_tag)
        if is_correct and not no_option_question:
            self.correct_answers += 1
        elif not no_option_question:
            self.wrong_answers += 1
        self.current_question_index += 1
        return is_correct

    def get_results(self):
        return (self.correct_answers, self.wrong_answers, self.total_questions)

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.quiz = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz Application')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        self.loadFileButton = QPushButton("Load Markdown File", self)
        self.loadFileButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadFileButton)

        self.questionLabel = QLabel("")
        self.questionLabel.setWordWrap(True)
        layout.addWidget(self.questionLabel)

        self.answerEdit = AnswerEdit(self)
        layout.addWidget(self.answerEdit)

        self.submitButton = QPushButton("Submit Answer", self)
        self.submitButton.clicked.connect(self.submitAnswer)
        layout.addWidget(self.submitButton)

        self.nextQuestionButton = QPushButton("Next Question", self)
        self.nextQuestionButton.clicked.connect(self.showNextQuestion)
        layout.addWidget(self.nextQuestionButton)

        self.feedbackEdit = QTextEdit()
        self.feedbackEdit.setReadOnly(True)
        layout.addWidget(self.feedbackEdit)

        self.reloadMarkdownButton = QPushButton("Reload Markdown File", self)
        self.reloadMarkdownButton.clicked.connect(self.reloadMarkdownFile)
        layout.addWidget(self.reloadMarkdownButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
        self.statusBar = self.statusBar()  # Initialize the status bar

        # Initially hide elements except for the load file button
        self.hideQuizElements()

    def updateStatusBar(self):
        if self.quiz:
            answered = self.quiz.current_question_index
            correct = self.quiz.correct_answers
            wrong = self.quiz.wrong_answers
            total = self.quiz.total_questions
            status_text = f"Answered: {answered}/{total} | Correct: {correct} | Wrong: {wrong}"
            self.statusBar.showMessage(status_text)

    def hideQuizElements(self):
        self.questionLabel.hide()
        self.answerEdit.hide()
        self.submitButton.hide()
        self.nextQuestionButton.hide()
        self.feedbackEdit.hide()
        self.reloadMarkdownButton.hide()
        
    def showQuizElements(self):
        self.questionLabel.show()
        self.answerEdit.show()
        self.submitButton.show()
        self.feedbackEdit.show()
        self.reloadMarkdownButton.show()
        self.loadFileButton.hide()

    def loadFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md)", options=options)
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                md_content = file.read()
            parsed_chapters = parse_markdown(md_content)
            dialog = ChapterSelectionDialog(parsed_chapters, self)
            if dialog.exec_() == QDialog.Accepted:
                selected_chapters = dialog.getSelectedChapters()
                if selected_chapters:
                    self.quiz = Quiz(selected_chapters)
                    self.showQuizElements()
                    self.showNextQuestion()
                else:
                    self.quiz = None
                    self.hideQuizElements()

    def startQuiz(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md)", options=options)
        if filename:
            with open(filename, 'r') as file:
                md_content = file.read()
            parsed_chapters = parse_markdown(md_content)
            self.quiz = Quiz(parsed_chapters)
            self.showNextQuestion()

    def reloadMarkdownFile(self):
        self.quiz = Quiz(self.quiz.chapters)
        self.questionLabel.setText("")
        self.answerEdit.clear()
        self.startQuiz()

    def showNextQuestion(self):
        self.answerEdit.clear()
        self.feedbackEdit.clear()
        if self.quiz:
            question = self.quiz.get_next_question()
            if question:
                display_text = f"<span style='color: lightblue; font-weight: bold;'>{question.text}</span>"
                if question.options:
                    for option in question.options:
                        display_text += f"<hr><span style='color: lightgreen;'>{option[0]}: {option[1]}</span>"
                self.questionLabel.setText(display_text)
                self.submitButton.show()
                self.nextQuestionButton.hide()
                self.updateStatusBar()
            else:
                correct, wrong, total = self.quiz.get_results()
                self.questionLabel.setText(f"Quiz Finished!\nCorrect Answers: {correct}\nWrong Answers: {wrong}\nTotal Questions: {total}")
                self.hideQuizElements()
                self.loadFileButton.show()


    def submitAnswer(self):
        if self.quiz:
            user_answer = self.answerEdit.toPlainText().strip().upper()
            is_correct = self.quiz.submit_answer(user_answer)
            self.showFeedback(is_correct)
            self.submitButton.hide()
            self.nextQuestionButton.show()
            self.updateStatusBar()

    def showFeedback(self, is_correct):
        question = self.quiz.questions[self.quiz.current_question_index - 1]
        if question.options:
            feedback_text = f"Correct answer: {question.correct_answer}\n"
            feedback_text += "Your answer is correct!" if is_correct else "Your answer is incorrect."
        else:
            feedback_text = f"{question.correct_answer}\n"
        self.feedbackEdit.setText(feedback_text)
        
def applyDarkTheme(app):
    app.setStyle("Fusion")

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53)) 
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    applyDarkTheme(app)
    font = QFont("Courier", 16)
    app.setFont(font)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
