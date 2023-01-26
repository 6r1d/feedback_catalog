FROM python:3.12-rc-alpine3.17

RUN pip install --upgrade pip

RUN mkdir /var/log/gunicorn
RUN mkdir /var/run/gunicorn
RUN mkdir /home/fbc

RUN addgroup -S fbc
RUN adduser -s /bin/bash -h /home/fbc -S fbc -G fbc
RUN chown fbc:fbc /home/fbc
RUN chown fbc:fbc /var/run/gunicorn
RUN chown fbc:fbc /var/log/gunicorn
USER fbc

WORKDIR /home/fbc
# Note on RUNs https://github.com/moby/moby/issues/37965
RUN mkdir doc_feedback
COPY doc_feedback /home/fbc/doc_feedback
WORKDIR /home/fbc/doc_feedback
RUN rm -f db.sqlite3
RUN rm -f .DJANGO_SECRET_KEY

ENV PATH="/home/fbc/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt

LABEL maintainer="Victor Gridnevsky <gridnevsky@soramitsu.co.jp>" \
      version="0.1.0"
