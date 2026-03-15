@echo off
echo ==========================================
echo  FinAI Frontend Setup
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/2] Installing npm dependencies...
npm install
if errorlevel 1 (
    echo ERROR: Node.js/npm not found. Install Node.js 18+ first.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Frontend setup complete!
echo  Run: start-frontend.bat to start the dev server
echo ==========================================
pause
