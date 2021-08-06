#!/bin/sh

timestamp=$(/bin/date +"%Y_%m_%d_%H_%M")

cd /tmp/mnt/entware/nsru
mkdir backup
./nvram-save.sh
mv backup backup_$timestamp
/mnt/data/my_scripts/transfer_nvram.sh $timestamp
