#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A lightweight wrapper around psycopg2 (PostgreSQL).
Replaces the original torndb (MySQL) wrapper.
"""

import logging
import time
import psycopg2
import psycopg2.extras
from psycopg2 import OperationalError

class Connection(object):
    def __init__(self, host, database, user=None, password=None, port=5432, **kwargs):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self._db = None
        self._db_args = kwargs
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error(f"Cannot connect to PostgreSQL on {self.host}", exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        self.close()
        self._db = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )
        self._db.autocommit = True

    def _ensure_connected(self):
        if self._db is None or self._db.closed:
            self.reconnect()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def _execute(self, cursor, query, parameters):
        try:
            # Replace %s with %s (same), check for other differences if needed
            return cursor.execute(query, parameters)
        except OperationalError:
            logging.error("Error connecting to PostgreSQL")
            self.close()
            raise

    def query(self, query, *parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return [Row(row) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for get() query")
        else:
            return rows[0]

    def execute(self, query, *parameters):
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            # PostgreSQL doesn't have lastrowid easily accessible without RETURNING
            # returning 0 or rowcount as fallback
            return cursor.rowcount 
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    # Aliases
    update = execute_rowcount
    updatemany = executemany_rowcount
    insert = execute_lastrowid
    insertmany = executemany_lastrowid

class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
