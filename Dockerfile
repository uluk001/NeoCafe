FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Установка supervisord
RUN apt-get update && apt-get install -y supervisor

COPY . .
COPY ../.env ./.env
EXPOSE 8000

ENTRYPOINT [ "bash", "-c", "./entrypoint.sh"]
