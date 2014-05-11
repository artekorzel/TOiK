#!/bin/bash

source config.sh

if [ ! -d "../positions" ]; then
	echo Creating positions folder
	mkdir ../positions
fi

rm ../positions/*

echo Starting computations
python -m pyage.core.bootstrap langtons_ant.conf
echo Computations finished
