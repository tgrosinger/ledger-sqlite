"""
Convert the provided ledger file into a SQLite database.
Configure input and output files with environment variables.
"""

import os
import os.path
import sys

from db import CursorContextManager, create_tables, write_transactions
from ledger import get_transactions


# TODO: Replace with os.environ.get() and produce nice error messages.
ledger_file = os.environ["LEDGER_FILE"]
output_file = os.environ["OUTPUT_FILE"]
overwrite_output = os.environ["OVERWRITE_OUTPUT"]

print(f"Converting {ledger_file} to {output_file}")


def to_bool(val: str) -> bool:
    """
    Return if the provided string is consider truthy.
    """
    return val.lower() in ["true", "1", "t", "y", "yes"]


if os.path.exists(output_file):
    if not to_bool(overwrite_output):
        print("Output file exists. Set OVERWRITE_OUTPUT=true to overwrite.")
        sys.exit(1)
    else:
        print("Output file exists. Overwriting.")

txs = get_transactions(ledger_file)

with CursorContextManager(filename=output_file) as db:
    create_tables(db)
    write_transactions(db, txs)


print("Conversion complete.")
