# docker build -t pg_test .
FROM postgres:9.5
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB evs
ADD create_tables.sql /docker-entrypoint-initdb.d/

