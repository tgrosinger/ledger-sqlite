# TODO: Change this to a multiarch hledger image
FROM dastapov/hledger:1.26 as hledger

FROM library/python:3.10-slim

RUN apt update && \
    apt install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}

COPY --from=hledger /usr/bin/hledger /usr/bin/hledger

COPY src /code
COPY docker-entrypoint.sh /entrypoint.sh

# TODO: Support more than one ledger file
ENV LEDGER_FILE=/data/all.ledger
ENV OUTPUT_FILE=/data/all.sqlite
ENV OVERWRITE_OUTPUT=true
ENV CRONTAB_SCHEDULE="0 15 * * *"

ENTRYPOINT ["sh", "/entrypoint.sh"]
CMD ["crond", "-f", "-l", "0"]
