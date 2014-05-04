#!/bin/bash

if [ $# -eq 0 ]; then
	ITER="1"
else
	ITER=$1
fi

echo "Plotting after $ITER iteration(s)"
python langtons_ant/plot.py $ITER
