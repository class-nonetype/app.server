#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE app.storage;
    CREATE USER dev WITH PASSWORD 'dev';
    GRANT ALL PRIVILEGES ON DATABASE app.storage TO dev;
EOSQL