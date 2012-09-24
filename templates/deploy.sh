#! /bin/bash
# ssh into webfactional
echo 'connecting to server ...'
ssh danieln@danieln.webfactional.com

# project deploy script
cd /home/danieln/webapps/{{ project_name }}/{{ project_name }}

# git pull origin master
echo 'deploying application ...'
git pull origin master

# restart apache
echo 'restarting apache ...'
/home/danieln/webapps/{{ project_name }}/apache2/bin/restart

echo 'done'