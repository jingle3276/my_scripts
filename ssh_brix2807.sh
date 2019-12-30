#!/bin/sh
# pass all arguments to the remote ssh command
# assument 
/usr/bin/ssh root@192.168.3.208 -i /etc/dropbear/dropbear_rsa_host_key -t "$@"
