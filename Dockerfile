FROM python:3.11-alpine

ENV SERVICE=app

WORKDIR /app

COPY ./entrypoint.sh ./entrypoint.sh
COPY ./requirements.txt ./requirements.txt

RUN set -xe \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./src ./

RUN set -xe \
    && addgroup -S ${SERVICE} \
    && adduser -G ${SERVICE} -SDH ${SERVICE} \
    && chown -R ${SERVICE}:${SERVICE} . 

USER ${SERVICE}

EXPOSE 8000
