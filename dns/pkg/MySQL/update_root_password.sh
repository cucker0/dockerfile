#!/bin/bash

NEW_PASSWORD='Py123456!'
INIT_PASSWORD=$(grep "root@localhost" /var/log/mysqld.log |awk -F "root@localhost: " '{print $2}')

main() {
    mysql -uroot -p${INIT_PASSWORD} --connect-expired-password < /pkg/MySQL/alter_user_password.sql;
    mysql -uroot -p${NEW_PASSWORD} < /pkg/MySQL/db.sql    
}

main