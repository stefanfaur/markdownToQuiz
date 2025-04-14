from dataclasses import dataclass
from typing import List, Optional
from .question import Question, ContentBlock, ContentType

@dataclass
class Chapter:
    """Represents a chapter containing multiple questions and optional chapter content."""
    title: str
    questions: List[Question]
    description: Optional[List[ContentBlock]] = None

    def __post_init__(self):
        if self.description is None:
            self.description = []

    @property
    def question_count(self) -> int:
        """Returns the total number of questions in the chapter."""
        return len(self.questions)

    def get_text_description(self) -> str:
        """Returns the text-only description of the chapter."""
        if not self.description:
            return ""
        text_blocks = [block.content for block in self.description 
                      if block.type == ContentType.TEXT]
        return "\n".join(text_blocks)

    def get_code_blocks(self) -> List[tuple[str, str]]:
        """Returns all code blocks in the chapter description."""
        if not self.description:
            return []
        return [(block.metadata.get('language', ''), block.content)
                for block in self.description
                if block.type == ContentType.CODE]

    def get_images(self) -> List[tuple[str, str]]:
        """Returns all images in the chapter description."""
        if not self.description:
            return []
        return [(block.content, block.metadata.get('alt_text', ''))
                for block in self.description
                if block.type == ContentType.IMAGE]

    def __repr__(self) -> str:
        return f"Chapter(title={self.title!r}, question_count={self.question_count})"
