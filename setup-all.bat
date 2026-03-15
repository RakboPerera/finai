@echo off
echo ==========================================
echo  FinAI - Financial Intelligence Platform
echo  Full Setup
echo  John Keells Holdings PLC
echo ==========================================
echo.

cd /d "%~dp0"

echo [Step 1] Setting up Backend...
echo -------------------------------------------
cd backend
call setup.bat
cd ..

echo.
echo [Step 2] Setting up Frontend...
echo -------------------------------------------
cd frontend
call setup.bat
cd ..

echo.
echo ==========================================
echo  Setup Complete!
echo.
echo  IMPORTANT: Edit backend\.env and set your
echo  ANTHROPIC_API_KEY before starting.
echo.
echo  To start the app:
echo    Terminal 1: cd backend ^& start-backend.bat
echo    Terminal 2: cd frontend ^& start-frontend.bat
echo.
echo  Frontend: http://localhost:3000
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo ==========================================
pause
