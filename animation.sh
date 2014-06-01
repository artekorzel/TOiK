#!/bin/bash

if [ $# -eq 0 ]; then
	ITER="0"
else
	ITER=$1
fi

python langtons_ant/animation.py $ITER