#!/bin/sh
# Define the app root
AROOT="/home/fbc/doc_feedback"
# Define fixture root path,
# a fixture path, a fixture loading marker,
# static collection marker
IROOT="$AROOT/installation"
# Define the installation marker filename
INSTALLED="$AROOT/ready"
# Check that sectet key is available
if [ ! -f "$INSTALLED" ]; then
    echo "export SECRET_KEY='$(openssl rand -hex 40)'" > "$AROOT/.DJANGO_SECRET_KEY"
fi
# Load Django secrets
source "$AROOT/.DJANGO_SECRET_KEY"
# Update PATH
PATH="/home/fbc/.local/bin:${PATH}"
# Migrate automatically
python manage.py makemigrations --noinput
python manage.py migrate --noinput
# Create the admin user if necessary
if [ -f "$INSTALLED" ]; then
    echo "Admin was previously added. Continuing."
else
    echo "Admin not found, adding."
    export DJANGO_SUPERUSER_EMAIL="admin@i2fbccatalog.info"
    export DJANGO_SUPERUSER_USERNAME="admin"
    export DJANGO_SUPERUSER_PASSWORD="admin"
    python manage.py createsuperuser --noinput
    touch $INSTALLED
fi
# Collect static
python manage.py collectstatic --noinput
gunicorn -c config/gunicorn/dev.py
