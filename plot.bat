@echo off
if "%1"=="" (
	set ITER="1"
) else (
	set ITER=%1
)

echo Plotting after %ITER% iteration(s)
python langtons_ant/plot.py %ITER%
