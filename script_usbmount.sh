# this script will be executed when usbmount happends (shortly after boot)

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

