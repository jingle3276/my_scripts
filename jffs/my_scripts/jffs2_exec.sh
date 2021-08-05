#!/bin/sh


#  custom script executed at boot (during start of jffs)
#
# Note: 1) NVRAM variable "jffs2_exec" must point to this script
#       2) The calling code waits for this script to terminate,
#          so in order to not stall the boot process, we quickly
#          move to the background
#

# maxwait=300
# #append_hosts='/jffs/bin/append_hosts'

# umask 022

# #
# # move to background in a subshell
# #
# (
#     cd /

#     # ignore SIGHUP
#     trap '' SIGHUP

#     # redirect STDIN, STDOUT, STDERR
#     exec 0< '/dev/null'
#     exec 1> '/dev/null'
#     exec 2> '/dev/null'

#     #
#     # wait till all the system services are started
#     # by polling "success_start_service" NVRAM variable
#     #
#     i=0
#     while [ "$i" -le "$maxwait" ]
#     do
#         success_start_service="$( nvram get 'success_start_service' )"
#         if [ "$success_start_service" == '1' ]
#         then
#             break
#         fi
#         sleep 10
#         i=$(( $i + 10 ))
#     done

#     if [ "$i" -gt "$maxwait" ]
#     then
#         # timeout
#         logger 'ffs2_exec.sh script: timout waiting for "success_start_service"'
#         exit 1
#     fi

#     #
#     # wait a little longer to allow ntp client to get correct time
#     #
#     sleep 60

#     logger 'ffs2_exec.sh script executing'

#     # append custom hosts file to hosts
#     # if [ -x "$append_hosts" ]
#     # then
#     #     eval "$append_hosts"
#     # fi
    
#     # add other stuff you want to do...
    





#     exit 0
# )&

# exit 0