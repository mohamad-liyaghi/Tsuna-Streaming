#!/bin/bash

echo "Running celery beat worker"
celery -A config beat --loglevel=info