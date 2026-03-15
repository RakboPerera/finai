@echo off
echo.
echo  ============================================
echo   FinAI - Financial Intelligence Platform
echo   John Keells Holdings PLC
echo  ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

:: Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [OK] Python and Node.js found
echo.

:: Setup Backend
echo [1/4] Setting up Backend...
cd backend
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
echo [OK] Backend dependencies installed

:: Create .env if not exists
if not exist .env (
    copy .env.example .env
    echo [NOTE] Created .env file - please add your ANTHROPIC_API_KEY
)
cd ..

echo.

:: Setup Frontend
echo [2/4] Setting up Frontend...
cd frontend
call npm install --silent
cd ..
echo [OK] Frontend dependencies installed

echo.
echo  ============================================
echo   Setup Complete!
echo  ============================================
echo.
echo  IMPORTANT: Add your Anthropic API key to backend\.env
echo.
echo  To start the app:
echo    Terminal 1: cd backend ^& venv\Scripts\activate ^& python main.py
echo    Terminal 2: cd frontend ^& npm run dev
echo.
echo  Frontend: http://localhost:3000
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo.
pause
