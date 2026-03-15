@echo off
echo Starting FinAI Backend on http://localhost:8000 ...
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
