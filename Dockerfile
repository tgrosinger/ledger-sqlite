# TODO: Change this to a multiarch hledger image
FROM dastapov/hledger:1.26 as hledger

FROM library/python:3.10-slim

COPY --from=hledger /usr/bin/hledger /usr/bin/hledger

COPY src /code

# TODO: Support more than one ledger file
ENV LEDGER_FILE=/data/all.ledger
ENV OUTPUT_FILE=/data/all.sqlite
ENV OVERWRITE_OUTPUT=true

ENTRYPOINT ["python", "/code/export.py"]
