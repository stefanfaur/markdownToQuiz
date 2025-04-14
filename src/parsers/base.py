from abc import ABC, abstractmethod
from typing import List
from ..models import Chapter

class Parser(ABC):
    """Abstract base class for document parsers."""
    
    @abstractmethod
    def parse(self, content: str) -> List[Chapter]:
        """Parse the content and return a list of chapters.
        
        Args:
            content: The string content to parse.
            
        Returns:
            List[Chapter]: A list of parsed chapters with their questions.
            
        Raises:
            ParserError: If there is an error during parsing.
        """
        pass

class ParserError(Exception):
    """Base exception for parser errors."""
    pass
