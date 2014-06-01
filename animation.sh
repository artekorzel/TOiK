#!/bin/bash

if [ $# -eq 0 ]; then
	ITER="1"
else
	ITER=$1
fi

python langtons_ant/animation.py $ITER