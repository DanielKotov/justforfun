FROM python:3.10-slim


WORKDIR /service
EXPOSE 8000

RUN apt update -y && \
    apt install -y --no-install-recommends wget xz-utils libfuse2 && \
    mkdir -p /vault/books && \
    mkdir -p /service/db && \
    touch /service/db/db.sqlite3


COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY project/auth /service/auth
COPY project/dao /service/dao

