ARG APP_DIR="/app"

FROM python:3.11-slim
# FROM mcr.microsoft.com/appsvc/python:3.11
ARG APP_DIR

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ${APP_DIR}/
RUN pip3 install --no-cache-dir -r ${APP_DIR}/requirements.txt 

COPY app/*.py ${APP_DIR}/

ENV PORT 8080
EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/uvicorn", "--port", "8080", "--host", "0.0.0.0", "--app-dir", "/app", "--access-log", "--no-use-colors", "main:app"]