@echo off

gnuplot --version >nul 2>&1 || (
	echo.
	echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	echo No GNUPLOT found. Please install it.
	echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	echo.
)

if "%1"=="" (
	set ITER="1"
) else (
	set ITER=%1
)

echo Plotting after %ITER% iteration(s)
python langtons_ant/plot.py %ITER%
