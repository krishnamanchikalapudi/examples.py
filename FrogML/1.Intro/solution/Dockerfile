# https://hub.docker.com/_/python
# FROM python:3.11-slim⁠
FROM psazuse.jfrog.io/krishnam-docker-virtual/python:3.11-slim⁠

WORKDIR /app
RUN mkdir -p api && chmod -R 755 /app

COPY solution/src/. /app/

RUN pip3 install --compile --disable-pip-version-check --no-cache-dir -r requirements.txt 
RUN python3 -m compileall .

EXPOSE 5000
#WORKDIR /app
ENV FLASK_APP PredictApi.py
ENV FLASK_ENV development
CMD [ "flask", "run", "--host", "0.0.0.0"]