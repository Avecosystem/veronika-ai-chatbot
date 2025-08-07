@echo off
cls
echo.
echo ================================================================
echo                    VERONIKA AI CHATBOT
echo                  LAUNCHING NOW...
echo ================================================================
echo.

:: Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

echo 🚀 Starting VERONIKA AI server...
start /min python simple_veronika.py

echo ⏱️  Waiting for server to initialize...
timeout /t 3 /nobreak >nul

echo 🌐 Opening web browser...
start http://127.0.0.1:5000

echo.
echo ================================================================
echo ✅ VERONIKA AI is now running!
echo 📍 URL: http://127.0.0.1:5000
echo 🤖 Status: Ready to chat!
echo ================================================================
echo.
echo Press any key to stop the server...
pause >nul

echo.
echo 🛑 Stopping VERONIKA AI server...
taskkill /f /im python.exe >nul 2>&1
echo ✅ Server stopped.
pause
