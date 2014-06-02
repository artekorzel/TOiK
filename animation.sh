#!/bin/bash

if [ $# -eq 0 ]; then
	ITER="0"
else
	ITER=$1
fi

python -m langtons_ant.animation.py $ITER