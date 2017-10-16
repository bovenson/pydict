#!/bin/bash
# echo `pwd` > /home/bovenson/Tmp/cron.log

FULLPATH="$PWD/$(dirname $0)"
cd $FULLPATH

python3 pydict-gui/pydict-gui.py 1>pydict-gui.log 2>&1 &
