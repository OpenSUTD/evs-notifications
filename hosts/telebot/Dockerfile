# docker build -t evs-telebot .
FROM python:3.9-alpine3.12

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
WORKDIR ./src

CMD ["python3", "main.py"]
