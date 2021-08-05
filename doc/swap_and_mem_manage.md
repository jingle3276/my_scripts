https://mydevtutorials.wordpress.com/2014/01/10/how-to-activate-swap-on-asus-rt-ac68u-router/


#create a 256MB swap file ("count" is in Kilobytes)
dd if=/dev/zero of=/tmp/mnt/entware/swap.swp bs=1k count=262144
 
#set up the swap file
mkswap /tmp/mnt/entware/swap.sw
 
#enable swap
swapon /tmp/mnt/entware/swap.sw
 
#check if swap is on
free
If you reboot your router, the swap will be inactive until you swapon again. To do this automatically you have to create the file /jffs/scripts/post-mount, or edit it if exists and add the line:

Add this to /jffs/my_scripts/script_usbmoun.sh
swapon /tmp/mnt/entware/swap.sw
Now every time the router reboots, it will turn on swap.