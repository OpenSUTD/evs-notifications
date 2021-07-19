# docker build -t evs-web-api .
FROM python:3.9-alpine3.12

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
WORKDIR ./src

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
