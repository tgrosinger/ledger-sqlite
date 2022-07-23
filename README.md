# Ledger SQLite

A simple containerized utility which creates a SQLite database from the contents of a ledger file. Uses [hledger](https://hledger.org) to output JSON which is then transformed into a database schema.

Exports are not designed to be consistent across iterations. It is recommended that you start from a fresh databse every export.

## Usage

The default configuration is to run in a long-lived mode where the conversion will happen on a regular schedule defined by cron. You can use [crontab guru](https://crontab.guru) to build the value for the `CRONTAB_SCHEDULE` variable.

```
docker run \
    --name ledger-sqlite \
    --env "LEDGER_FILE=/data/journal.ledger" \
    --env "OUTPUT_FILE=/data/journal.sqlite" \
    --env "CRONTAB_SCHEDULE=0 15 * * *" \
    -v /path/to/data:/data \
    ghcr.io/tgrosinger/ledger-sqlite:latest
```

Alternatively, a single conversion can be performed and the container will exit when complete. This can also be useful for debugging as the logs are easier to retrieve.

```
docker run \
    --rm
    --env "LEDGER_FILE=/data/journal.ledger" \
    --env "OUTPUT_FILE=/data/journal.sqlite" \
    -v /path/to/data:/data \
    --entrypoint python \
    ghcr.io/tgrosinger/ledger-sqlite:latest \
    /code/main.py

```
