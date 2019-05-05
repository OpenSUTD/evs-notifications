```
sudo -u postgres createuser --interactive
createdb evs
psql -d evs

\i create_tables.sql

\COPY account
FROM 'accounts.csv' DELIMITER ',' CSV;
```
