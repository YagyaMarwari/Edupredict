@echo off
title EduPredict - Share Website Publicly
color 0A

echo.
echo =========================================================
echo  EduPredict - Make Website Public ^& Shareable
echo =========================================================
echo.
echo  This generates a public HTTPS link that ANYONE on the
echo  internet (phones, laptops, tablets) can open worldwide!
echo.

if exist "%~dp0cloudflared.exe" (
    echo  [Cloudflare] Starting instant secure tunnel on port 8000...
    echo.
    "%~dp0cloudflared.exe" tunnel --url http://localhost:8000
    goto :end
)

:: Check if ngrok.exe is available locally
if exist "%~dp0ngrok.exe" (
    echo  [ngrok] Found ngrok. Starting tunnel...
    "%~dp0ngrok.exe" http 8000
    goto :end
)

:: Fallback: use pinggy.io via SSH (no install needed!)
echo  [pinggy] Using SSH tunnel (pinggy.io) as fallback...
ssh -o StrictHostKeyChecking=no -p 443 -R0:localhost:8000 a.pinggy.io

:end
echo.
echo  Tunnel closed. Your website is no longer public.
pause
