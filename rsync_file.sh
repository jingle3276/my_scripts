#!/bin/sh

BRIX2807_HOST=192.168.3.208


/opt/bin/rsync  --stats  --info=progress2  -e '/opt/bin/ssh -o "StrictHostKeyChecking no" -i /mnt/data/my_scripts/.ssh/id_rsa' ${1} root@${BRIX2807_HOST}:$2


