@echo off

call config.bat

if not exist positions (
	echo Creating positions folder
	mkdir ..\positions
)

echo Starting computations
python -m pyage.core.bootstrap langtons_ant.conf
echo Computations finished