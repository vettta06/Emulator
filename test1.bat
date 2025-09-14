@echo off
cd /d "%~dp0"
call .\venv\Scripts\activate.bat
python emulator.py --script "start.vfs"
pause