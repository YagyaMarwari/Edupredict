@echo off
title EduPredict - 1-Click Public Sharing Link
color 0B
echo.
echo =================================================================
echo   EduPredict - Instant Worldwide Public HTTPS Sharing Link
echo =================================================================
echo   Generating a secure, public HTTPS link via Cloudflare Tunnel...
echo   (No sign-up or accounts required - works on phones, 4G/5G, anywhere!)
echo =================================================================
echo.

if exist "%~dp0cloudflared.exe" (
    "%~dp0cloudflared.exe" tunnel --url http://localhost:8000
    goto :end
)

echo Cloudflared not found. Falling back to SSH tunnel...
ssh -p 443 -R0:localhost:8000 a.pinggy.io
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback tunnel...
    ssh -R 80:localhost:8000 nokey@localhost.run
)

:end
pause
