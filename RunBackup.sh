#!/bin/bash
#
## Author: zrwang(zrwang1993@126.com)
## Program: For routine backup.
## Usage: RunBackup.sh <path-to-backupservice>
## Changelog:
##     1. Initialization.
#

if [ "$1" != '' ]; then
  curr_dir=$1
fi

cd $curr_dir
python ./BackupService.py -b > /dev/null

