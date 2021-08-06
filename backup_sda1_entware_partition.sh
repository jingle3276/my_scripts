#!/bin/sh

# backup entware partition and put it on to remote server. 
# it takes about 20 mins to finish the job

timestamp=$(/bin/date +"%Y_%m_%d_%H_%M_%S")

remote_host=192.168.3.208
src_partition=/dev/sda1
file_name=sda1_entware_${timestamp}.partition.gzip
file_full_path=/mnt/data/backup/partition_images/${file_name}
remote_file_full_path=/srv/samba/data/backup/ac68u/partition/${file_name}



#echo "${timestamp}: backup running, src partion: ${src_partition}, destination: ${file_full_path}"
# backup command
#/opt/bin/time /bin/dd if=${src_partition} conv=sync,noerror bs=64K | gzip -c  > ${file_full_path}

# transfer to Brix2807
#/mnt/data/rsync_file.sh file_full_path /srv/samba/data/backup/ac68u

# delete after scuessful transfer 
#/bin/rm -rf file_full_path


# piped process. no local file generation 
echo "${timestamp}: backup running, src partion: ${src_partition}, remote host: ${remote_host}, destination: ${file_full_path}"
/bin/dd if=${src_partition} conv=sync,noerror bs=64K | gzip -c | /opt/bin/ssh root@${remote_host} -o "StrictHostKeyChecking no" -i /mnt/data/my_scripts/.ssh/id_rsa "cat > ${remote_file_full_path}"


