#!/bin/sh


src_dir=/tmp/mnt/entware/nsru/backup_$@

timestamp=$(/bin/date +"%Y %m %d %H %M %S")
remote_host=192.168.3.208
file_name=backup$@.tar.gz
remote_file_full_path=/srv/samba/data/backup/ac68u/nvram/nsru/${file_name}


# piped process. no local file generation 


echo "${timestamp}: backup running, src: ${src_dir}, remote host: ${remote_host}, destination: ${remote_file_full_path}"
/bin/tar zcvf - ${src_dir} | /opt/bin/ssh root@${remote_host} -o "StrictHostKeyChecking no" -i /mnt/data/my_scripts/.ssh/id_rsa "cat > ${remote_file_full_path}"

