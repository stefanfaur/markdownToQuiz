#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m PyInstaller --onefile --paths=src src/gui_quiz.py
deactivate
