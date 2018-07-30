#!/bin/bash
if [ $(ps aux | grep 'kukkohelper.py' | grep -v grep  | wc -l) -gt 0 ] 
then
	echo "Already running"
	exit
fi
echo "Launching kukkohelper"
python3 /opt/scripts/kukkohelper/kukkohelper.py
