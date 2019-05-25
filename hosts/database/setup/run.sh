docker run --rm -d -p 5432:5432 --name evs_pg evs_postgres
docker run --rm -t -i --link evs_pg:pg evs_postgres bash

# run the command below while inside docker bash to access database
# psql -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -d evs -U ubuntu --password
