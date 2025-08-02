@echo off

set CONDA_PATH=C:\Users\User\miniconda3
call "%CONDA_PATH%\condabin\conda.bat" activate moodle

set PYTHONPATH=%~dp0..

python main.py
pause