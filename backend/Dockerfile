FROM python:3.12-rc-alpine3.17

RUN mkdir /var/log/gunicorn
RUN mkdir /var/run/gunicorn
RUN mkdir /home/fbc

RUN addgroup -S fbc
RUN adduser -s /bin/bash -h /home/fbc -S fbc -G fbc
RUN chown fbc:fbc /home/fbc
RUN chown fbc:fbc /var/run/gunicorn
RUN chown fbc:fbc /var/log/gunicorn
# Install openssl
RUN apk add openssl
# Switch the user and work dir
USER fbc
WORKDIR /home/fbc
# Note on RUNs https://github.com/moby/moby/issues/37965
RUN mkdir doc_feedback
COPY doc_feedback /home/fbc/doc_feedback
WORKDIR /home/fbc/doc_feedback
RUN rm -f db.sqlite3
# Delete the unrelated key, generate a new one and reload Iroha
RUN rm -f .DJANGO_SECRET_KEY
RUN echo "export SECRET_KEY='$(openssl rand -hex 40)'" > .DJANGO_SECRET_KEY
# Update path
ENV PATH="/home/fbc/.local/bin:${PATH}"
# Update PIP and install its packages
RUN python -m pip install --upgrade pip
RUN pip install --user -r requirements.txt
# Load the secret key
RUN source .DJANGO_SECRET_KEY
RUN chmod +x ./.DJANGO_SECRET_KEY
SHELL ["/bin/sh", "-c", "./.DJANGO_SECRET_KEY"] 
RUN echo $SECRET_KEY
# Migrate the DB
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput

LABEL maintainer="Victor Gridnevsky <gridnevsky@soramitsu.co.jp>" \
      version="0.3.0"
