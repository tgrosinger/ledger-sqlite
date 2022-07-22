import sqlite3
from typing import List

from ledger import Transaction


class CursorContextManager:
    """
    CursorContextManager is a ContextManager for a SQLite database. Provides a
    Cursor to interact with the database.
    """

    _filename: str
    _conn: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, filename: str):
        self._filename = filename

    def __enter__(self):
        self._conn = sqlite3.connect(self._filename)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()


def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Create the necessary tables in the provided database.
    """

    # SQLite data types: https://www.sqlite.org/datatype3.html
    cursor.execute(
        """
        CREATE TABLE transactions
        (
            date text,
            check_num text,
            note text,
            account text,
            amount real,
            cleared integer,
            tags text
        )
        """
    )


def write_transactions(cursor: sqlite3.Cursor, txs: List[Transaction]) -> None:
    """
    Convert the transactions into a format that can be stored in the database
    and then store it.
    """

    print(txs[0])
