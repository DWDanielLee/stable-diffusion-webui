@echo off

del C:\Users\kei01\AppData\Local\Temp\*.png
pip cache purge

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--theme=dark --xformers --autolaunch --listen

call webui.bat
