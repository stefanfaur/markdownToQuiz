#!/usr/bin/env python3
"""
Markdown Quiz Application
A quiz application that parses markdown files to create interactive quizzes
with support for code blocks and images.
"""

import os
import sys

# Add the root directory to the Python path for proper imports
root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, 'src')
sys.path.insert(0, root_dir)

try:
    from src.main import main
    sys.exit(main())
except ImportError as e:
    print(f"Error importing required modules: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Fatal error: {e}", file=sys.stderr)
    sys.exit(1)
