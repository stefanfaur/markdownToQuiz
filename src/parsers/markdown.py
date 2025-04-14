import re
from typing import List, Optional, Tuple, Dict
from .base import Parser, ParserError
from ..models import Chapter, Question, ContentBlock, ContentType

class MarkdownParser(Parser):
    def parse(self, content: str) -> List[Chapter]:
        print("\nStarting parse") # Debug
        
        # First clean up line endings
        content = content.replace('\r\n', '\n')
        
        # Split into chapters
        chapters_raw = re.split(r'\n###\s+', content)
        print(f"Found {len(chapters_raw)} raw chapter splits") # Debug
        
        # Skip first part if it's just the document title
        if not chapters_raw[0].strip().startswith('###'):
            chapters_raw = chapters_raw[1:]
            print("Skipped document title section") # Debug
            
        if not chapters_raw:
            raise ParserError("No chapters found in content")
            
        chapters = []
        for chapter_content in chapters_raw:
            if not chapter_content.strip():
                continue
                
            # Split title and content
            chapter_lines = chapter_content.split('\n')
            title = chapter_lines[0].strip()
            content_lines = chapter_lines[1:]
            
            # Process chapter content
            print(f"\nProcessing chapter: {title}") # Debug
            questions = self._parse_questions('\n'.join(content_lines))
            print(f"Found {len(questions)} questions") # Debug
            if questions:
                chapters.append(Chapter(title=title, questions=questions))
                print(f"Added chapter with {len(questions)} questions") # Debug
            
        if not chapters:
            raise ParserError("No chapters found in content")
            
        return chapters
        
    def _parse_questions(self, content: str) -> List[Question]:
        questions = []
        current_content = []
        current_options = []
        current_answer = ''
        current_answer_tag = ''
        
        def create_question() -> Optional[Question]:
            nonlocal current_content, current_options, current_answer, current_answer_tag
            if current_content:
                question = Question(
                    content_blocks=[],
                    options=current_options if current_options else None,
                    correct_answer=current_answer,
                    correct_answer_tag=current_answer_tag
                )
                # Process content blocks
                for block in current_content:
                    # Code blocks
                    if block.startswith('```'):
                        lines = block.split('\n')
                        lang = lines[0][3:].strip()
                        code = '\n'.join(lines[1:-1])
                        question.content_blocks.append(
                            ContentBlock(
                                type=ContentType.CODE,
                                content=code.strip(),
                                metadata={'language': lang or 'text'}
                            )
                        )
                    # Regular text
                    else:
                        question.content_blocks.append(
                            ContentBlock(
                                type=ContentType.TEXT,
                                content=block.strip()
                            )
                        )
                current_content = []
                current_options = []
                current_answer = ''
                current_answer_tag = ''
                return question
            return None
            
        in_code_block = False
        code_block = []
        current_block = []
        
        for line in content.split('\n'):
            line = line.rstrip()
            
            # Handle code blocks
            if line.startswith('```'):
                if in_code_block:
                    code_block.append(line)
                    current_content.append('\n'.join(code_block))
                    code_block = []
                    in_code_block = False
                else:
                    if current_block:
                        current_content.append('\n'.join(current_block))
                        current_block = []
                    code_block = [line]
                    in_code_block = True
                continue
                
            if in_code_block:
                code_block.append(line)
                continue
                
            # Question start
            if match := re.match(r'^\d+\.\s+(.+)$', line):
                # Save previous question if any
                if current_block:
                    current_content.append('\n'.join(current_block))
                if question := create_question():
                    questions.append(question)
                    print(f"Created new question: {match.group(1)}") # Debug
                
                # Start new question
                current_block = [match.group(1)]
                current_content = []  # Reset content for new question
                current_options = []  # Reset options for new question
                current_answer = ''   # Reset answer for new question
                current_answer_tag = ''
                
            # Options
            elif match := re.match(r'^[A-Z]\)\s+(.+)$', line):
                # Finish current content block if exists
                if current_block:
                    current_content.append('\n'.join(current_block))
                    current_block = []
                
                current_options.append((line[0], match.group(1).strip()))
                print(f"Added option {line[0]}: {match.group(1)}") # Debug
                
            # Answer
            elif '**' in line:
                text = line.replace('*', '').strip()
                # Remove any leading dashes and whitespace
                text = re.sub(r'^[-\s]+', '', text)
                if match := re.match(r'^\s*([A-Z])\)(.*)', text):
                    # Just store the letter as the tag
                    current_answer_tag = match.group(1)
                    answer_text = match.group(2).strip()
                    # If no specific answer text, use the tag itself
                    current_answer = answer_text if answer_text else match.group(1)
                else:
                    # For text answers, use same text for both
                    current_answer = text
                    current_answer_tag = text
                print(f"Found answer: {current_answer} (tag: {current_answer_tag})") # Debug
                    
            # Additional content
            elif line.strip():
                current_block.append(line)
                
        # Finalize state before creating the last question
        if current_block: # Add any remaining text block
            current_content.append('\n'.join(current_block))
        if code_block: # Add any remaining code block
             current_content.append('\n'.join(code_block))
             
        # Add final question if content exists
        if question := create_question():
            questions.append(question)
            
        return questions
