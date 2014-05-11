#!/bin/bash

source config.sh

python -Wignore -m Pyro4.naming -n $NS_HOSTNAME
