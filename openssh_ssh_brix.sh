#!/bin/sh
/opt/bin/ssh root@192.168.3.208 -o "StrictHostKeyChecking no" -i /mnt/data/my_scripts/.ssh/id_rsa -t "$@"
