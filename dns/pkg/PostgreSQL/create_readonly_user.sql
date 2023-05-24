CREATE USER dns_r WITH ENCRYPTED PASSWORD 'Rr123456!';

-- 设置默认事务只读
ALTER USER dns_r SET default_transaction_read_only=on;
-- 赋予用户连接数据库bind_ui的权限
GRANT CONNECT ON DATABASE dns TO dns_r;
-- 切换到指定库bind_ui
\c dns

--schema public 所有表的指定权限授权给指定的用户
GRANT USAGE ON SCHEMA public TO dns_r;
-- schema public 以后新建的表的指定权限赋予给指定的用户
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dns_r;
-- schema public 的所有SEQUENCES(序列)的指定权限授权给指定的用户
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO dns_r;
-- schema public 下的表的select权限授权给指定用户 
GRANT SELECT ON ALL TABLES IN SCHEMA public TO dns_r; 