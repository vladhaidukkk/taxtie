from contextlib import contextmanager
from sqlite3 import Connection


@contextmanager
def execute_query(conn: Connection, query: str, params=()):
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()
        yield cur
    finally:
        cur.close()
