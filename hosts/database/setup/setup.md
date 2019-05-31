```
sudo -u postgres createuser --interactive
createdb evs
psql -d evs

\i create_tables.sql
```

## Docker
```
docker pull postgres:9.5
./run.sh
PGPASSWORD=docker psql -h localhost -U postgres -d evs
```
