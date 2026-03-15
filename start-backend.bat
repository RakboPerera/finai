@echo off
echo Starting FinAI Backend...
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
python main.py
