

# Quiz-from-Markdown Generator

## Introduction

This project is designed to help with studying for exams by converting Markdown files into interactive quizzes quickly. 
I built it for myself and my friends, we used it for some exams and it worked great.

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

You can find the executables in the Releases section of this repository. They are made using PyInstaller and should work on Linux, MacOS and Windows.
**They are not signed, so they will probably trigger your antivirus**

To run the quiz script yourself, navigate to the project directory and execute:

```bash
python3 src/gui_quiz.py
```

If you want to build an executable yourself, you can use the provided script:

```bash
bash build_release.sh
```

### Quiz Format

The Markdown file **must follow a specific format** to be correctly processed by the quiz generator. An example Markdown file can be found in `./assets/example.md`. Ensure your Markdown files conform to this structure. The software will not work correctly otherwise. 

**The parsing is not done very safely, so if some formatting is wrong, you probably didn't respect the example format ;)** 
The console will output what question "went wrong" though so you can fix it.
If you find any bugs, please open an issue, I'm happy to fix them.