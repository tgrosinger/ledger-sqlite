# Ledger SQLite

A simple containerized utility which creates a SQLite database from the contents of a ledger file. Uses [hledger](https://hledger.org) to output JSON which is then transformed into a database schema.

Exports are not designed to be consistent across iterations. It is recommended that you start from a fresh databse every export.

## Usage

TBD

Currently planning on designing the container to be able to run as a long-lived job with a cron schedule for exporting. There will also be a method for running as a one-off.
