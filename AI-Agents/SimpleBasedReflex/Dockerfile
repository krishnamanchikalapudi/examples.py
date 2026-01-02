FROM python:3.12-alpine  # https://hub.docker.com/_/python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


CMD ["python", "app.py"]