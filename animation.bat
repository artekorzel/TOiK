@echo off

if "%1"=="" (
	set ITER="0"
) else (
	set ITER=%1
)

python -m langtons_ant.animation.py %ITER%