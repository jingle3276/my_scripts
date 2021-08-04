#!/bin/sh
# pass all arguments to the remote ssh command
# add -y -y to bypass unknow remote host check 
# this has problem when used by cron, or django app
/usr/bin/ssh root@192.168.3.208 -i /etc/dropbear/dropbear_rsa_host_key -t "$@"
