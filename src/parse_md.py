from typing import List, Union
import re

class Question:
    def __init__(self, text: str, options: Union[List[tuple[str, str]], None], correct_answer: str, correct_answer_tag: str):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.correct_answer_tag = correct_answer_tag

    def __repr__(self):
        return f"Question(text={self.text}, options={self.options}, correct_answer={self.correct_answer}, correct_answer_tag={self.correct_answer_tag})"
    
    
class Chapter:
    def __init__(self, title: str, questions: List[Question]):
        self.title = title
        self.questions = questions

    def __repr__(self):
        return f"Chapter(title={self.title}, questions={self.questions})"



def parse_markdown(md_content: str) -> List[Chapter]:
    chapters = []
    
    # Splitting the markdown content into chapters
    chapter_splits = re.split(r'\n###\s+', md_content)
    for chapter_content in chapter_splits[1:]:  # Skip the document title
        # Extracting the chapter title
        chapter_title = chapter_content.split('\n')[0].strip()

        # Finding all questions and their answers in the chapter
        questions = []
        question_splits = re.split(r'\n\d+\.\s+', chapter_content)[1:]  # Skip the chapter title part
        for question_content in question_splits:
            try:
                question_parts = question_content.split('\n-')
                question_text = question_parts[0].split('\n')[0].strip()
                correct_answer = question_parts[1].strip()
                correct_answer_tag_match = re.search(r'\*\*(.*?)\*\*', correct_answer)
                correct_answer = correct_answer.strip(' **').strip()
                correct_answer = correct_answer.rstrip(')**').strip()
                correct_answer = correct_answer.replace('**', '')

                correct_answer_tag = correct_answer_tag_match.group(1) if correct_answer_tag_match else None
                correct_answer_tag = correct_answer_tag.rstrip(')').strip()
                print(correct_answer_tag)
            

            except Exception as e:
                print(f"Error parsing question: {question_text}")

            # Finding options if they exist, if not set to None
            options = None
            options_match = re.findall(r'([A-Z]\))\s+(.+?)(?<!\*\*)$', question_content, re.MULTILINE)
            if options_match:
                options = []
                for o in options_match:
                    option_tag = o[0].replace(")", "")  # Remove the closing parenthesis
                    option_detail = o[1]
                    options.append((option_tag, option_detail))  # Store as a tuple
                question_text = re.split(r'[A-Z]\)', question_text)[0].strip()

            question = Question(question_text, options, correct_answer, correct_answer_tag)
            questions.append(question)
        
        chapter = Chapter(chapter_title, questions)
        chapters.append(chapter)

    return chapters