ARG APP_DIR="/app"

FROM python:3.11-slim
ARG APP_DIR

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt ${APP_DIR}/
RUN pip3 install --no-cache-dir -r ${APP_DIR}/requirements.txt

COPY app/*.py ${APP_DIR}/

# Must be set to port 80 for Azure App Service to work!
ENV PORT 80
EXPOSE 80

ENTRYPOINT ["/usr/local/bin/uvicorn", "--port", "80", "--host", "0.0.0.0", "--app-dir", "/app", "--access-log", "--no-use-colors", "main:app"]