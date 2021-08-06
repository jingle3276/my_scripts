asus router by default uses dropbear ssh server. 
auth keys are stored in: /etc/dropbear/
which is a symlink to /jffs/.ssh

/jffs/.ssh is genereated by asus web gui. B

nvram get sshd_authkeys

Issue 08/05/2021
it seems the asus web gui it not working properly in generating the dropbear key

