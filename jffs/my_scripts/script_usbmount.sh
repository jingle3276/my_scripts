# this script will be executed when usbmount happends (shortly after boot)
# https://github.com/RMerl/asuswrt-merlin.ng/wiki/User-scripts

# must have this in the nvram entry: 
#   nvram set script_usbmount="/jffs/my_scripts/script_usbmount.sh"
#   nvram commit

# must have a USB drive plugged in the device


# copy admin (the crontab file) to crond watch dir
cp /jffs/my_scripts/admin /var/spool/cron/crontabs

# sync-time once so don't wait 5 minutes 
/jffs/my_scripts/sync_time.sh


# start entware: creating a soft link from entware to /tmp/opt and start opt
# assume entware is located on /tmp/mnt/entware/entware-ng.arm
if [ -d "/tmp/mnt/entware/entware-ng.arm" ]
then
ln -sf /tmp/mnt/entware/entware-ng.arm /tmp/opt
/opt/etc/init.d/rc.unslung start
fi

# mount swap file 256MB
/sbin/swapon /tmp/mnt/entware/swap.swp

# add brix2807 (192.168.3.208) to dropbear (ssh) known host: /tmp/home/root/.ssh/known_hosts
# this will ensure dropbear ssh command run without asking comfirm unknown host (first time after boot)
# echo 192.168.3.208 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOQ4g/cypUfRKORf0nGThOuYFsD6HOY4/GQdGmUbrJEecHSXv3Jklkq2u8WIlDSFY/TQKr6jzhJzeeGkfMdM17A= > /tmp/home/root/.ssh/known_hosts


# symlink .ssh from jffs to root home. target must be removed before ln
rm -rf /tmp/home/root/.ssh ; ln -s /jffs/my_scripts/secrets/.ssh /tmp/home/root/.ssh


# copy conf files to root $HOME
cp -a /mnt/data/my_scripts/conf/. /tmp/home/root/


# start django webapp
#/opt/bin/python /tmp/mnt/data/django/mysite/manage.py runserver 0.0.0.0:8000


# start bottle webapp
/tmp/mnt/data/my_scripts/start_bottle_server.sh
