@echo off

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python -m PyInstaller --onefile --paths=src src\gui_quiz.py
call deactivate