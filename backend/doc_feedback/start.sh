#!/bin/sh
# Define fixture root path,
# a fixture path, a fixture loading marker,
# static collection marker
IROOT="/home/fbc/doc_feedback/installation"
FIXTURES="$IROOT/base.json"
INSTALLED="/home/fbc/ready"
# Load Django secrets
source /run/secrets/django_secret
# Migrate before changing data
python manage.py makemigrations --noinput
python manage.py migrate --noinput
# Load fixtures if necessary
if [ -f "$INSTALLED" ]; then
    echo "Initial data was previously added. Continuing."
else
    echo "Initial data not found, adding Django fixtures."
    python manage.py loaddata $FIXTURES
    touch $INSTALLED
fi
# Collect static
python manage.py collectstatic --noinput
gunicorn -c config/gunicorn/dev.py
