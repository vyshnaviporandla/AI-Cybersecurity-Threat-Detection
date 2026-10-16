
@echo off
setlocal
cd /d "%~dp0"

title AI Cybersecurity Threat Detection

echo ==========================================
echo   AI CYBERSECURITY THREAT DETECTION
echo ==========================================
echo.

REM Check that the virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo Please create the .venv environment first.
    goto setup_failed
)

REM Check that the required dataset exists
if not exist "data\raw\UNSW_NB15_training-set.csv" (
    echo ERROR: Dataset not found.
    echo Expected:
    echo data\raw\UNSW_NB15_training-set.csv
    goto setup_failed
)

echo [1/3] Training model and generating evaluation reports...
echo.
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto training_failed

echo.
echo [2/3] Generating potential-attack alert report...
echo.
".venv\Scripts\python.exe" simulate.py
if errorlevel 1 goto alerts_failed

echo.
echo [3/3] Starting the Flask prediction API...
echo.
echo API address: http://127.0.0.1:5000
echo Health check: http://127.0.0.1:5000/health
echo.
echo Keep this window open while using the API.
echo Press Ctrl+C to stop the server.
echo ==========================================
echo.

".venv\Scripts\python.exe" app.py

echo.
echo The API server has stopped.
pause
exit /b 0

:training_failed
echo.
echo ERROR: Model training failed.
echo Check the error messages above.
pause
exit /b 1

:alerts_failed
echo.
echo ERROR: Alert generation failed.
echo Check the error messages above.
pause
exit /b 1

:setup_failed
echo.
echo Setup check failed. Please fix the issue above.
pause
exit /b 1
