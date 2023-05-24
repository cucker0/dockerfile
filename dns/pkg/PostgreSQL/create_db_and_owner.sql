-- sudo -u postgres psql -d testdb -U postgres -f /path/xxx.sql

CREATE USER dns_wr WITH ENCRYPTED PASSWORD 'Ww123456!';
CREATE DATABASE dns WITH ENCODING = 'UTF-8' TEMPLATE = template0 OWNER dns_wr;