#!/bin/sh

if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
    LOGLEVEL="CRITICAL"
else
    LOGLEVEL="DEBUG"
fi

echo "Running flower worker..."
celery -A config.celery flower --loglevel=$LOGLEVEL