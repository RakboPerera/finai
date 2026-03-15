@echo off
echo ==========================================
echo  FinAI Backend Setup
echo  John Keells Holdings PLC
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/4] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo [3/4] Installing dependencies...
pip install -r requirements.txt

echo [4/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit backend\.env and add your ANTHROPIC_API_KEY
    echo.
)

echo.
echo ==========================================
echo  Backend setup complete!
echo  Run: start-backend.bat to start the server
echo ==========================================
pause
