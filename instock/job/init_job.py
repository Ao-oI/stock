#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import psycopg2
import os
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.database as mdb

__author__ = 'myh '
__date__ = '2023/3/10 '

def create_new_database():
    # Connect to default 'postgres' database to create new db
    sys_db_params = mdb.MYSQL_CONN_DBAPI.copy()
    sys_db_params['database'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**sys_db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (mdb.db_database,))
            if not cur.fetchone():
                cur.execute(f'CREATE DATABASE "{mdb.db_database}"')
                logging.info(f"Database {mdb.db_database} created.")
            else:
                logging.info(f"Database {mdb.db_database} already exists.")
        conn.close()
        
        # Now create tables in the new database
        create_new_base_table()
        
    except Exception as e:
        logging.error(f"init_job.create_new_database exception: {e}")

def create_new_base_table():
    try:
        with mdb.get_connection() as conn:
            with conn.cursor() as db:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS cn_stock_attention (
                    datetime TIMESTAMP NULL,
                    code VARCHAR(6) NOT NULL,
                    PRIMARY KEY (code)
                );
                CREATE INDEX IF NOT EXISTS idx_datetime ON cn_stock_attention (datetime);
                """
                db.execute(create_table_sql)
                logging.info("Base tables created.")
    except Exception as e:
        logging.error(f"init_job.create_new_base_table exception: {e}")

def check_database():
    with mdb.get_connection() as conn:
        with conn.cursor() as db:
            db.execute("SELECT 1")

def main():
    try:
        check_database()
        logging.info("Database check passed.")
        # Ensure base tables exist even if DB exists
        create_new_base_table()
    except Exception as e:
        logging.error(f"Database check failed, attempting to create: {e}")
        create_new_database()

if __name__ == '__main__':
    main()
