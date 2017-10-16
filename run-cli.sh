#!/bin/bash
# echo `pwd` > /home/bovenson/Tmp/cron.log

FULLPATH="$PWD/$(dirname $0)"
cd $FULLPATH

python3 pydict-cli/pydict.py
