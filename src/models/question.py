import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any, Union
from enum import Enum
import re

class ContentType(Enum):
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"

@dataclass
class ContentBlock:
    type: ContentType
    content: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Question:
    """Represents a quiz question with support for rich content."""
    content_blocks: List[ContentBlock]
    options: Optional[List[Tuple[str, str]]]  # List of (tag, text) tuples for multiple choice
    correct_answer: str
    correct_answer_tag: str
    
    @property
    def is_multiple_choice(self) -> bool:
        """Returns True if this is a multiple choice question."""
        return self.options is not None and len(self.options) > 0
    
    def check_answer(self, answer: str) -> bool:
        """Check if the given answer is correct.
        For multiple choice questions, checks against the answer tag.
        For text questions, always returns None to indicate manual checking."""
        if not self.is_multiple_choice:
            return None
            
        # For multiple choice, accept various formats (A, a, A), a))
        answer = re.sub(r'[^A-Za-z]', '', answer).upper()
        expected = re.sub(r'[^A-Za-z]', '', self.correct_answer_tag).upper()
        return answer == expected
    
    @property
    def text(self) -> str:
        """Returns the main text content of the question."""
        text_blocks = [block.content for block in self.content_blocks 
                      if block.type == ContentType.TEXT]
        return "\n".join(text_blocks)

    def has_code(self) -> bool:
        """Checks if the question contains code blocks."""
        return any(block.type == ContentType.CODE for block in self.content_blocks)

    def has_images(self) -> bool:
        """Checks if the question contains images."""
        return any(block.type == ContentType.IMAGE for block in self.content_blocks)

    def get_code_blocks(self) -> List[Tuple[str, str]]:
        """Returns list of (language, code) tuples for all code blocks."""
        return [(block.metadata.get('language', ''), block.content)
                for block in self.content_blocks
                if block.type == ContentType.CODE]

    def get_images(self) -> List[Tuple[str, str]]:
        """Returns list of (path, alt_text) tuples for all images."""
        return [(block.content, block.metadata.get('alt_text', ''))
                for block in self.content_blocks
                if block.type == ContentType.IMAGE]

    def __repr__(self) -> str:
        return f"Question(text={self.text!r}, has_code={self.has_code()}, has_images={self.has_images()})"
