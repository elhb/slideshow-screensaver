#!/bin/bash

# Get script directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

xautolock -time 1 -locker "python2 $DIR/screensaver.py"
