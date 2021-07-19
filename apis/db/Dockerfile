# docker build -t evs-db-api .
FROM python:3.9-alpine3.12


COPY requirements.txt ./
RUN apk update \
  && apk add --no-cache --virtual .build-deps postgresql-dev gcc python3-dev musl-dev \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del .build-deps \
  && apk add --no-cache libpq

COPY ./src ./src
WORKDIR ./src

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
