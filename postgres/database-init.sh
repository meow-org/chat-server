#!/bin/bash

set -e
set -u

function create_user_and_database() {
	echo "  Creating database '$1'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE DATABASE $1;
EOSQL
}

if [ -n "$POSTGRES_TEST_DB" ]; then
	echo "Tests database creation requested: $POSTGRES_TEST_DB"
	create_user_and_database $POSTGRES_TEST_DB
	echo "Test database created"
fi