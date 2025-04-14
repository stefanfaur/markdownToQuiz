from dataclasses import dataclass, field
from typing import List, Optional, Dict
import random
from .chapter import Chapter
from .question import Question

@dataclass
class QuizStats:
    """Statistics for quiz progress and performance."""
    total_questions: int = 0
    answered_questions: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    mcq_answered: int = 0  # Count only multiple-choice questions answered
    # Chapter stats format: { 'total': int, 'answered': int, 'correct': int, 'wrong': int, 'mcq_answered': int }
    chapter_stats: Dict[str, Dict[str, int]] = field(default_factory=dict)

    @property
    def completion_percentage(self) -> float:
        """Returns the percentage of questions answered."""
        if self.total_questions == 0:
            return 0.0
        return (self.answered_questions / self.total_questions) * 100

    @property
    def accuracy_percentage(self) -> float:
        """Returns the percentage of correctly answered multiple-choice questions."""
        if self.mcq_answered == 0:
            return 0.0
        return (self.correct_answers / self.mcq_answered) * 100

@dataclass
class Quiz:
    """Manages the state and logic of a quiz session."""
    chapters: List[Chapter]
    shuffle: bool = True
    _questions: List[Question] = field(init=False, default_factory=list)
    _current_index: int = field(default=0, init=False)
    stats: QuizStats = field(default_factory=QuizStats, init=False)

    def __post_init__(self):
        """Initialize the quiz by preparing questions and statistics."""
        # Collect questions from chapters
        self._questions = []
        for chapter in self.chapters:
            self._questions.extend(chapter.questions)
        
        if self.shuffle:
            random.shuffle(self._questions)
        
        # Initialize statistics
        self.stats = QuizStats()
        self.stats.total_questions = len(self._questions)
        
        # Initialize chapter statistics
        for chapter in self.chapters:
            self.stats.chapter_stats[chapter.title] = {
                'total': chapter.question_count,
                'answered': 0,
                'correct': 0,
                'wrong': 0,
                'mcq_answered': 0  # Initialize chapter MCQ answered count
            }

    @property
    def current_question(self) -> Optional[Question]:
        """Returns the current question or None if quiz is finished."""
        if self._current_index >= len(self._questions):
            return None
        return self._questions[self._current_index]

    @property
    def questions(self) -> List[Question]:
        """Get all questions in the quiz."""
        return self._questions

    def _find_chapter_for_question(self, question: Question) -> Optional[Chapter]:
        """Find the chapter containing the given question."""
        for chapter in self.chapters:
            if question in chapter.questions:
                return chapter
        return None

    def submit_answer(self, answer: str) -> Optional[bool]:
        """Submit an answer for the current question.
        Returns:
        - True: Multiple choice question answered correctly
        - False: Multiple choice question answered incorrectly
        - None: Text-based question, no automatic validation
        """
        if not self.current_question:
            raise ValueError("No current question available")

        question = self.current_question
        chapter = self._find_chapter_for_question(question)
        
        # Always increment answered questions
        self.stats.answered_questions += 1
        chapter_stats = self.stats.chapter_stats[chapter.title]
        chapter_stats['answered'] += 1
        
        is_correct = question.check_answer(answer)
        
        # Only update stats for multiple choice questions
        if is_correct is not None:  # Multiple choice question
            self.stats.mcq_answered += 1 # Increment MCQ answered count
            chapter_stats['mcq_answered'] += 1 # Increment chapter MCQ answered count
            if is_correct:
                self.stats.correct_answers += 1
                chapter_stats['correct'] += 1
            else:
                self.stats.wrong_answers += 1
                chapter_stats['wrong'] += 1

        self._current_index += 1
        return is_correct

    def skip_question(self) -> None:
        """Skip the current question without answering."""
        if not self.current_question:
            raise ValueError("No current question available")
        self._current_index += 1

    def reset(self) -> None:
        """Reset the quiz to its initial state."""
        self._current_index = 0
        if self.shuffle:
            random.shuffle(self._questions)
        
        self.stats.total_questions = len(self._questions)
        self.stats.answered_questions = 0
        self.stats.correct_answers = 0
        self.stats.wrong_answers = 0
        self.stats.mcq_answered = 0 # Reset MCQ count
        
        # Reset chapter statistics
        for chapter in self.chapters:
            self.stats.chapter_stats[chapter.title] = {
                'total': chapter.question_count,
                'answered': 0,
                'correct': 0,
                'wrong': 0,
                'mcq_answered': 0 # Reset chapter MCQ count
            }

    @property
    def is_finished(self) -> bool:
        """Check if all questions have been answered."""
        return self._current_index >= len(self._questions)

    def get_remaining_count(self) -> int:
        """Get the number of remaining questions."""
        return len(self._questions) - self._current_index
