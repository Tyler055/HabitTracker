@echo off
echo Starting Flask backend...

REM Check if virtual environment exists
IF NOT EXIST ".myapp\Scripts\activate" (
    echo Virtual environment not found. Creating a new one...
    python -m venv .myapp

    REM Activate the virtual environment
    call .myapp\Scripts\activate

    REM Update pip (only first time)
    echo Updating pip...
    python -m pip install --upgrade pip

    REM Install dependencies (only first time)
    echo Installing dependencies...
    IF EXIST "requirements.txt" (
        pip install -r requirements.txt
    ) ELSE (
        echo WARNING: requirements.txt not found!
    )
) ELSE (
    echo Virtual environment found. Activating it...
    call .myapp\Scripts\activate
)

REM Navigate to the backend directory
cd backend

REM Set Flask environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

REM Start Flask backend in a new command window
echo Starting Flask server...
start cmd /k "flask run"

REM Wait for a few seconds to ensure Flask server has started
timeout /t 5 /nobreak >nul

REM Open the default web browser at Flask server URL
echo Opening browser...
start http://127.0.0.1:5000
