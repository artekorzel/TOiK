@echo off

if "%1"=="" (
	set ITER="1"
) else (
	set ITER=%1
)

python langtons_ant/animation.py %ITER%