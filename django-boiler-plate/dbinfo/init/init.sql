CREATE DATABASE django_wprj;
CREATE USER sangmin WITH PASSWORD '123456';
ALTER ROLE sangmin SET client_encoding TO 'utf8';
ALTER ROLE sangmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE sangmin SET TIME ZONE 'Asia/Seoul';
GRANT ALL PRIVILEGES ON DATABASE django_wprj To sangmin;