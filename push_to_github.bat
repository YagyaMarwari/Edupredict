@echo off
title EduPredict - Push to GitHub
cd /d "C:\Users\IIISI\OneDrive\Desktop\student_performance_predictor"

echo ======================================================================
echo                EDUPREDICT: PUSH CODE TO GITHUB
echo ======================================================================
echo.
echo Target Repository: https://github.com/YagyaMarwari/Edupredict.git
echo Working Directory: %CD%
echo.

set "GIT_EXE=D:\Git\cmd\git.exe"
if not exist "%GIT_EXE%" (
    where git >nul 2>nul
    if %errorlevel% equ 0 (
        set "GIT_EXE=git"
    ) else (
        echo [ERROR] Git was not found at D:\Git\cmd\git.exe or in PATH.
        pause
        exit /b 1
    )
)

echo [*] Staging all files...
"%GIT_EXE%" add .

echo [*] Checking commit status...
"%GIT_EXE%" commit -m "Initial commit: EduPredict Academic Performance Predictor & Faculty Portal" >nul 2>&1

echo [*] Pushing branch 'main' to GitHub origin...
echo (If a browser window opens, please click "Authorize" or sign in)
echo.
"%GIT_EXE%" push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! All project files pushed to:
    echo  https://github.com/YagyaMarwari/Edupredict
    echo ======================================================================
) else (
    echo.
    echo [ERROR] Push failed or was canceled.
)

echo.
pause
