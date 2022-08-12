# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV APP_SETTINGS "config.DevelopmentConfig"
ENV DATABASE_URL "postgresql://admin:admin123@localhost:5432/collect"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /project
