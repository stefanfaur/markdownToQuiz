

# Quiz-from-Markdown Generator

## Introduction

This project is designed to help with studying for exams by converting Markdown files into interactive quizzes. 
I built it for myself and my friends, we used it to study for some exams and it worked great.

- It supports both text answer and multiple-choice questions.
- This tool can make study sessions more engaging and effective.

## Getting Started

### Requirements

- Python 3.x
- PyQt5

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/stefanfaur/markdownToQuiz
```

Navigate to the project directory:

```bash
cd markdownToQuiz
```

Install the required dependencies (if any):

```bash
pip install -r requirements.txt
```

### Usage

To run the quiz generator, navigate to the project directory and execute:

```bash
python3 src/gui_quiz.py
```

Currently, the tool is run from the command line, with an executable version in development.

### Quiz Format

The Markdown file **must follow a specific format** to be correctly processed by the quiz generator. An example Markdown file can be found in `./assets/example.md`. Ensure your Markdown files conform to this structure. The software will not work correctly otherwise. 

**The parsing is not done very safely, so if some formatting is wrong, you probably didn't respect the example format ;)**