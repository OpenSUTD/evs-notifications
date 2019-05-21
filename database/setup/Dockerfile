# example Dockerfile from https://docs.docker.com/engine/examples/postgresql_service/
# for more information on commands, visit the above website
FROM ubuntu:16.04

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y libssl1.0.0 software-properties-common postgresql-9.5 postgresql-client-9.5 postgresql-contrib-9.5

USER postgres

# Create a PostgreSQL role named ``ubuntu`` with ``password`` as the password and
# then create a database `evs` owned by the ``ubuntu`` role.
# Also create database tables according to create_tables.sql.
ADD create_tables.sql /tmp/create_tables.sql
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER ubuntu WITH SUPERUSER PASSWORD 'password';" &&\
    createdb -O ubuntu evs &&\
    psql -d evs --command "\i /tmp/create_tables.sql"

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]
