# docker build -t evs-front-api .
FROM python:3.9-alpine3.12

COPY app.py requirements.txt demo.json ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
