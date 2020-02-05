FROM library/postgres:9.6-alpine

COPY database-init.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/database-init.sh

EXPOSE 5432
