FROM python:3.11.3-slim AS base
WORKDIR /app
COPY requirements /app/requirements
RUN apt-get update && apt-get -y install build-essential python-dev wget tzdata
RUN pip install -r requirements/backend.txt

FROM base AS dev
ENV DEBUG "True"
ENV TZ Europe/Kiev

FROM base AS prd

COPY forecaster_http /app/forecaster_http
COPY forecaster_teletram /app/forecaster_telegram
COPY forecaster /app/forecaster
COPY forecaster_jobs /app/forecaster_jobs
COPY scripts app/scripts

ENV DEBUG "False"
ENV TZ Europe/Kiev
