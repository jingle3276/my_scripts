#!/bin/sh

src=/tmp/mnt/data/my_scripts/jffs


/opt/bin/rsync -a ${src}/etc/profile /jffs/etc/profile
/opt/bin/rsync -a $src/my_scripts/admin /jffs/my_scripts/
cp /jffs/my_scripts/admin /var/spool/cron/crontabs/admin 
/opt/bin/rsync -a $src/my_scripts/script_usbmount.sh /jffs/my_scripts/
/opt/bin/rsync -a $src/my_scripts/script_usbumount.sh /jffs/my_scripts/
/opt/bin/rsync -a $src/my_scripts/sync_time.sh /jffs/my_scripts/



echo "deployment finished"
