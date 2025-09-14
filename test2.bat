@echo off
cd /d "%~dp0"
call .\venv\Scripts\activate.bat
python emulator.py --vfs-path "C:\myvfs" --script "start.vfs"
pause