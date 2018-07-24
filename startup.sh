#!/bin/bash
if [ $(ps aux | grep 'kukkohelper.py' | grep -v grep | wc -w) -gt 0 ] ;
then
echo "Script running" ;
exit
fi
python3 /opt/scripts/kukkohelper/kukkohelper.py
