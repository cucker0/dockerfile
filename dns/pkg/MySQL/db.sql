-- 创建数据库
CREATE DATABASE dns CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 新建用户
CREATE USER 'dns_wr'@'%' IDENTIFIED BY 'Ww123456!';
GRANT all ON dns.* TO 'dns_wr'@'%';

CREATE USER 'dns_r'@'%' IDENTIFIED BY 'Rr123456!';
GRANT SELECT ON dns.* TO 'dns_r'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
