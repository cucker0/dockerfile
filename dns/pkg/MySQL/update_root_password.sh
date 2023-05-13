#!/bin/bash

NEW_PASSWORD='Py123456!'
INIT_PASSWORD=$(grep "root@localhost" /var/log/mysqld.log |awk -F "root@localhost: " '{print $2}')

main() {
    # 修改 "root@localhost" 用户密码
    mysql -uroot -p${INIT_PASSWORD} --connect-expired-password < /pkg/MySQL/alter_user_password.sql;
    # 或这样修改 root@localhost 密码
    #mysql -uroot -p${INIT_PASSWORD} --connect-expired-password -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'Py123456!' ;"
    mysql -uroot -p${NEW_PASSWORD} < /pkg/MySQL/db.sql    
}

main