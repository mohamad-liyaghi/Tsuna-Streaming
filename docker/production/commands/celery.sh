#!/bin/bash

echo "Running celery"
celery -A config worker --loglevel=info