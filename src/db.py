import sqlite3
from typing import List

from ledger import Posting, Transaction


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
    Create the necessary tables in the provided database. Will first attempt to
    drop the tables if they already exist.
    """

    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS postings")

    # SQLite data types: https://www.sqlite.org/datatype3.html
    cursor.execute(
        """
        CREATE TABLE transactions
        (
            id integer,
            date text,
            description text,
            comment text,
            cleared integer,
            tags text
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE postings
        (
            transaction_id integer,
            date text,
            description text,
            account text,
            amount real,
            cleared integer,
            tags text,
            comment text
        )
        """
    )


def get_posting_amount(posting: Posting) -> float:
    # TODO: Is there a way to denote that these fields are required and avoid all the None checking?

    amount = posting.get("pamount")
    if amount is None or len(amount) != 1:
        print("Unexpected number of amounts in posting")
        print(posting)
        return 0

    quantity = amount[0].get("aquantity")
    if quantity is None:
        print("Unexpected number of amounts in posting")
        print(posting)
        return 0

    val = quantity.get("floatingPoint")
    if val is None:
        print("Unexpected number of amounts in posting")
        print(posting)
        return 0

    return val


def write_transactions(cursor: sqlite3.Cursor, txs: List[Transaction]) -> None:
    """
    Convert the transactions into a format that can be stored in the database
    and then store it.
    """

    for transaction in txs:
        comment = transaction.get("tcomment")
        if comment is not None:
            comment = comment.strip()

        cursor.execute(
            """
            INSERT INTO transactions
            (
                id, date, description, comment, cleared, tags
            ) VALUES (
                ?, ?, ?, ?, ?, ?
            )
            """,
            [
                transaction.get("tindex"),
                transaction.get("tdate"),
                transaction.get("tdescription"),
                comment,
                transaction.get("tstatus"),
                ",".join(transaction.get("ttags") or []),
            ],
        )

        postings = transaction.get("tpostings")
        if postings is None:
            continue

        for posting in postings:
            status = posting.get("pstatus")
            if status == "Unmarked":
                status = transaction.get("tstatus")

            comment = posting.get("pcomment")
            if comment is None or comment == "":
                comment = transaction.get("tcomment")
            if comment is not None:
                comment = comment.strip()

            tags = ",".join([":".join(x) for x in posting.get("ptags") or []])
            if tags == "":
                tags = ",".join(transaction.get("ttags") or [])

            cursor.execute(
                """
                INSERT INTO postings
                (
                    transaction_id, date, description, account, amount, cleared, tags, comment
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                [
                    transaction.get("tindex"),
                    transaction.get("tdate"),
                    transaction.get("tdescription"),
                    posting.get("paccount"),
                    get_posting_amount(posting),
                    status,
                    tags,
                    comment,
                ],
            )
