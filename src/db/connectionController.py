from lib2to3.fixes.fix_input import context
from typing import Generator, Any
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2.pool
from psycopg2.extensions import connection
import psycopg2
from sqlalchemy.engine import cursor


class Connection:
    def __init__(self, user_params, autocommit = False):
        self.autocommit = autocommit
        self.pool = psycopg2.pool.SimpleConnectionPool(1, 10, **user_params)

    @contextmanager
    def get_cursor(self) -> Generator[cursor, Any, None]:
        conn: connection = None

        try:
            conn = self.pool.getconn()
            conn.autocommit = self.autocommit

            yield conn.cursor()
        finally:
            if conn:
                self.pool.putconn(conn)