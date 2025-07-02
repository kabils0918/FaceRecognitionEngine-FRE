@REM double click this file from the File Explorer to run the project- This script activates the virtual environment and starts the Face Recognition System and Flask Dashboard at a time.
@echo off
echo [INFO] Activating virtual environment...
call env_temp\Scripts\activate

echo [INFO] Starting Face Recognition System...
start cmd /k python src\03_Face_Recognition.py

timeout /t 3 >nul
echo [INFO] Starting Flask Dashboard...
start cmd /k python app.py
