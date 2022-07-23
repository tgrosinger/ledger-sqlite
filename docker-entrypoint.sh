#!/bin/sh

# Inspired by https://github.com/dkruger/docker-cron

cat << EOF > /var/spool/cron/crontabs/root
${CRONTAB_ENTRY} python /code/main.py
EOF

exec "$@"
