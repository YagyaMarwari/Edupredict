@echo off
title EduPredict - Student Performance Predictor
echo =====================================================================
echo   EduPredict - Statistical Machine Learning Web Application
echo =====================================================================
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=python
) else (
    py --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PY_CMD=py
    ) else (
        echo.
        echo [ERROR] Python was not found on your computer!
        echo Please download and install Python from: https://www.python.org/downloads/
        echo IMPORTANT: Check the box "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    )
)

echo Found Python launcher: %PY_CMD%
echo.
echo [2/3] Installing dependencies (pandas, scikit-learn, fastapi, etc.)...
%PY_CMD% -m pip install -r requirements.txt
echo.
echo [3/3] Launching EduPredict Web Application...
echo =====================================================================
echo   Website running! Your browser will open automatically.
echo   URL: http://127.0.0.1:8000
echo   To stop the server: Press Ctrl + C in this window.
echo =====================================================================
echo.
%PY_CMD% app.py
pause
