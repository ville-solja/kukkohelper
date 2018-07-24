#!/bin/bash
COUNT=$(ps aux | grep 'skripti.py' | grep -v grep | wc -l)
if [$COUNT -gt 0] ;
then
        echo "Script running" ;
else
        echo "Script not running"
        python3 /opt/scripts/skripti.py ;
fi
