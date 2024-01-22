import random
from typing import List
from parse_md import parse_markdown, Chapter, Question

class Quiz:
    def __init__(self, chapters: List[Chapter]):
        self.chapters = chapters
        self.total_questions = sum(len(chapter.questions) for chapter in chapters)
        self.answered_questions = 0
        self.correct_answers = 0
        self.wrong_answers = 0

    def start(self):
        print("Welcome to the Quiz!")
        self.select_chapter()

    def select_chapter(self):
        print("Select a chapter:")
        print("0. All Chapters")
        for i, chapter in enumerate(self.chapters, 1):
            print(f"{i}. {chapter.title}")
        chapter_choice = int(input("Enter your choice: "))

        if chapter_choice == 0:
            self.run_quiz(self.chapters)
        else:
            self.run_quiz([self.chapters[chapter_choice - 1]])

    def run_quiz(self, selected_chapters: List[Chapter]):
        questions = [q for chapter in selected_chapters for q in chapter.questions]
        random.shuffle(questions)

        for question in questions:
            self.ask_question(question)

            if self.answered_questions == self.total_questions:
                break

        self.display_results()

    def ask_question(self, question: Question):
        print("\n" + question.text)
        if question.options:
            for option in question.options:
                print(f"{option[0]}: {option[1]}")
            user_answer = input("Your answer: ").upper()
            is_correct = user_answer == question.correct_answer
        else:
            print("Write your answer (press Enter when done):")
            user_answer = input()  # User writes the answer for review
            is_correct = True  # For text answer, we assume the user reviews it

        self.answered_questions += 1
        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1
        self.show_answer_feedback(question, is_correct, user_answer)

    def show_answer_feedback(self, question: Question, is_correct: bool, user_answer: str):
        if question.options:
            print(f"Correct answer: {question.correct_answer}")
        else:
            print(f"The correct answer is: {question.correct_answer}")
        
        if is_correct:
            print("That's correct!")
        else:
            print("That's incorrect.")

    def display_results(self):
        print("\nQuiz Done! Good job boss.")
        print(f"Total Questions: {self.total_questions}")
        print(f"Answered Questions: {self.answered_questions}")
        print(f"Correct Answers: {self.correct_answers}")
        print(f"Wrong Answers: {self.wrong_answers}")

with open('../assets/example.md', 'r') as file:
        md_example = file.read()

# Parse the markdown content
parsed_chapters = parse_markdown(md_example)

# Create and start the quiz
quiz = Quiz(parsed_chapters)
quiz.start() 

