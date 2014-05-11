@echo off

call config.bat

python -Wignore -m Pyro4.naming -n %NS_HOSTNAME%